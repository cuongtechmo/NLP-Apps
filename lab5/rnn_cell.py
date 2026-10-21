import torch
import torch.nn as nn


class SimpleRNNCell(nn.Module):
    def __init__(self, input_size, hidden_size):
        super().__init__()
        self.input_size = input_size
        self.hidden_size = hidden_size

        # Khởi tạo trọng số W_xh, W_hh và bias b_h
        # W_xh có kích thước (hidden_size, input_size)
        # W_hh có kích thước (hidden_size, hidden_size)
        # b_h  có kích thước (hidden_size,)
        self.W_xh = nn.Parameter(torch.randn(hidden_size, input_size) * 0.1)
        self.W_hh = nn.Parameter(torch.randn(hidden_size, hidden_size) * 0.1)
        self.b_h = nn.Parameter(torch.zeros(hidden_size))

    def forward(self, x_t, h_prev):
        # Công thức: h_t = tanh(x_t @ W_xh^T + h_prev @ W_hh^T + b_h)
        linear_x = torch.matmul(x_t, self.W_xh.T)
        linear_h = torch.matmul(h_prev, self.W_hh.T)

        h_t = torch.tanh(linear_x + linear_h + self.b_h)
        return h_t

# 1. Định nghĩa tham số kích thước
batch_size = 2
input_size = 4
hidden_size = 3

# 2. Tạo input giả lập
x_t = torch.randn(batch_size, input_size)
h_prev = torch.randn(batch_size, hidden_size)

# 3. Khởi tạo SimpleRNNCell tự cài đặt và PyTorch RNNCell
custom_cell = SimpleRNNCell(input_size, hidden_size)
official_cell = nn.RNNCell(input_size, hidden_size, nonlinearity='tanh')
with torch.no_grad():
    custom_cell.W_xh.copy_(official_cell.weight_ih)
    custom_cell.W_hh.copy_(official_cell.weight_hh)
    custom_cell.b_h.copy_(official_cell.bias_ih + official_cell.bias_hh)

# 5. Chạy forward pass
h_custom = custom_cell(x_t, h_prev)
h_official = official_cell(x_t, h_prev)

# 6. In kết quả kiểm tra
print("--- Kết quả từ SimpleRNNCell (Tự cài đặt) ---")
print(h_custom)

print("\n--- Kết quả từ torch.nn.RNNCell (Khung thư viện) ---")
print(h_official)

# Tính độ lệch tuyệt đối tối đa giữa 2 kết quả
max_diff = torch.max(torch.abs(h_custom - h_official)).item()
print(f"\nĐộ lệch lớn nhất (Max Absolute Difference): {max_diff:.8f}")

if max_diff < 1e-6:
    print("=> XÁC NHẬN: Cài đặt chính xác hoàn toàn so với PyTorch!")
else:
    print("=> CẢNH BÁO: Kết quả có sự sai lệch.")