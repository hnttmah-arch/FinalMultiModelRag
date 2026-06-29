# Dự án DDM501 - AutoDiag AI (Thông tin Context dành cho Agent)

File này chứa toàn bộ bối cảnh dự án để AI Agent tự động đọc hiểu khi bắt đầu một phiên làm việc mới, giúp tiết kiệm Token và thời gian cho User mà không cần đọc lại code.

## 1. Vai trò của Agent & User
- **User:** Là Member 4 (Phụ trách Frontend Streamlit, Viết Pytest QA & Triển khai MLOps Grafana/Prometheus).
- **Agent:** AI Coding Assistant cấp cao. Hỗ trợ Member 4 hoàn thiện, gỡ lỗi và nâng cấp tính năng.
- **Quy tắc làm việc:** Tuân thủ Zero-Yapping (chỉ xuất code khi cần, không giải thích dài dòng), code modular, chuyên nghiệp.

## 2. Tổng quan Kiến trúc Hệ thống (Đã tách Microservices)
Dự án được chia thành 4 thành phần chạy song song bằng `docker-compose` (Tất cả đã hoàn thiện):

- **1. Streamlit UI (Port 8501):** Code nằm ở `app/ui/main.py`. Nhiệm vụ nhận ảnh (giới hạn <5MB), text, voice. Gửi Request (`app/ui/api_client.py`) sang Gateway bằng thư viện `requests`. Giao diện đã được thiết kế Commercial Dark/Light mode cao cấp.
- **2. Mock FastAPI Gateway (Port 8000):** Code nằm ở `app/gateway/main.py`. Đóng vai trò làm "Kẻ đóng thế" cho Node 2. Tự động trả về JSON Mock (có mô phỏng độ trễ 2s hoặc lỗi 504 Timeout) để UI hiển thị. Đã tích hợp `prometheus-fastapi-instrumentator` tại `/metrics`.
- **3. QA Pytest:** Nằm ở `app/tests/`. Có 2 phần: Unit Test (`test_validation.py`) để test logic chặn ảnh >5MB, và Integration Test (`test_integration.py`) dùng `TestClient` để test kết nối đến API Gateway. Toàn bộ test hiện tại đang PASSED 100%.
- **4. MLOps (Prometheus Port 9090 & Grafana Port 3000):** Đã cấu hình Auto-provisioning trong `grafana/provisioning/`. Chỉ cần bật Docker, Grafana sẽ tự động nạp Dashboard "DDM501 - AutoDiag AI Monitoring" đo Latency và Error Rate.

## 3. Các thiết lập Kỹ thuật quan trọng (Cần nhớ để fix lỗi)
- Trong `docker-compose.yml`, thư mục gốc của Host (`.`) được mount vào container dưới dạng `.:/app`.
- Biến môi trường `PYTHONPATH=/app` được sử dụng để tránh lỗi `ModuleNotFoundError`, do đó code Python import dùng cấu trúc tuyệt đối như: `from app.ui.api_client import process_request`.

## 4. Lệnh vận hành Hệ thống (Runbook - AI HÃY NHẮC USER CHẠY LỆNH NÀY KHI MỞ PROJECT)
Khi User vừa mở project (mở VSCode), AI hãy hướng dẫn User mở Terminal (Ctrl + ~) và chạy các lệnh sau:

**1. Khởi động toàn bộ hệ thống (Bắt buộc chạy đầu tiên):**
```bash
docker-compose up -d
```
Sau khi chạy xong, hãy truy cập:
- Giao diện làm việc chính: `http://localhost:8501`
- Màn hình MLOps (Grafana): `http://localhost:3000` (User/Pass: admin/admin -> Vào mục Dashboards)
- Backend API Docs: `http://localhost:8000/docs`

**2. Chạy kiểm thử tự động (Khi cần test lỗi):**
```bash
venv\Scripts\activate
python -m pytest app/tests/ -v
```

**3. Tắt hệ thống khi làm xong:**
```bash
docker-compose down
```

## 5. Tình trạng hiện tại (State)
- Giao diện UI đã xong. 
- Tính năng chặn lỗi Validation đã xong. 
- Bài test QA đã passed 100%. 
- Grafana Auto-provisioning đã xong.
- Lỗi ModuleNotFoundError đã được fix bằng PYTHONPATH.
