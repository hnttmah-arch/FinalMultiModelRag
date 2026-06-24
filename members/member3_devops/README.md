# Member 3 Workspace: Backend & DevOps

Thư mục này dành riêng cho **Member 3** để lưu trữ các file cấu hình Docker, script thiết lập CI/CD, cấu hình mạng LAN và thiết kế ban đầu của API Gateway.

## Các công việc phụ trách:
1. Thiết kế API Gateway chính bằng FastAPI.
2. Cấu hình địa chỉ IP tĩnh cho Node 2 và thiết lập Firewall rule trên Windows Defender.
3. Đóng gói Dockerfile cho tất cả các dịch vụ (Frontend, Gateway, CV, RAG).
4. Thiết lập file `docker-compose.node1.yml` và `docker-compose.node2.yml`.
5. Tạo workflow GitHub Actions tự động kiểm thử và build ảnh docker.

## Cấu trúc đề xuất trong thư mục:
* `/gateway_dev/`: File nháp hoặc các phiên bản thử nghiệm của FastAPI Gateway.
* `/docker_configs/`: Chứa các Dockerfile, cấu hình Nginx (nếu có) hoặc file phụ trợ cho Docker.
* `/cicd/`: Các file YAML định nghĩa workflow GitHub Actions (sẽ được copy vào `.github/workflows/` sau).
* `/network_setup/`: Các tài liệu hướng dẫn nhanh, script PowerShell thiết lập IP tĩnh và firewall cho Windows.
