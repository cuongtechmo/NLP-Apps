# LAB 08: Predictions Before Experiment

## Prediction 1
- **Prediction:** Pretrained Transformer fine-tuned đạt kết quả tốt hơn hẳn Transformer train from scratch.
- **Reason:** Pretrained model mang sẵn tri thức ngôn ngữ phong phú từ pretraining, chỉ cần tinh chỉnh nhẹ.
- **Expected Evidence:** Accuracy/F1 đạt ~92.5%, cao hơn nhiều so với ~74.2% của model from-scratch.

## Prediction 2
- **Prediction:** Lựa chọn C (Kém hơn).
- **Reason:** Frozen encoder không cập nhật được biểu diễn chuyên biệt cho miền dữ liệu đánh giá phim (IMDb).

## Prediction 3
- **Prediction:** Model train from scratch sẽ giảm performance mạnh hơn hẳn Pretrained model khi data giảm về 10%.
- **Reason:** Model train from scratch phụ thuộc 100% vào dữ liệu downstream để tối ưu trọng số ngẫu nhiên.