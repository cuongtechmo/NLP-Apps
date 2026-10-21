## Prediction 1: Word Order Handling (TF-IDF + Logistic Regression vs. RNN + Embedding)

* **Prediction:** **RNN + Embedding** có khả năng xử lý thứ tự từ (word order) trực tiếp và hiệu quả hơn hẳn **TF-IDF + Logistic Regression**.
* **Reason:**
  * **TF-IDF** dựa trên mô hình *Bag-of-Words* (tập hợp các từ không có thứ tự). Biểu diễn này hoàn toàn triệt tiêu thông tin vị trí của từ trong câu (ví dụ: *"this movie is not good"* và *"this movie is good, not"* có vector biểu diễn hoàn toàn giống nhau nếu cùng tần suất).
  * **RNN** đọc chuỗi theo từng mốc thời gian $t$ thông qua công thức đệ quy $h_t = \tanh(W_{xh} x_t + W_{hh} h_{t-1} + b_h)$. Trạng thái ẩn $h_t$ liên tục cập nhật dựa trên thông tin tích lũy từ các token trước đó, giúp mô hình duy trì và mô hình hóa trực tiếp mối quan hệ thứ tự và ngữ cảnh của chuỗi.
* **Confidence:** High (95%)

---

## Prediction 2: Long-Range Dependency Handling (Simple RNN vs. LSTM)

* **Prediction:** **LSTM** có khả năng học và duy trì phụ thuộc xa (long-range dependency) tốt hơn nhiều so với **Simple RNN**.
* **Reason:**
  * **Simple RNN** gặp hiện tượng **Vanishing Gradient** (biến mất đạo hàm) nghiêm trọng khi lan truyền ngược qua thời gian (BPTT). Đạo hàm của trạng thái ẩn $\frac{\partial h_T}{\partial h_t} = \prod_{k=t+1}^{T} \frac{\partial h_k}{\partial h_{k-1}}$ chứa tích liên tiếp của các ma trận trọng số $W_{hh}$ và đạo hàm hàm kích hoạt $\tanh'$ (luôn $\le 1$). Khi chuỗi dài, giá trị này tiến tiệm cận về $0$, khiến RNN "quên" ngữ cảnh ở các bước đầu tiên.
  * **LSTM** giới thiệu cơ chế **Cell State ($c_t$)** hoạt động như một "đường cao tốc thông tin" tuyến tính (*constant error carousel*). Luồng thông tin trên Cell State được điều phối bởi 3 cổng:
    * **Forget Gate ($f_t$):** Quyết định lượng thông tin cũ cần giữ lại.
    * **Input Gate ($i_t$):** Quyết định lượng thông tin mới cần cập nhật.
    * **Output Gate ($o_t$):** Quyết định thông tin xuất ra trạng thái ẩn $h_t$.
    
    Cấu trúc cộng $c_t = f_t \odot c_{t-1} + i_t \odot \tilde{c}_t$ giúp gradient có thể truyền ngược về quá khứ mà không bị nhân dồn triệt tiêu như RNN.
* **Confidence:** High (95%)

---

## Prediction 3: Effect of Increasing Sequence Length ($50 \rightarrow 200$) on RNN Training

* **Prediction:** Khi tăng `max_length` từ $50$ lên $200$:
  1. **Thời gian huấn luyện (Training Time)** và **bộ nhớ GPU/RAM** sẽ tăng xấp xỉ tuyến tính (gấp ~4 lần).
  2. **Quá trình huấn luyện của RNN sẽ trở nên kém ổn định hơn**, nguy cơ bị trôi/biến mất gradient (Vanishing/Exploding Gradient) tăng cao.
* **Reason:**
  * Thuật toán Backpropagation Through Time (BPTT) phải duỗi (unroll) đồ thị tính toán qua $T$ bước thời gian. Độ dài $T$ tăng từ 50 lên 200 làm tăng gấp 4 lần số lượng phép nhân ma trận ở cả Forward pass và Backward pass.
  * Việc lan truyền đạo hàm qua 200 bước đệ quy khiến chuỗi nhân ma trận Jacobian dài hơn gấp 4 lần, làm hiện tượng Vanishing Gradient trầm trọng hơn, khiến RNN rất khó học được ngữ cảnh ở đầu chuỗi 200 token.
* **Confidence:** High (90%)

---

## Prediction 4: Impact of Severe Truncation (`max_length = 30`)

* **Prediction:** Việc truncate toàn bộ review về $30$ tokens sẽ **làm giảm đáng kể độ chính xác (Accuracy/F1-score)** của mô hình phân loại cảm xúc.
* **Reason:**
  * Độ dài trung bình của các bài đánh giá phim trên tập dữ liệu IMDb thường lớn hơn $200$ từ.
  * Việc cắt ngắn chỉ lấy 30 token đầu tiên làm mất toàn bộ đoạn kết luận quan trọng phía sau, dẫn đến việc mô hình đưa ra dự đoán sai lệch.
* **Confidence:** High (90%)

---

## Prediction 5: Universal Superiority of LSTM over RNN

* **Prediction:** **Không chắc chắn.** LSTM **không phải lúc nào cũng đạt Accuracy cao hơn RNN trên mọi tập dữ liệu**.
* **Reason:**
  * **Với chuỗi rất ngắn (Short Sequences, ví dụ $< 10-15$ tokens):** RNN cơ bản không bị ảnh hưởng nặng bởi Vanishing Gradient và hoàn toàn có khả năng học tốt ngữ cảnh ngắn.
  * **Vấn đề số lượng tham số và Overfitting:** LSTM có số lượng tham số gấp khoảng 4 lần so với Simple RNN (do có 4 bộ ma trận trọng số cho $f_t, i_t, o_t, \tilde{c}_t$). Nếu tập dữ liệu huấn luyện có kích thước quá nhỏ, LSTM dễ bị học vẹt (**overfitting**) hơn so với Simple RNN nếu không được áp dụng các phương pháp regularization (như Dropout hay Weight Decay) phù hợp.
* **Confidence:** High (95%)