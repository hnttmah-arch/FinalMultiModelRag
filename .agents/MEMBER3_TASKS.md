# BẢNG HƯỚNG DẪN DÀNH CHO MEMBER 3 (BACKEND & DEVOPS LEAD)

Chào Member 3,
Nhóm đã khởi chạy thành công toàn bộ kiến trúc (Frontend UI, QA, MLOps Monitor) trên **Node 1**. Chức năng "vỏ bọc" của API Gateway cũng đã được hoàn thiện để UI có thể ghép nối.

Bây giờ là lúc bạn thể hiện sức mạnh của một DevOps & Backend Lead. Đây là **Lộ trình công việc (Roadmap)** để bạn làm mượt mà nhất mà không dẫm chân lên code của bất kỳ ai:

---

## 🚀 Giai đoạn 1: Lấy Code và Hiểu Hệ Thống Hiện Tại
1. **Lấy code mới nhất:** Hãy clone nhánh (branch) mới nhất trên GitHub về. Cấu trúc hiện tại có 4 container chạy đồng thời: `ui`, `gateway`, `prometheus`, `grafana`.
2. **Khởi chạy thử:** Mở Terminal ở thư mục dự án và chạy `docker-compose up -d`. Vào `localhost:8000/docs` (Swagger API) và `localhost:8501` (Giao diện) để xem mọi thứ hoạt động thế nào.
3. **Đọc "Bộ luật":** Đọc kỹ file **`docs/05_MEMBER3_BACKEND_CONTRACT.md`**. File này quy định rõ các luật cấm xóa code (như đoạn `prometheus_fastapi_instrumentator` ở file `gateway/main.py`) để bảo vệ hệ thống giám sát.

---

## 🚀 Giai đoạn 2: Xây dựng Backend Thực Sự (Tại Node 1)
Nhiệm vụ của bạn là đập bỏ đoạn logic Giả lập (Mock) trong file `app/gateway/main.py` và thay bằng logic thật.
1. **Kết nối Vector Database (ChromaDB):**
   - Viết code kết nối vào ChromaDB/FAISS.
   - Khi API nhận được `query` từ UI, bạn dùng ChromaDB để truy xuất các đoạn văn bản (context) liên quan nhất.
2. **Gọi API sang Node 2 (Inference Worker):**
   - Đóng gói (Ảnh + Câu hỏi + Ngữ cảnh từ ChromaDB) thành một request HTTP.
   - Gửi sang địa chỉ IP tĩnh của **Node 2** (máy PC chạy RTX 5080).
3. **Trả dữ liệu về cho UI:**
   - Hứng kết quả từ Node 2.
   - Đóng gói thành định dạng JSON chuẩn (có `status`, `car_model`, `confidence`, `rag_answer`) như đã thoả thuận trong file Contract và `return` về cho UI.

---

## 🚀 Giai đoạn 3: Triển khai Node 2 (Máy chủ AI)
Vì bạn là DevOps Lead, bạn phải lo cả việc làm sao để Node 2 chạy lên được.
1. Tạo một file `docker-compose.node2.yml` hoàn toàn mới (hoặc thư mục riêng) dành cho Node 2.
2. Trong đó chứa các dịch vụ: 
   - Ollama (LLM) để sinh chữ.
   - Container chạy API nhận diện ảnh (ResNet/EfficientNet).
3. Cấu hình để Container trên Node 2 có quyền truy cập vào Card đồ hoạ NVIDIA RTX 5080 (`deploy.resources.reservations.devices`).

---

## 🚀 Giai đoạn 4: Thiết lập CI/CD (GitHub Actions)
Sau khi Code chạy ổn định, bước cuối cùng là tự động hóa:
1. Tạo thư mục `.github/workflows/`.
2. Viết file `ci.yml` để mỗi khi có ai Push code lên nhánh `main`:
   - GitHub sẽ tự động chạy lệnh cài thư viện (`pip install -r requirements.txt`).
   - GitHub tự động chạy bộ test của Member 4 bằng lệnh `python -m pytest app/tests/ -v`.
   - Nếu Test báo xanh (PASSED), mới cho phép gộp code (Merge).

---
**💡 Chốt lại:** Việc khó nhất là định hình cấu trúc Microservices thì Member 4 đã dựng khung (Framework) giúp bạn rồi. Bạn chỉ cần tập trung não bộ vào việc **truy vấn VectorDB, bắn API qua Node 2 và viết CI/CD** là chúng ta sẽ có một Project điểm A+! Chúc bạn làm việc hiệu quả!
