# Hướng Dẫn Cài Đặt & Cơ Bản Về Docker

Tài liệu này giúp bạn (Member 4) hiểu bản chất của Docker và cách sử dụng nó trong dự án DDM501 để quản lý MLOps và FastAPI Gateway một cách dễ dàng.

## 1. Docker là gì? Tại sao phải dùng Docker?
Hãy tưởng tượng dự án của bạn cần: Python 3.9, FastAPI, Streamlit, Grafana, Prometheus.
Nếu không có Docker, bạn sẽ phải:
- Tự cài Python, tự `pip install`.
- Tự tải Grafana về máy, cài đặt bằng file `.exe`, sửa file cấu hình thủ công.
- Tự tải Prometheus, mở nhiều tab Terminal để chạy.
-> **Rất mất thời gian và dễ gặp lỗi (chạy được trên máy này nhưng lỗi trên máy khác).**

**Docker** sinh ra để giải quyết vấn đề này. Nó đóng gói toàn bộ ứng dụng (code + thư viện + cấu hình môi trường) vào một "Hộp kín" gọi là **Container**. Bạn có thể mang cái "Hộp" này sang bất kỳ máy tính nào (Windows, Mac, Linux) và chạy ngay lập tức mà không cần cài đặt lại môi trường.

**Docker Compose** là công cụ giúp chạy nhiều "Hộp" (Containers) cùng lúc. Trong dự án của chúng ta:
- Hộp 1: Streamlit UI
- Hộp 2: Mock API Gateway
- Hộp 3: Prometheus
- Hộp 4: Grafana
Chỉ cần 1 lệnh `docker-compose up`, cả 4 hộp này sẽ tự động liên kết với nhau và hoạt động đồng bộ.

## 2. Hướng dẫn cài đặt Docker trên Windows

1. **Tải Docker Desktop:** Truy cập [https://www.docker.com/products/docker-desktop/](https://www.docker.com/products/docker-desktop/) và tải bộ cài đặt cho Windows.
2. **Kích hoạt WSL 2 (Windows Subsystem for Linux):** 
   Docker Desktop trên Windows yêu cầu WSL 2 để chạy nhanh hơn. Trong quá trình cài đặt Docker, hãy đảm bảo bạn tick vào ô *"Use WSL 2 instead of Hyper-V"*.
3. **Cài đặt và Khởi động:**
   - Chạy file `.exe` vừa tải và bấm Next/Install.
   - Sau khi cài xong, máy tính có thể yêu cầu Restart.
   - Mở ứng dụng **Docker Desktop** từ Start Menu. Lần đầu mở, bạn cần Accept điều khoản sử dụng. Chờ đến khi biểu tượng con cá voi ở khay hệ thống (góc dưới bên phải màn hình) chuyển sang màu xanh lá (hoặc hiện chữ "Engine running" trên giao diện).

## 3. Các lệnh Docker thiết yếu cho Dự án DDM501

Mở Terminal tại thư mục `DDM501_Frontend` và sử dụng các lệnh sau:

- **Khởi động toàn bộ hệ thống:**
  ```bash
  docker-compose up --build -d
  ```
  *(Lệnh này sẽ xây dựng lại image từ Dockerfile và chạy ngầm (chế độ `-d`).)*

- **Kiểm tra các service đang chạy:**
  ```bash
  docker ps
  ```

- **Xem Log lỗi của một service (ví dụ xem log của FastAPI Gateway):**
  ```bash
  docker-compose logs -f gateway
  ```

- **Tắt toàn bộ hệ thống:**
  ```bash
  docker-compose down
  ```

## 4. Kiểm tra hệ thống sau khi chạy Docker
Sau khi lệnh `docker-compose up` chạy thành công, bạn có thể truy cập:
- **UI Streamlit:** `http://localhost:8501`
- **FastAPI Docs:** `http://localhost:8000/docs`
- **Grafana Dashboard:** `http://localhost:3000` (User/Pass mặc định thường là `admin` / `admin`). Đồ thị giám sát của chúng ta đã được tự động thêm vào đây.
