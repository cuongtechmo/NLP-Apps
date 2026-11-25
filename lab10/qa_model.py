import re
import string
from typing import Dict, List, Tuple
import torch
import torch.nn as nn
import torch.nn.functional as F
from transformers import AutoModel


def normalize_answer(text: str) -> str:
  """Chuẩn hóa câu trả lời theo chuẩn SQuAD: lowercase, bỏ dấu câu, bỏ mạo từ a/an/the, chuẩn hóa khoảng trắng."""

  def remove_articles(s: str) -> str:
    return re.sub(r"\b(a|an|the)\b", " ", s)

  def white_space_fix(s: str) -> str:
    return " ".join(s.split())

  def remove_punc(s: str) -> str:
    exclude = set(string.punctuation)
    return "".join(ch for ch in s if ch not in exclude)

  def lower(s: str) -> str:
    return s.lower()

  return white_space_fix(remove_articles(remove_punc(lower(text))))


def compute_exact_match(prediction: str, ground_truth: str) -> float:
  return float(normalize_answer(prediction) == normalize_answer(ground_truth))


def compute_f1_score(prediction: str, ground_truth: str) -> float:
  pred_tokens = normalize_answer(prediction).split()
  gold_tokens = normalize_answer(ground_truth).split()

  if not pred_tokens and not gold_tokens:
    return 1.0
  if not pred_tokens or not gold_tokens:
    return 0.0

  common = {}
  for tok in pred_tokens:
    common[tok] = common.get(tok, 0) + 1

  num_same = 0
  for tok in gold_tokens:
    if common.get(tok, 0) > 0:
      num_same += 1
      common[tok] -= 1

  if num_same == 0:
    return 0.0

  precision = num_same / len(pred_tokens)
  recall = num_same / len(gold_tokens)
  return (2 * precision * recall) / (precision + recall)


def keyword_overlap_baseline(question: str, context: str) -> str:
  """Baseline đơn giản: chọn câu trong context có độ trùng từ khóa cao nhất với câu hỏi."""
  q_words = set(normalize_answer(question).split()) - {
      "what",
      "who",
      "where",
      "when",
      "which",
      "why",
      "how",
      "is",
      "are",
      "was",
      "were",
  }
  sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", context) if s.strip()]
  if not sentences:
    return context

  best_sentence = sentences[0]
  best_score = -1.0

  for sent in sentences:
    s_words = normalize_answer(sent).split()
    if not s_words:
      continue
    overlap = sum(1 for w in s_words if w in q_words)
    # Chuẩn hóa nhẹ theo độ dài câu để tránh thiên vị câu quá dài
    score = overlap / (len(s_words) ** 0.5)
    if score > best_score:
      best_score = score
      best_sentence = sent

  return best_sentence


class ExtractiveQAModel(nn.Module):
  """Backbone Transformer + Start/End classification heads."""

  def __init__(self, model_name: str = "bert-base-uncased"):
    super().__init__()
    self.encoder = AutoModel.from_pretrained(model_name)
    hidden_size = self.encoder.config.hidden_size
    self.qa_outputs = nn.Linear(hidden_size, 2)  # [start_logit, end_logit]

  def forward(
      self,
      input_ids: torch.Tensor,
      attention_mask: torch.Tensor,
      token_type_ids: torch.Tensor = None,
      start_positions: torch.Tensor = None,
      end_positions: torch.Tensor = None,
  ) -> Dict[str, torch.Tensor]:
    kwargs = {"input_ids": input_ids, "attention_mask": attention_mask}
    if (
        token_type_ids is not None
        and "token_type_ids" in self.encoder.forward.__code__.co_varnames
    ):
      kwargs["token_type_ids"] = token_type_ids

    outputs = self.encoder(**kwargs)
    sequence_output = outputs.last_hidden_state  # (batch_size, seq_len, hidden)

    logits = self.qa_outputs(sequence_output)  # (batch_size, seq_len, 2)
    start_logits, end_logits = logits.split(1, dim=-1)
    start_logits = start_logits.squeeze(-1)  # (batch_size, seq_len)
    end_logits = end_logits.squeeze(-1)  # (batch_size, seq_len)

    loss = None
    if start_positions is not None and end_positions is not None:
      loss_start = F.cross_entropy(start_logits, start_positions)
      loss_end = F.cross_entropy(end_logits, end_positions)
      loss = 0.5 * (loss_start + loss_end)

    return {
        "loss": loss,
        "start_logits": start_logits,
        "end_logits": end_logits,
    }


def decode_best_span(
    start_logits: torch.Tensor,
    end_logits: torch.Tensor,
    offsets: List[Tuple[int, int]],
    context: str,
    max_answer_len: int = 30,
) -> str:
  """Chọn cặp (i, j) với i <= j có tổng logit lớn nhất và ánh xạ ngược ra chuỗi ký tự của context."""
  start_probs = F.softmax(start_logits, dim=-1).detach().cpu().numpy()
  end_probs = F.softmax(end_logits, dim=-1).detach().cpu().numpy()

  best_score = -1.0
  best_span = (0, 0)

  seq_len = len(offsets)
  for i in range(seq_len):
    if offsets[i] == (0, 0):
      continue
    for j in range(i, min(seq_len, i + max_answer_len)):
      if offsets[j] == (0, 0):
        continue
      # Đảm bảo cả i và j đều nằm trên cùng một phần context (offset[j][1] >= offset[i][0])
      if offsets[j][1] < offsets[i][0]:
        continue
      score = float(start_probs[i] * end_probs[j])
      if score > best_score:
        best_score = score
        best_span = (offsets[i][0], offsets[j][1])

  char_start, char_end = best_span
  if char_end <= char_start:
    return ""
  return context[char_start:char_end]