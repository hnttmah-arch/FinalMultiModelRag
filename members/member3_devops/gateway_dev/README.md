# Hướng dẫn Phát triển API Gateway (FastAPI)

Thư mục này dành cho việc phát triển thử nghiệm và thiết lập cấu hình cổng kết nối chính của hệ thống.

## Các chức năng chính cần hoàn thiện:
1. Tiếp nhận request từ Streamlit UI:
   - File ảnh người dùng tải lên (`image`).
   - Câu hỏi dạng text hoặc file audio (`voice`).
2. Tích hợp module chuyển giọng nói thành văn bản (Google Cloud Speech-to-Text).
3. Gửi ảnh xe sang CV Service ở Node 2 (`http://<node2-ip>:8001/predict`) để lấy tên xe và độ tin cậy.
4. Sử dụng tên xe vừa nhận diện được để làm bộ lọc metadata, sau đó truy vấn vào ChromaDB/FAISS (chạy local trên Node 1) để lấy context (đoạn text + đường dẫn sơ đồ ảnh có điểm tương đồng cao nhất).
5. Gửi toàn bộ dữ liệu (câu hỏi, ảnh xe, text context, sơ đồ ảnh) sang Ollama API trên Node 2 (`http://<node2-ip>:11434/api/generate`) chạy mô hình Llama-3.2-Vision/Llava.
6. Trả về JSON tích hợp đầy đủ thông tin cho Streamlit hiển thị.

## Custom Metrics cho Prometheus (MLOps):
```python
from prometheus_client import Counter, Histogram

# Đếm số lượng request và mã lỗi
REQUEST_COUNT = Counter('gateway_requests_total', 'Total HTTP Requests', ['method', 'endpoint', 'status_code'])

# Theo dõi thời gian xử lý toàn trình và từng service
LATENCY_TOTAL = Histogram('gateway_request_duration_seconds', 'Total request processing duration')
LATENCY_CV = Histogram('gateway_cv_latency_seconds', 'Inference latency of CV service')
LATENCY_VLM = Histogram('gateway_vlm_latency_seconds', 'Generation latency of VLM service')
```
