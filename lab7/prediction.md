# 8. Prediction trước experiment

**Prediction 1: Một Transformer có thể xử lý các token trong sequence song song hơn RNN không?**
* **Prediction:** Có.
* **Reason:** RNN tính toán trạng thái ẩn nối tiếp theo từng bước thời gian ($t_1 \rightarrow t_2 \rightarrow t_3$), khiến bước sau bắt buộc phải chờ bước trước. Trong khi đó, cơ chế Self-Attention của Transformer cho phép tính toán ma trận giữa tất cả các token trong chuỗi cùng một lúc trên GPU.
* **Confidence:** 95%

---

**Prediction 2: Nếu bỏ positional encoding, Transformer có còn biết thứ tự token không?**
* **Prediction:** Không.
* **Reason:** Cơ chế Self-Attention bản chất là "hoán vị bất biến", tức là nó xử lý tập hợp các token như một túi từ và chỉ tính điểm tương đồng giữa các ma trận $Q, K, V$. Nếu không có Positional Encoding để gán thông tin vị trí, mô hình hoàn toàn mất khả năng nhận biết token nào đứng trước, token nào đứng sau.
* **Confidence:** 95%

---

**Prediction 3: Nếu hai câu có cùng tập token nhưng khác thứ tự, Transformer không có positional information có thể phân biệt chúng không?**
* **Prediction:** Không.
* **Reason:** Tương tự như Prediction 2, khi không có vị trí, đầu ra biểu diễn vector và điểm attention của hai câu chứa các từ giống hệt nhau (ví dụ: "Mèo đuổi chuột" và "Chuột đuổi mèo") sẽ hoàn toàn như nhau.
* **Confidence:** 95%

---

**Prediction 4: Hai attention heads có nhất thiết học cùng một attention pattern không?**
* **Prediction:** Không.
* **Reason:** Mỗi attention head được khởi tạo trọng số ngẫu nhiên khác nhau và chiếu dữ liệu sang các không gian con biểu diễn khác nhau . Mục đích của Multi-Head Attention là cho phép mô hình học đồng thời các dạng mối quan hệ đa dạng (ví dụ: một head học quan hệ ngữ pháp, một head học quan hệ khoảng cách xa).
* **Confidence:** 90%

---

**Prediction 5: Tăng số attention heads có chắc chắn làm accuracy tăng không?**
* **Prediction:** Không.
* **Reason:** Tăng số head chia nhỏ kích thước vector của từng head ($d_{k} = d_{model} / h$). Nếu chia quá nhiều head, kích thước mỗi head trở nên quá nhỏ dẫn đến giảm khả năng biểu diễn. Ngoài ra, nó có thể làm tăng nguy cơ quá khớp (overfitting) hoặc xuất hiện các head bị thừa (redundant heads).
* **Confidence:** 90%

---

**Prediction 6: Transformer có luôn nhanh hơn RNN trên mọi sequence length không?**
* **Prediction:** Không.
* **Reason:** Độ phức tạp tính toán của Self-Attention chuẩn là $\mathcal{O}(N^2)$ với $N$ là độ dài chuỗi, trong khi RNN là $\mathcal{O}(N)$. Với chuỗi cực kỳ dài ($N$ lớn), chi phí bộ nhớ và tính toán $\mathcal{O}(N^2)$ của Transformer sẽ vượt xa RNN và có thể chậm hơn hoặc gây tràn bộ nhớ (OOM).
* **Confidence:** 85%