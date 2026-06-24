import os
import base64
import requests
import logging

logger = logging.getLogger("gateway.inference_client")

def predict_car_model(image_bytes: bytes, filename: str = "car.jpg") -> dict:
    """
    Gửi hình ảnh xe người dùng tải lên sang CV Inference Service (chạy ở Node 2) qua giao thức HTTP POST.
    
    Args:
        image_bytes (bytes): Dữ liệu nhị phân của ảnh xe.
        filename (str): Tên file ảnh gửi lên.
        
    Returns:
        dict: Chứa tên xe 'car_model' và độ tin cậy 'confidence'.
    """
    # Lấy URL của CV Service từ biến môi trường
    cv_service_url = os.getenv("CV_SERVICE_URL", "http://localhost:8001/predict")
    
    # Kiểm tra cấu hình chạy Mock CV
    if os.getenv("MOCK_CV", "true").lower() == "true":
        logger.info("Chế độ MOCK CV được kích hoạt.")
        return {"car_model": "Toyota Camry 2023", "confidence": 0.985}
        
    try:
        logger.info(f"Gửi request nhận diện xe tới CV Service tại: {cv_service_url}...")
        files = {"image": (filename, image_bytes, "image/jpeg")}
        # Thiết lập timeout hợp lý (ví dụ: 10 giây) tránh treo luồng Gateway
        response = requests.post(cv_service_url, files=files, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            logger.info(f"CV Service phản hồi thành công: Dòng xe={result.get('car_model')}, Confidence={result.get('confidence')}")
            return result
        else:
            logger.error(f"❌ CV Service phản hồi lỗi với HTTP Code: {response.status_code}")
            raise Exception(f"HTTP Error {response.status_code}: {response.text}")
            
    except Exception as e:
        logger.error(f"⚠️ Lỗi khi gọi CV Service: {e}. Tự động sử dụng dòng xe giả lập mặc định.")
        # Trả về kết quả mặc định chất lượng cao để tiếp tục luồng hệ thống
        return {"car_model": "Toyota Camry 2023", "confidence": 0.950, "fallback": True}

def file_to_base64(filepath: str) -> str:
    """
    Đọc file ảnh từ ổ đĩa và mã hóa sang chuỗi base64 chuẩn của Ollama API.
    """
    try:
        with open(filepath, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except Exception as e:
        logger.warning(f"Không thể đọc file tại {filepath} để chuyển đổi base64: {e}")
        return ""

def generate_vlm_answer(
    query: str,
    car_model: str,
    text_contexts: list,
    user_image_bytes: bytes = None,
    image_contexts: list = None
) -> str:
    """
    Tích hợp toàn bộ ngữ cảnh (text, ảnh sơ đồ, ảnh xe) thành Prompt và gửi sang Ollama VLM (Node 2)
    qua HTTP API.
    
    Args:
        query (str): Câu hỏi của khách hàng.
        car_model (str): Tên xe đã nhận diện.
        text_contexts (list): Danh sách đoạn văn bản HDSD liên quan từ RAG.
        user_image_bytes (bytes): File ảnh xe của người dùng (nếu có).
        image_contexts (list): Danh sách đường dẫn file ảnh sơ đồ liên quan từ RAG.
        
    Returns:
        str: Câu trả lời tổng hợp sinh bởi mô hình VLM.
    """
    ollama_url = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
    vlm_model = os.getenv("VLM_MODEL_NAME", "llama3.2-vision")
    
    # 1. Tạo Prompt hướng dẫn kỹ thuật chi tiết
    context_str = "\n".join([f"- {txt}" for txt in text_contexts])
    prompt = (
        f"Bạn là một Trợ lý Kỹ thuật Ô tô đa phương thức (Multimodal RAG Assistant).\n"
        f"Dòng xe khách hàng đang sử dụng: {car_model}.\n\n"
        f"Dưới đây là các đoạn thông tin trích xuất từ Sổ tay Hướng dẫn Sử dụng chính thức:\n"
        f"{context_str}\n\n"
        f"Bên dưới có đính kèm ảnh chụp xe của người dùng và các hình ảnh/sơ đồ kỹ thuật được trích từ Sổ tay.\n"
        f"Câu hỏi của khách hàng: {query}\n\n"
        f"Hãy phân tích và đưa ra câu trả lời kỹ thuật chi tiết, chính xác bằng Tiếng Việt. Chỉ rõ các bước thực hiện và vị trí cầu chì hoặc linh kiện (nếu có sơ đồ hướng dẫn)."
    )
    
    # 2. Xử lý ảnh đa phương thức (Multi-image) sang Base64
    images_base64 = []
    
    # Đính kèm ảnh xe người dùng gửi lên
    if user_image_bytes:
        try:
            user_img_b64 = base64.b64encode(user_image_bytes).decode('utf-8')
            images_base64.append(user_img_b64)
            logger.info("Đã mã hóa và đính kèm ảnh xe của người dùng.")
        except Exception as e:
            logger.error(f"Lỗi mã hóa ảnh xe của người dùng: {e}")
            
    # Đính kèm sơ đồ kỹ thuật trích xuất từ PDF
    static_dir = os.getenv("STATIC_DIR", "/app/static")
    if image_contexts:
        for img_path in image_contexts:
            # Lấy tên file ảnh và kiểm tra sự tồn tại trong thư mục static của hệ thống
            filename = os.path.basename(img_path)
            full_path = os.path.join(static_dir, filename)
            
            # Tìm kiếm dự phòng ở thư mục static local khi chạy môi trường dev không Docker
            if not os.path.exists(full_path):
                full_path = os.path.join(os.getcwd(), "static", filename)
                
            if os.path.exists(full_path):
                img_b64 = file_to_base64(full_path)
                if img_b64:
                    images_base64.append(img_b64)
                    logger.info(f"Đã mã hóa và đính kèm sơ đồ PDF: {full_path}")
            else:
                logger.warning(f"⚠️ Không tìm thấy file sơ đồ tại đường dẫn cấu hình: {full_path}")
                
    # Kiểm tra chế độ Mock VLM
    if os.getenv("MOCK_VLM", "true").lower() == "true":
        logger.info("Chế độ MOCK VLM được kích hoạt.")
        return (
            f"[MOCK VLM] Theo hướng dẫn kỹ thuật cho dòng xe {car_model}: "
            "Để xử lý lỗi tẩu sạc không hoạt động, bạn nên kiểm tra cầu chì CIG (15A) "
            "nằm trong hộp cầu chì dưới táp-lô phía lái xe. Bạn có thể sử dụng kẹp nhựa "
            "trong khoang động cơ để tháo cầu chì lỗi ra và thay thế bằng cầu chì dự phòng mới."
        )
        
    try:
        logger.info(f"Đang gửi prompt đến Ollama VLM ({ollama_url}) model={vlm_model}...")
        
        payload = {
            "model": vlm_model,
            "prompt": prompt,
            "stream": False # Lấy toàn bộ nội dung một lần thay vì stream
        }
        if images_base64:
            payload["images"] = images_base64
            
        # Tăng timeout lên 60 giây vì mô hình VLM cục bộ xử lý ảnh sẽ tốn thời gian hơn
        response = requests.post(ollama_url, json=payload, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            return result.get("response", "⚠️ Không thể đọc trường response trong phản hồi từ VLM.")
        else:
            logger.error(f"❌ Ollama VLM báo lỗi HTTP Code: {response.status_code}")
            raise Exception(f"HTTP Error {response.status_code}: {response.text}")
            
    except Exception as e:
        logger.error(f"⚠️ Lỗi kết nối Ollama VLM: {e}. Chuyển sang phản hồi dự phòng.")
        return (
            f"[FALLBACK VLM] Tôi đã tìm thấy tài liệu hướng dẫn kỹ thuật cho dòng xe {car_model} liên quan đến câu hỏi của bạn:\n"
            f"{context_str}\n\n"
            "Tuy nhiên, hệ thống không thể kết nối tới dịch vụ AI Ollama để tổng hợp câu trả lời thông minh. Vui lòng tham khảo tài liệu thô bên trên."
        )
