import streamlit as st
import time
import os
from app.ui.api_client import process_request
import app.ui.api_client as api_client

# Đọc biến môi trường
api_client.GATEWAY_URL = os.getenv("GATEWAY_URL", "http://localhost:8000")

# --- Frontend: Page Config ---
st.set_page_config(page_title="AutoDiag AI", page_icon="🚘", layout="wide")

# --- CSS Chuyên nghiệp (Commercial Look) ---
st.markdown("""
<style>
    /* Ẩn header và footer mặc định của Streamlit để trông giống app Native hơn */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Import Font Inter cao cấp */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Thiết kế Nút bấm (Call to Action) */
    .stButton>button {
        background-color: #0F172A;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 0.6rem 1.2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }
    .stButton>button:hover {
        background-color: #2563EB;
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(37, 99, 235, 0.2), 0 4px 6px -2px rgba(37, 99, 235, 0.1);
        color: white;
    }
    
    /* Thẻ thông số (Metric Cards) */
    .metric-card {
        border: 1px solid rgba(100, 116, 139, 0.2);
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
        height: 100%;
    }
    .metric-value {
        font-size: 1.6rem;
        font-weight: 800;
        margin-top: 8px;
    }
    .metric-label {
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        opacity: 0.7;
    }
    
    /* Hộp Kết quả (Result Box) */
    .success-box {
        background: linear-gradient(145deg, rgba(34, 197, 94, 0.1) 0%, rgba(59, 130, 246, 0.05) 100%);
        border-left: 4px solid #22C55E;
        padding: 24px;
        border-radius: 0 12px 12px 0;
        margin-top: 24px;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02);
    }
    .success-box h4 {
        margin-top: 0;
        margin-bottom: 12px;
        font-weight: 700;
        font-size: 1.1rem;
    }
    .success-box p {
        margin: 0;
        line-height: 1.7;
        font-size: 1rem;
    }
    
    /* Header Container */
    .main-header {
        text-align: center;
        padding-bottom: 24px;
        border-bottom: 1px solid rgba(100, 116, 139, 0.2);
        margin-bottom: 32px;
        margin-top: 10px;
    }
    .main-header h1 {
        font-weight: 800;
        letter-spacing: -0.03em;
        margin-bottom: 8px;
        font-size: 2.5rem;
    }
    .main-header p {
        font-size: 1.1rem;
        opacity: 0.8;
        margin: 0;
    }
    
    /* Định dạng lại File Uploader để nhìn gọn gàng hơn */
    div[data-testid="stFileUploader"] {
        border: 2px dashed rgba(100, 116, 139, 0.3);
        border-radius: 12px;
        padding: 16px;
    }
</style>
""", unsafe_allow_html=True)

# --- Các hàm Validation (Member 4 QA Task) ---
def validate_inputs(img_file, text_val, audio_val):
    if not img_file:
        return False, "Vui lòng tải lên Hình ảnh táp-lô xe để hệ thống có thể nhận diện."
    
    # Kiểm tra kích thước (Max 5MB)
    if img_file.size > 5 * 1024 * 1024:
        return False, f"File ảnh tải lên quá lớn ({img_file.size / (1024*1024):.1f} MB). Vui lòng chọn ảnh dưới 5MB để đảm bảo hiệu năng LAN."
    
    if not text_val and not audio_val:
        return False, "Vui lòng nhập câu hỏi dạng Văn bản hoặc Giọng nói."
        
    return True, ""

# --- Header ---
st.markdown("""
<div class="main-header">
    <h1><span style='color: #2563EB;'>Auto</span>Diag AI</h1>
    <p>Hệ thống Chuẩn đoán Thông minh & Trợ lý Bảo dưỡng</p>
</div>
""", unsafe_allow_html=True)

# --- Main Layout ---
col_input, col_spacing, col_output = st.columns([4.5, 0.5, 5])

with col_input:
    st.markdown("#### 📥 Dữ liệu Đầu vào")
    st.markdown("<p style='font-size: 0.9rem; opacity: 0.7; margin-bottom: 16px;'>Cung cấp hình ảnh táp-lô và mô tả vấn đề bạn đang gặp phải.</p>", unsafe_allow_html=True)
    
    img = st.file_uploader("Hình ảnh Táp-lô (Bắt buộc - Tối đa 5MB)", type=["png", "jpg", "jpeg"])
    
    st.markdown("<br/>", unsafe_allow_html=True)
    query = st.text_input("Mô tả Vấn đề (Văn bản)", placeholder="VD: Đèn cảnh báo màu vàng hình bình chứa nước là lỗi gì?")
    
    audio = st.audio_input("Hoặc Ghi âm Trực tiếp") if hasattr(st, 'audio_input') else st.file_uploader("Upload file Audio", type=["wav", "mp3"])

    st.markdown("<br/>", unsafe_allow_html=True)
    submit_btn = st.button("🚀 PHÂN TÍCH DỮ LIỆU")

with col_output:
    st.markdown("#### 📋 Kết quả Chuẩn đoán")
    
    if submit_btn:
        # Chạy logic Validation của QA
        is_valid, error_msg = validate_inputs(img, query, audio)
        
        if not is_valid:
            st.error(f"⚠️ **Validation Error:** {error_msg}")
        else:
            with st.spinner("Đang xử lý dữ liệu qua mô hình AI (Node 2)..."):
                start_time = time.time()
                res = process_request(img, text_query=query, audio_data=audio)
                
                status = res.get("status")
                if status == 200:
                    # Metrics Row
                    c1, c2, c3 = st.columns(3)
                    with c1:
                        st.markdown(f"<div class='metric-card'><div class='metric-label'>Dòng xe</div><div class='metric-value' style='color:#2563EB;'>{res['car_model']}</div></div>", unsafe_allow_html=True)
                    with c2:
                        st.markdown(f"<div class='metric-card'><div class='metric-label'>Độ tin cậy</div><div class='metric-value' style='color:#059669;'>{res['confidence']*100}%</div></div>", unsafe_allow_html=True)
                    with c3:
                        latency = res.get('latency_ms', 0)
                        st.markdown(f"<div class='metric-card'><div class='metric-label'>Xử lý Model</div><div class='metric-value'>{latency}<span style='font-size: 0.9rem; font-weight: 500;'> ms</span></div></div>", unsafe_allow_html=True)
                    
                    # Result Box
                    st.markdown(f"""
                    <div class='success-box'>
                        <h4 style='color: #166534;'>Hướng dẫn Xử lý chi tiết</h4>
                        <p>{res['rag_answer']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    total_time = int((time.time() - start_time)*1000)
                    st.caption(f"Network roundtrip: {total_time} ms")
                    
                # Bắt lỗi theo yêu cầu MLOps/QA
                elif status == 504:
                    st.error("🔌 **Lỗi Timeout (Quá tải Model):** Máy chủ AI (Node 2) đang bận xử lý hoặc không phản hồi quá 10 giây. Vui lòng thử lại sau.")
                elif status == 500:
                    st.error("⚠️ **Lỗi Internal Server / Mạng LAN:** Không thể kết nối hoặc API Gateway gặp sự cố. Vui lòng kiểm tra IP tĩnh của Node 2 và Firewall.")
                else:
                    st.error(f"❌ **Lỗi {status}:** {res.get('error', 'Unknown Error')}")
    else:
        st.info("Hệ thống đang trong trạng thái chờ. Vui lòng cung cấp dữ liệu ở khung bên trái và chọn Phân tích.")
