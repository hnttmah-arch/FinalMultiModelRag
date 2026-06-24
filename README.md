# Dự án Multimodal RAG - DDM501

Hệ thống Trợ lý ảo đa phương thức hỗ trợ nhận dạng xe qua hình ảnh và tra cứu Hướng dẫn sử dụng bằng ngôn ngữ tự nhiên (Văn bản/Giọng nói) dựa trên công nghệ Multimodal RAG phân tán.

## Cấu trúc Thư mục Dự án

```
d:/FinalMultiModalRag/
├── README.md                     # Tài liệu giới thiệu tổng quan dự án
├── plan.md                       # Kế hoạch triển khai chi tiết cho từng thành viên
├── docker-compose.node1.yml       # Cấu hình container chạy trên Node 1 (Proxmox Server)
├── docker-compose.node2.yml       # Cấu hình container chạy trên Node 2 (Windows GPU PC)
│
├── services/                     # Mã nguồn chính của các dịch vụ hệ thống
│   ├── frontend/                 # Giao diện người dùng Streamlit (Member 4)
│   ├── gateway/                  # FastAPI API Gateway (Member 3)
│   ├── cv_service/               # Dịch vụ nhận diện dòng xe PyTorch (Member 1)
│   └── rag_service/              # Dịch vụ quản lý Vector Database & Ingestion (Member 2)
│
└── members/                      # Không gian làm việc, thử nghiệm độc lập của các thành viên
    ├── member1_cv/               # Nghiên cứu CV, Training script, Explainability (LIME/SHAP)
    ├── member2_nlp/              # Nghiên cứu NLP, Parser PDF, Embedding, Prompt RAG
    ├── member3_devops/           # Script DevOps, Cấu hình CI/CD GitHub Actions, Docker configs
    └── member4_frontend/         # Thử nghiệm UI Streamlit, QA Pytest, Prometheus/Grafana configs
```

## Các Node Triển khai

* **Node 1 (Application Server - IP Tĩnh)**: Chạy Frontend UI, API Gateway, Vector DB (ChromaDB/FAISS), Prometheus & Grafana.
* **Node 2 (AI Inference Worker - IP Tĩnh)**: Chạy CV Service và Ollama VLM (Llama-3.2-Vision/Llava).
