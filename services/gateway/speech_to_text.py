import os
import logging
from google.cloud import speech

# Thiết lập Logger để theo dõi quá trình chạy
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("gateway.speech_to_text")

def transcribe_audio_file(audio_bytes: bytes) -> str:
    """
    Chuyển đổi file âm thanh (giọng nói) sang dạng văn bản sử dụng Google Cloud Speech-to-Text.
    Hỗ trợ cơ chế Fallback (Giả lập) nếu không có cấu hình key Google Cloud để không làm gián đoạn luồng test.
    
    Args:
        audio_bytes (bytes): Dữ liệu nhị phân của file âm thanh tải lên (.wav, .mp3, .ogg...)
        
    Returns:
        str: Văn bản sau khi nhận diện hoặc văn bản giả lập (mock)
    """
    # Lấy đường dẫn file credentials từ biến môi trường
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    
    # 1. Cơ chế kiểm tra và Fallback nếu thiếu key Google Cloud
    if not credentials_path or not os.path.exists(credentials_path):
        logger.warning(
            "⚠️ GOOGLE_APPLICATION_CREDENTIALS chưa được thiết lập hoặc file không tồn tại. "
            "Chuyển sang chế độ GIẢ LẬP (MOCK) STT."
        )
        # Trả về câu hỏi giả định để bạn có thể tiếp tục kiểm thử luồng tích hợp với RAG và CV
        return "Làm sao để thay thế cầu chì tẩu sạc xe Toyota Camry 2023?"
        
    try:
        # 2. Khởi tạo SpeechClient bằng thư viện chính thức của Google Cloud
        client = speech.SpeechClient()
        
        # 3. Đóng gói audio và cấu hình nhận diện
        audio = speech.RecognitionAudio(content=audio_bytes)
        config = speech.RecognitionConfig(
            # Nhận dạng tiếng Việt làm mặc định
            language_code="vi-VN",
            # Google STT có thể tự phát hiện encoding và sample rate cho các định dạng phổ biến như WAV, FLAC.
            # Tuy nhiên, nếu gặp định dạng thô (RAW PCM), bạn có thể cần chỉ định rõ ở đây.
            enable_automatic_punctuation=True, # Tự động thêm dấu câu
        )
        
        logger.info("Đang gửi yêu cầu chuyển đổi giọng nói tới Google Cloud Speech-to-Text API...")
        response = client.recognize(config=config, audio=audio)
        
        # 4. Trích xuất văn bản từ phản hồi của Google
        transcripts = []
        for result in response.results:
            # Chọn phương án thay thế có độ tin cậy cao nhất (index 0)
            best_alternative = result.alternatives[0]
            transcripts.append(best_alternative.transcript)
            logger.info(f"Kết quả phân đoạn: {best_alternative.transcript} (Độ tin cậy: {best_alternative.confidence:.2f})")
            
        if transcripts:
            full_text = " ".join(transcripts)
            logger.info(f"Hoàn thành chuyển đổi giọng nói: '{full_text}'")
            return full_text
        else:
            logger.warning("Google STT API phản hồi thành công nhưng không tìm thấy đoạn hội thoại nào.")
            return ""
            
    except Exception as e:
        logger.error(f"❌ Lỗi khi kết nối Google Cloud Speech-to-Text API: {e}")
        # Fallback sang Mock khi có lỗi xảy ra để hệ thống không bị crash
        return "[FALLBACK STT] Đã xảy ra lỗi API. Cần kiểm tra lại cấu hình mạng hoặc key Google."
