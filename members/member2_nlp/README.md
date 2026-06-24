# Member 2 Workspace: NLP & Multimodal RAG Pipeline

Thư mục này dành riêng cho **Member 2** để lưu trữ các mã nguồn nghiên cứu, trích xuất dữ liệu đa phương thức từ PDF và cấu hình luồng hỏi đáp RAG.

## Các công việc phụ trách:
1. Trích xuất văn bản (Text Chunks) từ PDF sổ tay xe.
2. Trích xuất sơ đồ/hình ảnh từ PDF và tự động gọi VLM cục bộ để tạo mô tả ảnh (captioning).
3. Đẩy văn bản và mô tả ảnh vào Vector Database (ChromaDB/FAISS).
4. Thiết lập Ollama chạy VLM cục bộ (Llama-3.2-Vision/Llava) và tinh chỉnh prompt hỏi đáp.
5. Tích hợp Google Cloud Speech-to-Text API để xử lý voice query.

## Cấu trúc đề xuất trong thư mục:
* `/notebooks/`: File Jupyter Notebook test trích xuất PDF và tương tác với ChromaDB/Ollama.
* `/pdf_parser/`: Các script trích xuất PDF và lưu trữ ảnh sơ đồ tạm thời.
* `/prompts/`: Lưu trữ các file prompt system/user template cho VLM.
* `/google_stt/`: Script test gọi API Google Speech-to-Text.
