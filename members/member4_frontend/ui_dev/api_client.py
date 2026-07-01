import requests
from typing import Optional, Dict, Any

# Mặc định trỏ về Gateway. Khi chạy Docker, biến môi trường GATEWAY_URL sẽ là http://gateway:8000
GATEWAY_URL = "http://localhost:8000"

def process_request(image_data: Any, text_query: str = "", audio_data: Optional[Any] = None) -> Dict[str, Any]:
    """
    Gửi request từ Streamlit UI tới FastAPI Gateway qua HTTP POST.
    Sử dụng multipart/form-data.
    """
    url = f"{GATEWAY_URL}/api/v1/inference"
    
    files = {}
    data = {}
    
    if image_data:
        files["image"] = (image_data.name, image_data.getvalue(), image_data.type)
        
    if audio_data:
        files["audio"] = (audio_data.name, audio_data.getvalue(), audio_data.type)
        
    if text_query:
        data["query"] = text_query

    try:
        response = requests.post(url, files=files, data=data, timeout=10) # Timeout 10s
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        return {"status": 504, "error": "Timeout: Không thể kết nối tới API Gateway hoặc Node 2."}
    except requests.exceptions.RequestException as e:
        # Gateway trả về lỗi 400 hoặc 500
        if e.response is not None:
            try:
                error_detail = e.response.json().get("detail", str(e))
            except ValueError:
                error_detail = e.response.text
            return {"status": e.response.status_code, "error": error_detail}
        return {"status": 500, "error": f"Lỗi kết nối mạng: {str(e)}"}
