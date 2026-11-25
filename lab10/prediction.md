# LAB 10 — Prediction Before Experiment

## 1. Tại sao cần hai prediction (`start` và `end`) thay vì chỉ một prediction?

Trong bài toán **Extractive Question Answering**, câu trả lời là một span liên tục $A = C_{i:j}$ nằm trong ngữ cảnh $C$, bắt đầu tại vị trí token $i$ và kết thúc tại vị trí token $j$ (với $i \le j$).

* Nếu mô hình chỉ dự đoán **một vị trí duy nhất**, nó chỉ biết một điểm mốc mà không xác định được ranh giới còn lại hoặc độ dài của cụm từ trả lời—đặc biệt khi đáp án gồm nhiều từ (như *"New York City"* hoặc *"museums and architectural landmarks"*).
* Khi tách thành hai đầu dự đoán $P_{\text{start}}(i)$ và $P_{\text{end}}(j)$ với hàm mất mát trung bình:
  $$L = \frac{L_{\text{start}} + L_{\text{end}}}{2}$$
  mô hình có thể học riêng biệt tín hiệu mở đầu và tín hiệu kết thúc của span trong biểu diễn ngữ cảnh của từng token.

---

## 2. Dự đoán trước khi chạy thực nghiệm (Predictions Before Experiment)

### Prediction 1 — Trùng lặp từ vựng cao giữa Question và Context
* **Câu hỏi:** Nếu `question` và `context` chứa nhiều từ giống nhau nhưng chỉ một vị trí thực sự trả lời câu hỏi, model có dễ bị nhầm không?
* **Dự đoán:** **Có, dễ bị nhầm** (đặc biệt ở giai đoạn đầu huấn luyện hoặc ở baseline dựa trên từ khóa). Các từ trùng khớp dễ kéo điểm chú ý/xác suất về phía các câu hoặc cụm từ chứa nhiều từ giống câu hỏi thay vì vị trí chứa đáp án thực sự, nhất là khi có nhiều mệnh đề tương tự nhau.

### Prediction 2 — Độ dài Answer Span và độ khó dự đoán ranh giới
* **Câu hỏi:** Answer span càng dài thì boundary prediction có khó hơn không?
* **Dự đoán:** **Có, khó hơn**. Span càng dài thì khoảng cách giữa `start` và `end` càng lớn, số cặp ranh giới hợp lệ càng nhiều và khả năng mô hình bị thiếu/thừa từ ở đầu hoặc cuối (ví dụ lấy thiếu từ cuối hoặc kéo thêm mạo từ/giới từ/mệnh đề phụ) càng cao, khiến `EM` giảm mạnh hơn `F1`.

### Prediction 3 — Context chứa nhiều thông tin không liên quan / Distractor
* **Câu hỏi:** Nếu `context` chứa nhiều thông tin không liên quan hoặc đoạn gây nhiễu (*distractor*), hiệu năng sẽ thay đổi như thế nào?
* **Dự đoán:** **Hiệu năng (`EM` và `F1`) có xu hướng giảm**. Thông tin nhiễu làm loãng ngữ cảnh và tạo thêm các ứng viên span trông có vẻ hợp lý với câu hỏi; nếu độ dài vượt `max_length`, việc cắt cụt hoặc chia cửa sổ (`stride`) cũng làm tăng nguy cơ bỏ sót hoặc chọn nhầm đoạn chứa đáp án.

### Prediction 4 — Thay đổi thứ tự một số câu trong Context nhưng giữ nguyên Answer
* **Câu hỏi:** Nếu chỉ thay đổi thứ tự một số câu trong `context` nhưng giữ nguyên `answer`, model có bị ảnh hưởng không?
* **Dự đoán:** **Có thể bị ảnh hưởng ở mức độ vừa/nhẹ tùy ngữ cảnh**. Nếu câu chứa đáp án vẫn giữ nguyên vẹn và các câu bị đổi vị trí không làm đứt gãy tham chiếu đại từ/mốc thời gian/ngữ cảnh lân cận, mô hình vẫn có thể tìm ra đáp án; tuy nhiên thay đổi trật tự diễn đạt có thể làm lệch phân phối ngữ cảnh toàn cục hoặc đưa câu chứa đáp án sang cửa sổ/vị trí khác.