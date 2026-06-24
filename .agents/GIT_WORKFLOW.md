# Hướng Dẫn Sử Dụng Git Dành Cho Member 4

Tài liệu này lưu trữ các câu lệnh Git cơ bản và chuẩn mực nhất để bạn (Member 4) quản lý mã nguồn mà không làm hỏng code của nhóm.

## 1. Lần đầu tiên (Khởi tạo và Liên kết với GitHub)
*Chỉ chạy 1 lần duy nhất khi thư mục code chưa có Git.*

```bash
# 1. Biến thư mục hiện tại thành kho chứa Git
git init

# 2. Liên kết kho này với GitHub của bạn (Nhớ thay link URL bằng link thật của kho DDM501)
git remote add origin https://github.com/Ten-Cua-Ban/Ten-Kho-Github.git
```

## 2. Quy trình Code Hàng Ngày (Workflow Chuẩn)
Mỗi khi bạn code xong một chức năng (ví dụ: làm xong UI, làm xong Test), bạn bắt buộc phải làm theo 4 bước sau để lưu trữ và đẩy lên nhánh riêng của mình:

```bash
# BƯỚC 1: Gói ghém toàn bộ các file vừa thay đổi
git add .

# BƯỚC 2: Dán nhãn (Ghi chú) cho gói hàng này
# Hãy ghi rõ bạn vừa làm gì để sau này dễ tìm lại
git commit -m "feat: Member 4 hoan thanh Streamlit UI, QA Pytest va MLOps Grafana"

# BƯỚC 3: Tạo nhánh (Branch) riêng mang tên bạn và chuyển sang đó
# Tham số -b giúp tạo nhánh mới. Tên nhánh viết liền không dấu.
git checkout -b member4-frontend

# BƯỚC 4: Đẩy nhánh vừa tạo lên kho GitHub
git push -u origin member4-frontend
```

## 3. Các lần Code tiếp theo (Rất Nhàn)
Hôm sau, khi bạn mở máy lên code thêm chức năng mới, nhánh `member4-frontend` của bạn đã có sẵn trên GitHub rồi. Quy trình chỉ còn lại 3 lệnh cực ngắn:

```bash
# Thêm file mới
git add .

# Ghi chú công việc hôm nay
git commit -m "fix: sua lai mau sac giao dien Streamlit"

# Đẩy thẳng lên (Không cần lệnh dài như Bước 4 nữa)
git push
```

> **Lưu ý Quan Trọng:** Luôn luôn nhớ chạy `git push` trước khi tắt máy tính để đảm bảo code của bạn đã được sao lưu an toàn trên máy chủ của GitHub nhé!
