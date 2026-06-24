# Member 1 Workspace: Computer Vision & Responsible AI

Thư mục này dành riêng cho **Member 1** để nghiên cứu, thực hiện các thí nghiệm huấn luyện mô hình và lưu trữ các script phục vụ cho cấu phần Computer Vision & Giải thích mô hình.

## Các công việc phụ trách:
1. Huấn luyện mô hình phân loại ảnh xe (EfficientNet/ResNet).
2. Tích hợp MLflow để theo dõi tham số & log checkpoint mô hình.
3. Sử dụng LIME/Grad-CAM để phân tích tính giải thích được (Explainability).
4. Phân tích tính công bằng (Fairness) của mô hình phân loại.

## Cấu trúc đề xuất trong thư mục:
* `/notebooks/`: Chứa file Jupyter Notebook thử nghiệm huấn luyện và chạy LIME/SHAP.
* `/scripts/`: Chứa script Python huấn luyện chính (`train.py`, `eval.py`).
* `/models/`: Lưu trữ file mô hình đã train cục bộ (file `.pth` hoặc `.h5`).
* `/explainability/`: Kết quả chạy LIME/Grad-CAM (hình ảnh heatmap).
