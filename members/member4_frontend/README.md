# Member 4 Workspace: Frontend, QA & MLOps

Thư mục này dành riêng cho **Member 4** để phát triển giao diện Streamlit UI, viết các kịch bản kiểm thử Pytest và thiết lập hệ thống giám sát thời gian thực Prometheus/Grafana.

## Các công việc phụ trách:
1. Xây dựng giao diện Streamlit UI (hỗ trợ upload ảnh, voice query, chatbox và hiển thị sơ đồ ảnh minh họa).
2. Viết Unit Test và Integration Test bằng Pytest.
3. Thiết lập cấu hình Prometheus để cào metrics từ FastAPI Gateway.
4. Xây dựng Dashboard theo dõi hiệu năng hệ thống trên Grafana.

## Cấu trúc đề xuất trong thư mục:
* `/ui_dev/`: Thử nghiệm giao diện, custom CSS hoặc các widget phụ trợ.
* `/tests/`: Chứa các file test (`test_api.py`, `test_cv.py`, `test_rag.py`).
* `/monitoring_configs/`: File cấu hình `prometheus.yml` và file JSON export của Grafana Dashboard.
