# Giải Thích Cấu Trúc & Nhiệm Vụ Code 

Tài liệu này giải thích chi tiết chức năng của từng thư mục và file code để Member 4 dễ dàng nắm bắt, bảo trì và báo cáo đồ án.

## 1. Cấu trúc Thư mục Hệ thống
Hệ thống được chia thành 4 mảng rõ rệt:
```text
DDM501_Frontend/
├── app/
│   ├── gateway/         (Mảng Backend API Mock)
│   ├── ui/              (Mảng Frontend Streamlit)
│   └── tests/           (Mảng QA & Kiểm thử)
├── grafana/             (Mảng MLOps Provisioning)
├── prometheus/          (Mảng MLOps Metrics)
├── Dockerfile.gateway   (Script đóng gói Backend)
├── Dockerfile.ui        (Script đóng gói Frontend)
└── docker-compose.yml   (Script kết nối 4 mảng trên)
```

## 2. Chi tiết Chức năng từng File Code

### A. Mảng Frontend (Thư mục `app/ui/`)
- **`app/ui/main.py`**: Là trái tim của giao diện.
  - Chứa toàn bộ HTML/CSS được nhúng qua `st.markdown` để tạo giao diện AutoDiag AI cao cấp.
  - **Logic Validation:** Hàm `validate_inputs` kiểm tra bắt buộc người dùng tải ảnh (dung lượng dưới 5MB) và có nhập chữ/giọng nói trước khi cho phép gọi API.
  - **Error Handling:** Đọc mã lỗi trả về (VD: `504 Timeout`, `500 Server Error`) để in ra cảnh báo màu đỏ thân thiện thay vì làm sập (crash) toàn bộ màn hình.

- **`app/ui/api_client.py`**: Là "Cầu nối giao tiếp".
  - Sử dụng thư viện `requests` gửi dữ liệu đa phương thức (`multipart/form-data`) sang FastAPI.
  - Cài đặt thời gian chờ tối đa (`timeout=10`) để đề phòng Node 2 bị treo, từ đó chủ động ném lỗi `504` về cho `main.py` xử lý.

### B. Mảng Mock Backend (Thư mục `app/gateway/`)
- **`app/gateway/main.py`**: 
  - Khởi tạo FastAPI Server (`@app.post("/api/v1/inference")`).
  - Đóng vai trò là "Kẻ thế thân" (Mock) cho Member 2 và Member 3. Nó tự động tạo ra một câu trả lời JSON ảo sau một khoảng thời gian `time.sleep()` ngẫu nhiên để giả lập quá trình GPU Inference.
  - **Tích hợp MLOps:** Import `Instrumentator()` để FastAPI tự động phơi bày `/metrics` cho Prometheus vào lấy số liệu quét (Scrape).

### C. Mảng QA & Kiểm thử (Thư mục `app/tests/`)
- **`app/tests/test_validation.py` (Unit Test):**
  - Chứa các hàm test độc lập để gọi hàm `validate_inputs()` trong Streamlit. Kiểm chứng xem logic chặn file 5MB và chặn form rỗng có hoạt động chính xác không.
- **`app/tests/test_integration.py` (Integration Test):**
  - Dùng `fastapi.testclient` để bắn các request HTTP giả lập thẳng vào Mock API Gateway. Xác nhận Gateway phản hồi đúng mã `400` khi thiếu ảnh và `200` / `504` khi chạy bình thường.

### D. Mảng MLOps (Prometheus & Grafana)
- **`docker-compose.yml`**: Trái tim của hệ thống vận hành. Chứa 4 container: `gateway`, `ui`, `prometheus`, `grafana`. Các container này tự động nhận diện nhau qua mạng ảo nội bộ của Docker.
- **`grafana/provisioning/`**: 
  - Thay vì tự config UI, các file YAML và JSON trong này cung cấp sẵn các biểu đồ giám sát (Latency, Error rate). Docker sẽ đẩy thẳng thư mục này vào trong ruột của Grafana, giúp biểu đồ hiển thị ngay lần chạy đầu tiên.
