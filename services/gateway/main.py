import time
import logging
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST, REGISTRY

# Import các helper module nội bộ
from speech_to_text import transcribe_audio_file
from rag_client import retrieve_context_from_db
from inference_client import predict_car_model, generate_vlm_answer

# Cấu hình logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("gateway.main")

app = FastAPI(title="Multimodal RAG API Gateway", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- KHỞI TẠO METRICS PROMETHEUS (MLOps) ---
# Tránh lỗi trùng lặp đăng ký khi uvicorn reload
for metric_name in ['gateway_requests_total', 'gateway_request_duration_seconds', 'gateway_cv_latency_seconds', 'gateway_vlm_latency_seconds']:
    if metric_name in REGISTRY._names_to_collectors:
        REGISTRY.unregister(REGISTRY._names_to_collectors[metric_name])

# Đếm số lượng request và mã trạng thái trả về
REQUEST_COUNT = Counter(
    'gateway_requests_total', 
    'Tổng số HTTP Requests gửi đến API Gateway', 
    ['method', 'endpoint', 'status_code']
)

# Đo lường thời gian xử lý các phân đoạn chính
LATENCY_TOTAL = Histogram('gateway_request_duration_seconds', 'Thời gian xử lý toàn trình của request')
LATENCY_CV = Histogram('gateway_cv_latency_seconds', 'Thời gian suy luận của CV Service ở Node 2')
LATENCY_VLM = Histogram('gateway_vlm_latency_seconds', 'Thời gian sinh câu trả lời của VLM ở Node 2')


@app.get("/")
def read_root():
    REQUEST_COUNT.labels(method="GET", endpoint="/", status_code="200").inc()
    return {"message": "API Gateway is running!"}


@app.get("/metrics")
def metrics():
    """
    Endpoint xuất dữ liệu metrics định dạng Prometheus để Prometheus Server định kỳ scrape.
    """
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.post("/api/query")
async def query_assistant(
    image: UploadFile = File(None),
    query_text: str = Form(None),
    voice_file: UploadFile = File(None)
):
    start_total = time.time()
    
    if not image:
        REQUEST_COUNT.labels(method="POST", endpoint="/api/query", status_code="400").inc()
        raise HTTPException(status_code=400, detail="Vui lòng cung cấp hình ảnh xe để nhận diện.")
        
    try:
        # 1. Chuyển đổi giọng nói thành văn bản nếu có file âm thanh
        if voice_file:
            logger.info(f"Nhận file âm thanh: {voice_file.filename}")
            try:
                audio_bytes = await voice_file.read()
                transcribed_text = transcribe_audio_file(audio_bytes)
                if transcribed_text:
                    query_text = transcribed_text
            except Exception as e:
                logger.error(f"Lỗi đọc file âm thanh: {e}")
                
        # Nếu sau khi check cả voice vẫn không có câu hỏi, đặt câu hỏi mặc định
        if not query_text:
            query_text = "Làm sao để thay thế cầu chì tẩu sạc?"
            logger.info("Không nhận được câu hỏi, sử dụng câu hỏi mặc định.")

        # Đọc dữ liệu ảnh xe để truyền cho các service
        image_bytes = await image.read()
        
        # 2. Gọi CV Service nhận dạng dòng xe
        logger.info("Giai đoạn 1: Nhận diện dòng xe...")
        start_cv = time.time()
        cv_result = predict_car_model(image_bytes, image.filename)
        cv_latency = time.time() - start_cv
        LATENCY_CV.observe(cv_latency) # Ghi nhận latency CV
        
        car_model = cv_result.get("car_model", "Toyota Camry 2023")
        confidence = cv_result.get("confidence", 1.0)
        
        # 3. Truy vấn Vector DB lấy ngữ cảnh sổ tay ô tô
        logger.info(f"Giai đoạn 2: Tìm kiếm ngữ cảnh cho {car_model}...")
        rag_result = retrieve_context_from_db(query=query_text, car_model=car_model)
        
        text_contexts = rag_result.get("text_contexts", [])
        image_contexts = rag_result.get("image_contexts", [])
        
        # 4. Gửi Prompt và các ảnh ngữ cảnh sang Ollama VLM
        logger.info("Giai đoạn 3: Sinh câu trả lời qua VLM...")
        start_vlm = time.time()
        answer = generate_vlm_answer(
            query=query_text,
            car_model=car_model,
            text_contexts=text_contexts,
            user_image_bytes=image_bytes,
            image_contexts=image_contexts
        )
        vlm_latency = time.time() - start_vlm
        LATENCY_VLM.observe(vlm_latency) # Ghi nhận latency VLM
        
        # 5. Ghi nhận thời gian hoàn tất toàn trình
        total_latency = time.time() - start_total
        LATENCY_TOTAL.observe(total_latency)
        
        # Tăng Counter đếm request thành công
        REQUEST_COUNT.labels(method="POST", endpoint="/api/query", status_code="200").inc()
        
        return {
            "status": "success",
            "car_model": car_model,
            "confidence": confidence,
            "query": query_text,
            "answer": answer,
            "retrieved_diagrams": image_contexts
        }
        
    except Exception as e:
        logger.error(f"❌ Lỗi xử lý request trong API Gateway: {e}")
        REQUEST_COUNT.labels(method="POST", endpoint="/api/query", status_code="500").inc()
        raise HTTPException(status_code=500, detail=f"Lỗi hệ thống: {str(e)}")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
