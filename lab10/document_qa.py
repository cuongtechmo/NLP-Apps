import argparse
import torch
from transformers import AutoTokenizer
from qa_model import ExtractiveQAModel, decode_best_span


def answer_question(question: str, context: str, model_path_or_name: str, max_length: int = 384, stride: int = 128) -> dict:
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    tokenizer = AutoTokenizer.from_pretrained(model_path_or_name)
    model = ExtractiveQAModel(model_path_or_name).to(device)
    model.eval()

    encodings = tokenizer(
        question,
        context,
        truncation="only_second",
        max_length=max_length,
        stride=stride,
        return_overflowing_tokens=True,
        return_offsets_mapping=True,
        padding="max_length",
    )

    best_answer = ""
    best_confidence = -1.0

    with torch.no_grad():
        for i in range(len(encodings["input_ids"])):
            input_ids = torch.tensor([encodings["input_ids"][i]], device=device)
            attention_mask = torch.tensor([encodings["attention_mask"][i]], device=device)
            token_type_ids = (
                torch.tensor([encodings["token_type_ids"][i]], device=device)
                if "token_type_ids" in encodings
                else None
            )
            offsets = encodings["offset_mapping"][i]

            out = model(
                input_ids=input_ids,
                attention_mask=attention_mask,
                token_type_ids=token_type_ids,
            )
            start_probs = torch.softmax(out["start_logits"][0], dim=-1)
            end_probs = torch.softmax(out["end_logits"][0], dim=-1)
            conf = float(start_probs.max() * end_probs.max())

            pred_text = decode_best_span(
                out["start_logits"][0],
                out["end_logits"][0],
                offsets,
                context,
            )
            if pred_text and conf > best_confidence:
                best_confidence = conf
                best_answer = pred_text

    return {
        "question": question,
        "answer": best_answer,
        "confidence": round(best_confidence, 4),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Mini Document Extractive QA")
    parser.add_argument("--question", type=str, required=True)
    parser.add_argument("--context", type=str, required=True)
    parser.add_argument("--model", type=str, default="bert-base-uncased")
    args = parser.parse_args()

    result = answer_question(args.question, args.context, args.model)
    print(result)