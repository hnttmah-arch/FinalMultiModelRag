# TÀI LIỆU BÀN GIAO BACKEND (API CONTRACT) - DÀNH CHO MEMBER 3

Chào Member 3 (Backend & DevOps Lead),

Member 4 đã hoàn thành việc thiết lập **Giao diện (Frontend Streamlit)**, hệ thống **Kiểm thử tự động (Pytest)** và hệ thống **Giám sát MLOps (Grafana/Prometheus)** trên Node 1. 

Để bạn (Member 3) có thể dễ dàng code và ghép nối hệ thống mà không làm hỏng các phần UI/MLOps đã chạy ổn định, vui lòng đọc kỹ các quy ước "Bất di bất dịch" dưới đây.

---

## 1. Nơi bạn sẽ code (Vị trí file)
Bạn sẽ viết code chính của API Gateway tại file: **`app/gateway/main.py`**.
Hiện tại, file này đang chứa code **GIẢ LẬP (Mock)** do Member 4 viết tạm để test UI. Khi bạn làm xong logic kết nối VectorDB (Node 1) và gọi AI Inference (Node 2), bạn hãy **XÓA BỎ logic giả lập** và viết code thật của bạn đè lên.

---

## 2. Quy tắc Sinh tử (DO NOT TOUCH) ⚠️
Để hệ thống Giám sát hiệu năng (Grafana) của Member 4 hoạt động được, bạn **BẮT BUỘC PHẢI GIỮ LẠI** các dòng code cấu hình Prometheus sau trong `app/gateway/main.py`:

```python
# 1. BẮT BUỘC PHẢI CÓ dòng import này
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(title="DDM501 API Gateway")

# 2. BẮT BUỘC PHẢI CÓ dòng này ngay dưới khai báo app
Instrumentator().instrument(app).expose(app)
```
*(Nếu bạn xóa đoạn code trên, hệ thống MLOps sẽ mù tịt, không đo lường được Latency và Error Rate).*

---

## 3. Giao thức Kết nối (API Contract)
Giao diện Streamlit của Member 4 hiện tại đang gửi dữ liệu cố định theo định dạng sau. Bạn phải viết endpoint FastAPI hứng đúng định dạng này:

### A. Endpoint
- **URL:** `POST /api/v1/inference`
- **Content-Type:** `multipart/form-data`

### B. Input (Dữ liệu gửi lên từ UI)
Các trường (fields) bắt buộc phải cấu hình `Optional` ở FastAPI (vì logic bắt lỗi ném HTTP 400 đã được Streamlit và Gateway Mock xử lý tay để test):
- `image`: `UploadFile` (Ảnh táp-lô người dùng chụp).
- `query`: `str` (Câu hỏi dạng chữ).
- `audio`: `UploadFile` (Câu hỏi bằng giọng nói, nếu có).

### C. Output (Dữ liệu bạn phải trả về cho UI)
Sau khi Node 2 xử lý xong, bạn đóng gói và trả về cho UI một file JSON có cấu trúc **chính xác** như sau:

```json
{
  "status": "success",
  "message": "Xử lý thành công",
  "data": {
    "car_model": "Kia Seltos 2024",     // Kết quả từ Computer Vision Model
    "confidence": 0.98,                 // Độ tin cậy (Float)
    "rag_answer": "Để bật đèn sương mù, bạn hãy..." // Câu trả lời sinh ra từ LLM
  }
}
```
*(Lưu ý: Nếu có lỗi kết nối Node 2 hoặc lỗi nội bộ, hãy trả về HTTP Status Code `500` hoặc `504` để UI của Member 4 tự động bắt lỗi và hiện cảnh báo đỏ cho người dùng).*

---

## 4. Cách chạy thử (Dành cho Member 3)
Sau khi bạn code xong logic thật, bạn mở Terminal và chạy:
```bash
docker-compose up --build -d
```
Sau đó truy cập `http://localhost:8000/docs` để kiểm tra Swagger API của bạn, và vào `http://localhost:8501` để xem giao diện Streamlit có nhận đúng dữ liệu bạn trả về hay không.

Chúc bạn code mượt và ghép nối thành công!
