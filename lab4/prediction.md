## Prediction 1: TF-IDF + Logistic Regression
* **Prediction:** Đúng (Có khả năng hoạt động tốt)
* **Reason:** TF-IDF kết hợp Logistic Regression là một baseline rất mạnh, phổ biến và hiệu quả trong phân loại văn bản (như phân loại chủ đề, phân loại thư rác, phân tích cảm xúc đơn giản). Mô hình này huấn luyện nhanh, ít tốn tài nguyên và ít bị overfit trên tập dữ liệu kích thước vừa và nhỏ.
* **Confidence:** Cao (95%)

---

## Prediction 2: Average Word2Vec vs TF-IDF
* **Prediction:** Sai (Không chắc chắn tốt hơn)
* **Reason:** Việc tính trung bình các vector từ (Average Word2Vec) làm trung hòa và mất đi thông tin của các từ khóa quan trọng trong câu. Trong khi đó, TF-IDF gán trọng số cao cho các từ mang tính phân biệt tốt. Với nhiều bài toán phân loại dựa trên từ khóa, TF-IDF cho hiệu năng tương đương hoặc tốt hơn Average Word2Vec.
* **Confidence:** Cao (95%)

---

## Prediction 3: Vocabulary Size vs Accuracy
* **Prediction:** Sai (Accuracy không chắc chắn tăng)
* **Reason:** Tăng vocabulary size sẽ đưa thêm nhiều từ hiếm, từ gõ sai hoặc nhiễu vào mô hình. Điều này gia tăng số lượng chiều (curse of dimensionality), khiến mô hình dễ bị quá khớp (overfitting) và làm giảm accuracy trên tập kiểm thử (test set).
* **Confidence:** Cao (95%)

---

## Prediction 4: Stopwords vs Performance
* **Prediction:** Sai (Performance không chắc chắn tăng)
* **Reason:** Bỏ stopwords có thể làm mất ngữ cảnh quan trọng hoặc thành phần phủ định. Trong các bài toán phân tích cảm xúc hoặc mô hình cần giữ cấu trúc ngữ pháp câu, loại bỏ stopwords có thể làm giảm performance của mô hình.
* **Confidence:** Cao (90%)

---

## Prediction 5: Accuracy vs F1-score
* **Prediction:** Đúng (Hoàn toàn có thể cho kết luận khác nhau)
* **Reason:** Khi tập dữ liệu bị mất cân bằng lớp (imbalanced dataset), Accuracy có thể đạt rất cao chỉ bằng cách đoán toàn bộ dữ liệu thuộc lớp đa số. Ngược lại, F1-score cân bằng giữa Precision và Recall, phản ánh chính xác khả năng nhận diện lớp thiểu số. Hai chỉ số này thường đưa ra đánh giá khác biệt lớn trong trường hợp này.
* **Confidence:** Cao (100%)