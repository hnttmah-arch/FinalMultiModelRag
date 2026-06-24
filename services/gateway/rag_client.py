import os
import logging

logger = logging.getLogger("gateway.rag_client")

# Khai báo biến toàn cục cho model và client để tránh nạp lại nhiều lần
embedding_model = None
chroma_client = None

def get_embedding_model():
    """
    Khởi tạo và tải mô hình sentence-transformers để nhúng câu hỏi của người dùng.
    """
    global embedding_model
    if embedding_model is None:
        model_name = os.getenv("EMBEDDING_MODEL_NAME", "all-MiniLM-L6-v2")
        logger.info(f"Đang tải mô hình Embedding: {model_name}...")
        try:
            from sentence_transformers import SentenceTransformer
            embedding_model = SentenceTransformer(model_name)
            logger.info("Đã tải thành công mô hình Embedding.")
        except Exception as e:
            logger.error(f"❌ Không thể tải mô hình embedding: {e}")
    return embedding_model

def retrieve_context_from_db(query: str, car_model: str, top_k: int = 3):
    """
    Truy vấn ChromaDB để lấy các đoạn văn bản hướng dẫn và sơ đồ hình ảnh có liên quan nhất.
    Có cơ chế tự động chuyển sang chế độ giả lập (Mock) nếu ChromaDB chưa được khởi chạy hoặc bị lỗi.
    
    Args:
        query (str): Câu hỏi của người dùng.
        car_model (str): Tên dòng xe đã được nhận diện bởi CV Service.
        top_k (int): Số lượng kết quả văn bản liên quan nhất cần lấy.
        
    Returns:
        dict: Chứa list văn bản (text_contexts) và list đường dẫn sơ đồ (image_contexts).
    """
    chroma_host = os.getenv("CHROMA_HOST", "localhost")
    chroma_port = int(os.getenv("CHROMA_PORT", "8000"))
    
    # Kiểm tra biến cấu hình chạy thử nghiệm nhanh
    if os.getenv("MOCK_RAG", "true").lower() == "true":
        logger.info("Chế độ MOCK RAG được kích hoạt.")
        return get_mock_context(car_model)
        
    try:
        import chromadb
        
        # 1. Kết nối tới ChromaDB Server qua HTTP
        logger.info(f"Kết nối tới ChromaDB tại {chroma_host}:{chroma_port}...")
        client = chromadb.HttpClient(host=chroma_host, port=chroma_port)
        
        # 2. Lấy các collections chứa văn bản và ảnh hướng dẫn sử dụng
        # Các collection này do Member 2 (RAG Lead) ingest dữ liệu từ PDF vào trước đó.
        text_collection = client.get_collection(name="car_manual_texts")
        image_collection = client.get_collection(name="car_manual_images")
        
        # 3. Tạo vector nhúng cho câu hỏi của người dùng
        model = get_embedding_model()
        if not model:
            raise Exception("Mô hình Embedding chưa sẵn sàng.")
        query_vector = model.encode(query).tolist()
        
        # 4. Tìm kiếm ngữ cảnh văn bản (lọc theo dòng xe cụ thể)
        logger.info(f"Đang tìm kiếm văn bản liên quan cho dòng xe: {car_model}...")
        text_results = text_collection.query(
            query_embeddings=[query_vector],
            n_results=top_k,
            where={"car_model": car_model} # Metadata filter để đảm bảo tìm đúng tài liệu của dòng xe đó
        )
        
        # 5. Tìm kiếm sơ đồ hình ảnh liên quan nhất
        logger.info(f"Đang tìm kiếm sơ đồ ảnh liên quan...")
        image_results = image_collection.query(
            query_embeddings=[query_vector],
            n_results=1,
            where={"car_model": car_model}
        )
        
        # 6. Đóng gói kết quả trả về
        text_contexts = []
        if text_results and 'documents' in text_results and text_results['documents']:
            text_contexts = text_results['documents'][0]
            
        image_contexts = []
        if image_results and 'metadatas' in image_results and image_results['metadatas']:
            for meta in image_results['metadatas'][0]:
                if 'image_path' in meta:
                    image_contexts.append(meta['image_path'])
                    
        return {
            "text_contexts": text_contexts,
            "image_contexts": image_contexts
        }
        
    except Exception as e:
        logger.error(f"❌ Lỗi khi truy vấn ChromaDB: {e}. Tự động chuyển sang Mock dữ liệu.")
        return get_mock_context(car_model)

def get_mock_context(car_model: str):
    """
    Hàm sinh dữ liệu giả lập chất lượng cao phục vụ việc phát triển và test offline.
    """
    # Chuẩn hóa tên xe để tạo dữ liệu mock phù hợp
    car = car_model.lower()
    if "camry" in car:
        return {
            "text_contexts": [
                "Sổ tay Toyota Camry 2023 - Trang 120: Hộp cầu chì khoang cabin nằm ở phía dưới bảng taplo, bên trái vô lăng. Cần kéo nhẹ nắp đậy ra ngoài để kiểm tra các cầu chì bảo vệ thiết bị điện tử trong xe.",
                "Sổ tay Toyota Camry 2023 - Trang 121: Cầu chì tẩu sạc thuốc và sạc điện thoại có ký hiệu 'CIG' hoặc 'POWER OUTLET' loại 15A màu xanh dương. Tuyệt đối không thay thế cầu chì có ampe lớn hơn 15A."
            ],
            "image_contexts": [
                "/static/camry_fuse_diagram_page12.png"
            ]
        }
    elif "vf8" in car or "vinfast" in car:
        return {
            "text_contexts": [
                "Sổ tay VinFast VF8 - Trang 215: Hộp cầu chì khoang động cơ nằm ở góc phải phía trước của khoang máy. Cần tháo các lẫy khóa để nhấc nắp hộp cầu chì bảo vệ.",
                "Sổ tay VinFast VF8 - Trang 216: Cầu chì cổng sạc 12V (tẩu sạc phụ) ký hiệu là 'AUX_POWER_OUTLET' loại 15A nằm ở hàng thứ 3 của hộp cầu chì trong cabin xe."
            ],
            "image_contexts": [
                "/static/vf8_fuse_diagram_page45.png"
            ]
        }
    else:
        return {
            "text_contexts": [
                f"Sổ tay kỹ thuật {car_model} - Hộp cầu chì tổng: Vị trí các cầu chì bảo vệ hệ thống điện tử phụ trợ nằm trong khoang lái hoặc dưới nắp capo máy.",
                f"Sổ tay kỹ thuật {car_model} - Cầu chì tẩu sạc phụ trợ (12V): Vui lòng kiểm tra cầu chì ký hiệu Outlet/CIG loại 15A."
            ],
            "image_contexts": [
                "/static/default_fuse_diagram.png"
            ]
        }
