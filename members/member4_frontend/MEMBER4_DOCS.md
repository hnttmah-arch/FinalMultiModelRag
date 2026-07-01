# Tài liệu Tổng quan Dành cho Member 4 (Frontend, QA & MLOps)

Tài liệu này tổng hợp toàn bộ tri thức, cấu trúc thư mục, chức năng của các file và hướng dẫn vận hành cục bộ các module thuộc trách nhiệm của **Member 4**. Việc này giúp tiết kiệm thời gian khi xem lại code và bàn giao dự án.

## 1. Vai trò của Member 4
- **Frontend (UI):** Xây dựng giao diện tương tác chính cho người dùng bằng **Streamlit**. Giao diện cho phép upload ảnh (giới hạn <5MB), nhập text/voice và hiển thị kết quả từ hệ thống AI (RAG).
- **QA (Quality Assurance):** Viết các kịch bản kiểm thử tự động bằng **Pytest** để đảm bảo tính đúng đắn của logic (Unit Test) và tính ổn định của luồng kết nối API (Integration Test).
- **MLOps (Monitoring):** Triển khai hệ thống giám sát (Monitoring) bằng **Prometheus** và vẽ biểu đồ hiệu năng trên **Grafana**. 

---

## 2. Cấu trúc thư mục & Ý nghĩa từng file

Thư mục `members/member4_frontend/` chứa các thành phần sau:

### 📁 `ui_dev/` (Giao diện Streamlit)
Nơi chứa toàn bộ mã nguồn của Frontend.
- **`main.py`**: Điểm neo chính (Entry point) của ứng dụng Streamlit. Xử lý giao diện người dùng (UI), hiển thị Dark/Light theme, các nút bấm upload ảnh, khung chat và gọi tới logic của Client.
- **`api_client.py`**: Chứa logic đóng gói Request (Ảnh, Text, Voice) và gửi tới API Gateway (FastAPI) thông qua thư viện `requests`. File này hoạt động độc lập để tách biệt logic xử lý data và giao diện.

### 📁 `tests/` (Kiểm thử Pytest)
Nơi chứa các kịch bản kiểm thử tự động, hiện tại đã Pass 100%.
- **`test_validation.py`** (Unit Test): Kiểm tra các ràng buộc độc lập. Ví dụ: Chặn người dùng nếu upload ảnh có kích thước vượt quá 5MB.
- **`test_api_client.py`** (Unit Test): Mock (giả lập) các API gọi đến Gateway để kiểm tra xem UI có xử lý đúng phản hồi (Response JSON) từ backend không.
- **`test_integration.py`** (Integration Test): Sử dụng thư viện `TestClient` để tạo luồng test tích hợp, đảm bảo từ UI gọi qua Gateway hoạt động liền mạch mà không bị lỗi.

### 📁 `monitoring_configs/` (Cấu hình MLOps)
Nơi chứa các cấu hình cho hệ thống Monitoring, được gọi vào bởi Docker Compose.
- **`prometheus.yml`**: Tệp cấu hình gốc của Prometheus, chỉ định mục tiêu cào dữ liệu (scrape target) là API Gateway (Port 8000/metrics) sau mỗi 5 giây.
- **`grafana_provisioning/`**: Cấu hình tự động nạp (Auto-provisioning) cho Grafana.
  - `dashboards/`: Chứa file JSON giao diện bảng điều khiển (Dashboard) đo Latency và Error Rate. Khi Grafana bật lên, Dashboard sẽ tự động hiển thị mà không cần setup tay.
  - `datasources/`: Chứa cấu hình khai báo Prometheus là Data Source mặc định cho Grafana.

---

## 3. Hướng dẫn chạy các ứng dụng (Runbook cho Member 4)

### Cách 1: Chạy toàn bộ hệ thống bằng Docker Compose (Khuyên dùng)
Vì dự án được cấu trúc theo Microservices, cách tốt nhất là khởi động tất cả cùng lúc từ thư mục gốc của dự án (`FinalMultiModelRag`).
1. Mở Terminal (VSCode).
2. Chạy lệnh:
   ```bash
   docker-compose up -d
   ```
3. Truy cập các dịch vụ:
   - **Giao diện Streamlit:** `http://localhost:8501`
   - **Dashboard Grafana:** `http://localhost:3000` (User/Pass: admin/admin)
   - **Backend API Docs:** `http://localhost:8000/docs`

### Cách 2: Chạy kiểm thử tự động (QA Pytest)
Khi bạn sửa code UI hoặc logic và muốn test lại xem có bị lỗi gì không:
1. Mở Terminal và kích hoạt môi trường ảo (nếu có): `venv\Scripts\activate`
2. Đứng ở thư mục gốc của project (hoặc trỏ đường dẫn tới file test), chạy lệnh:
   ```bash
   python -m pytest members/member4_frontend/tests/ -v
   ```
*(Lưu ý: Nếu bị lỗi `ModuleNotFoundError`, hãy set biến môi trường: `set PYTHONPATH=.` trước khi chạy pytest)*.

### Cách 3: Chạy độc lập Streamlit UI (Dev Mode)
Nếu bạn chỉ muốn thiết kế, chỉnh sửa giao diện mà không muốn khởi động qua Docker để có thể xem thay đổi ngay lập tức (Hot-reload):
1. Đảm bảo đã cài đủ thư viện: `pip install -r requirements.txt`
2. Chạy lệnh (từ thư mục gốc):
   ```bash
   python -m streamlit run members/member4_frontend/ui_dev/main.py
   ```
*(Streamlit sẽ tự động mở tab mới trên trình duyệt)*.
