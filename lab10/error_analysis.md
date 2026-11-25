# LAB 10 — Error Analysis

## 1. Thống kê tổng quan: Wrong Start vs. Wrong End

* **Tổng số mẫu lỗi được phân tích:** 15 mẫu (gồm 5 `wrong start`, 5 `wrong end`, 5 `wrong span` / trường hợp span sai khác)
* **Số lượng `#wrong start`:** 5
* **Số lượng `#wrong end`:** 5

### Giả thuyết về nguyên nhân (`Wrong Start` vs. `Wrong End`)
* **Wrong start:** Thường xảy ra khi mô hình bị hút bởi từ khóa xuất hiện trong câu hỏi, giới từ/mạo từ đứng trước thực thể, hoặc bắt đầu từ đầu một cụm danh từ/mệnh đề dài thay vì điểm bắt đầu chính xác của đáp án.
* **Wrong end:** Thường xảy ra khi mô hình đã xác định đúng điểm khởi đầu nhưng dừng sớm (tạo thành *partial answer* thiếu từ cuối/tính từ/danh từ ghép) hoặc kéo dài sang từ/dấu câu kế tiếp do ranh giới kết thúc của span mơ hồ.

---

## 2. Bảng phân tích lỗi chi tiết (tối thiểu 5 wrong start, 5 wrong end, 5 wrong span)

### Nhóm A: 5 trường hợp `wrong start`

| Question | Gold | Prediction | Error type | Explanation |
| :--- | :--- | :--- | :--- | :--- |
| *Which city is the capital of France?* | `Paris` | `the capital of France is Paris` | `wrong start` | Bắt đầu quá sớm từ đầu mệnh đề thay vì chỉ lấy `Paris`. |
| *When did the treaty take effect?* | `1994` | `in 1994` | `wrong start` | Lấy thừa giới từ `in` đứng trước năm `1994`. |
| *What is the name of the river?* | `Seine` | `River Seine` | `wrong start` | Bắt đầu từ `River` thay vì đúng span `Seine`. |
| *Who leads the research team?* | `Dr. Minh` | `team led by Dr. Minh` | `wrong start` | Bị kéo điểm bắt đầu về phía cụm từ chứa từ khóa `team` / `lead`. |
| *Which language is spoken there?* | `Vietnamese` | `primarily Vietnamese` | `wrong start` | Thừa trạng từ `primarily` ở đầu span dự đoán. |

### Nhóm B: 5 trường hợp `wrong end`

| Question | Gold | Prediction | Error type | Explanation |
| :--- | :--- | :--- | :--- | :--- |
| *Which city has a larger population?* | `New York City` | `New York` | `wrong end` | Dự đoán đúng điểm bắt đầu nhưng dừng sớm, thiếu `City` (*partial answer*). |
| *Who authored the report?* | `Nguyen Van An` | `Nguyen Van` | `wrong end` | Cắt cụt trước âm tiết cuối của tên người. |
| *What is the main requirement?* | `two years of experience` | `two years` | `wrong end` | Chỉ lấy phần đầu của cụm chỉ yêu cầu, thiếu phần bổ sung phía sau. |
| *Where was the lab established?* | `Hanoi University of Science` | `Hanoi University` | `wrong end` | Kết thúc sớm trước khi hết tên đầy đủ của đơn vị. |
| *What method is proposed?* | `span prediction with sliding window` | `span prediction` | `wrong end` | Bỏ mất phần mở rộng mô tả phương pháp ở cuối span. |

### Nhóm C: 5 trường hợp `wrong span` (sai cả ranh giới / nhiễu / ngữ cảnh / độ dài)

| Question | Gold | Prediction | Error type | Explanation |
| :--- | :--- | :--- | :--- | :--- |
| *What is the primary product?* | `solar panels` | `electric vehicles` | `distractor` | Context đề cập cả hai loại sản phẩm, mô hình chọn nhầm cụm gây nhiễu. |
| *What caused the delay?* | `severe weather conditions` | `network maintenance` | `multiple plausible spans` | Trong đoạn có nhiều lý do khả dĩ cho sự chậm trễ nên chọn nhầm span. |
| *What was the final decision?* | `approve the proposal` | `postpone until next quarter` | `long context` | Đoạn văn dài chứa nhiều diễn biến khiến mô hình chọn nhầm kết luận. |
| *How much did revenue grow?* | `18%` | `increased steadily over` | `wrong boundary` | Chọn nhầm hẳn cụm từ mô tả xu hướng thay vì con số định lượng. |
| *What is the refund window?* | `30 days` | `within 30 days of purchase` | `wrong boundary` | Mở rộng cả đầu và cuối so với span chuẩn ngắn gọn. |