from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional
import time
import random
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(title="Node 1 - API Gateway (MOCK)", description="Gateway nhận request từ Streamlit UI, gọi Mock VectorDB và Node 2")

# Tích hợp Prometheus Metrics vào FastAPI (đo Latency, Request count, Error rate)
Instrumentator().instrument(app).expose(app, endpoint="/metrics")

@app.post("/api/v1/inference")
async def inference(
    image: Optional[UploadFile] = File(None, description="Ảnh táp-lô"),
    query: Optional[str] = Form(None, description="Câu hỏi text"),
    audio: Optional[UploadFile] = File(None, description="Câu hỏi giọng nói")
):
    """
    Endpoint nhận dữ liệu đa phương thức.
    Trong thực tế, hàm này sẽ:
    1. Gọi Speech-to-Text nếu có audio.
    2. Gọi ChromaDB để lấy ngữ cảnh.
    3. Gửi Request sang LAN IP của Node 2.
    Hiện tại, đây là Mock (Giả lập) để Member 4 có thể test.
    """
    if not image:
        raise HTTPException(status_code=400, detail="Thiếu dữ liệu ảnh đầu vào (Image is required).")
    
    if not query and not audio:
        raise HTTPException(status_code=400, detail="Thiếu câu hỏi (Text query hoặc Audio data là bắt buộc).")

    # Giả lập xử lý timeout
    if random.random() < 0.1:
        time.sleep(3)
        raise HTTPException(status_code=504, detail="Timeout: Node 2 không phản hồi sau 3 giây.")

    # Giả lập quá trình xử lý GPU trên Node 2
    latency = random.uniform(1.2, 2.5)
    time.sleep(latency)
    
    actual_query = query
    if audio and not query:
        actual_query = "[Đã chuyển giọng nói thành văn bản]: Đèn này là đèn gì?"

    return JSONResponse(content={
        "status": 200,
        "car_model": "Kia Seltos",
        "confidence": 0.98,
        "rag_answer": f"Với thắc mắc '{actual_query}', theo sổ tay hướng dẫn, bạn cần dừng xe an toàn, tắt máy và gọi cứu hộ để kiểm tra hệ thống điện.",
        "latency_ms": int(latency * 1000)
    })
