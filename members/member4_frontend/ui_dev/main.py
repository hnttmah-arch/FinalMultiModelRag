import streamlit as st
import time
import os
from app.ui.api_client import process_request
import app.ui.api_client as api_client

# Đọc biến môi trường
api_client.GATEWAY_URL = os.getenv("GATEWAY_URL", "http://localhost:8000")

# --- Frontend: Page Config ---
st.set_page_config(page_title="AutoDiag AI", page_icon="🚘", layout="wide")

# --- Session State cho tính năng Làm mới ---
if "reset_key" not in st.session_state:
    st.session_state.reset_key = 0

def clear_data():
    st.session_state.reset_key += 1

# --- CSS Chuyên nghiệp (Dark Mode, Futuristic, Tech Mesh) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
    }
    
    :root {
      --neon-teal: #06b6d4;
      --mint-green: #34d399;
      --bg-navy: #111827;
      --card-bg: #1f2937;
      --text-light: #f3f4f6;
      --text-dim: #9ca3af;
    }

    /* App Background with Technical Mesh */
    .stApp {
        background-color: var(--bg-navy);
        background-image: 
            radial-gradient(circle at 50% 10%, rgba(6, 182, 212, 0.15) 0%, transparent 40%),
            linear-gradient(rgba(255, 255, 255, 0.02) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255, 255, 255, 0.02) 1px, transparent 1px);
        background-size: 100% 100%, 40px 40px, 40px 40px;
        color: var(--text-light);
    }
    
    /* Header */
    .premium-header {
        text-align: center;
        padding: 2rem 0 3rem 0;
    }
    .premium-header h1 {
        font-weight: 800;
        font-size: 3.5rem;
        color: var(--neon-teal);
        text-shadow: 0 0 20px rgba(6, 182, 212, 0.4);
        margin-bottom: 0.5rem;
        letter-spacing: -1px;
    }
    .premium-header p {
        font-size: 1.15rem;
        color: var(--mint-green);
        opacity: 0.9;
        font-weight: 500;
    }

    /* Card styling (Targeting Streamlit Columns) */
    [data-testid="column"]:nth-of-type(1),
    [data-testid="column"]:nth-of-type(3) {
        background: var(--card-bg);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.25);
    }
    
    [data-testid="column"]:nth-of-type(2) {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }

    /* Column titles */
    h3 {
        color: var(--neon-teal) !important;
        font-weight: 600 !important;
        font-size: 1.25rem !important;
        padding-bottom: 12px;
        border-bottom: 1px solid rgba(6, 182, 212, 0.2);
        margin-bottom: 1.5rem !important;
    }
    
    /* Sub-headers */
    .sub-header {
        color: var(--text-light);
        font-weight: 600;
        font-size: 0.95rem;
        margin-bottom: 12px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* File uploader custom (Dashed Teal) */
    div[data-testid="stFileUploader"] {
        background: rgba(17, 24, 39, 0.4);
        border: 2px dashed var(--neon-teal);
        border-radius: 8px;
        padding: 1rem;
    }
    div[data-testid="stFileUploader"] section {
        color: var(--text-light) !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        border-bottom: none;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        padding: 8px 16px;
        color: var(--text-dim);
    }
    .stTabs [aria-selected="true"] {
        background-color: rgba(6, 182, 212, 0.15) !important;
        border: 1px solid var(--neon-teal) !important;
        color: var(--neon-teal) !important;
    }
    .stTabs [data-baseweb="tab-highlight"] {
        display: none;
    }
    
    /* Text Input */
    div[data-baseweb="input"] {
        background-color: rgba(17, 24, 39, 0.8);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 8px;
    }
    
    /* Buttons */
    .stButton>button[kind="primary"], .stButton>button:first-child {
        background: var(--neon-teal);
        color: #000;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
        font-weight: 700;
        transition: all 0.2s ease;
    }
    .stButton>button[kind="primary"]:hover, .stButton>button:first-child:hover {
        background: #22d3ee;
        box-shadow: 0 0 15px rgba(6, 182, 212, 0.4);
        color: #000;
    }
    
    .stButton>button[kind="secondary"] {
        background: transparent !important;
        color: var(--neon-teal) !important;
        border: 1px solid var(--neon-teal) !important;
        border-radius: 8px !important;
        font-weight: 600;
    }
    .stButton>button[kind="secondary"]:hover {
        background: rgba(6, 182, 212, 0.1) !important;
        color: #22d3ee !important;
    }
    
    /* Results Grid Table */
    .results-grid {
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        overflow: hidden;
    }
    .grid-row {
        display: flex;
        justify-content: space-between;
        padding: 12px 16px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        background: rgba(17, 24, 39, 0.4);
    }
    .grid-row:last-child {
        border-bottom: none;
    }
    .grid-label {
        color: var(--text-dim);
        font-size: 0.95rem;
    }
    .grid-value {
        color: white;
        font-weight: 600;
        font-size: 0.95rem;
    }
    .grid-value.mint {
        color: var(--mint-green);
    }
    
    /* RAG Answer */
    .rag-answer {
        background: rgba(17, 24, 39, 0.8);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 20px;
        border-radius: 8px;
        line-height: 1.6;
        margin: 10px 0 20px 0;
        color: var(--text-light);
    }
    
    /* Reference Link */
    .ref-link {
        color: var(--neon-teal);
        text-decoration: none;
        display: flex;
        align-items: center;
        gap: 6px;
        font-size: 0.95rem;
    }
    .ref-link:hover {
        text-decoration: underline;
    }
    
    /* Limit Image Height to avoid scrolling */
    [data-testid="stImage"] img {
        max-height: 250px;
        object-fit: cover;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# --- Các hàm Validation ---
def validate_inputs(img_file, text_val, audio_val):
    if not img_file:
        return False, "Vui lòng tải lên Hình ảnh xe để nhận diện."
    if img_file.size > 5 * 1024 * 1024:
        return False, f"File ảnh tải lên quá lớn ({img_file.size / (1024*1024):.1f} MB)."
    if not text_val and not audio_val:
        return False, "Vui lòng nhập câu hỏi dạng Văn bản hoặc Giọng nói."
    return True, ""

# --- Header ---
st.markdown("""
<div class="premium-header">
    <h1>AutoDiag AI</h1>
    <p>Hệ thống Chuẩn đoán thông minh & Trợ lý Bảo dưỡng Đa phương thức</p>
</div>
""", unsafe_allow_html=True)

# --- Main Layout ---
col_input, col_spacing, col_output = st.columns([4.2, 0.3, 5.5])

with col_input:
    st.markdown("### ĐẦU VÀO ĐA PHƯƠNG THỨC")
    
    img = st.file_uploader("Tải lên hình ảnh xe (Bắt buộc)", type=["png", "jpg", "jpeg"], key=f"img_{st.session_state.reset_key}")
    
    st.markdown("<br/>", unsafe_allow_html=True)
    
    tab_text, tab_voice = st.tabs(["Nhập Văn bản", "Ghi âm Giọng nói"])
    
    with tab_text:
        query = st.text_input("Nhập câu hỏi", placeholder="Ví dụ: Đèn áp suất lốp sáng trên xe VF8?", key=f"text_{st.session_state.reset_key}", label_visibility="collapsed")
    
    with tab_voice:
        audio_key = f"audio_{st.session_state.reset_key}"
        audio = st.audio_input("Ghi âm", key=audio_key, label_visibility="collapsed") if hasattr(st, 'audio_input') else st.file_uploader("Upload file Audio", type=["wav", "mp3"], key=audio_key, label_visibility="collapsed")

    st.markdown("<br/>", unsafe_allow_html=True)
    
    col_submit, col_clear = st.columns([1.5, 1])
    with col_submit:
        submit_btn = st.button("BẮT ĐẦU TRUY VẤN", type="primary", use_container_width=True)
    with col_clear:
        st.button("LÀM MỚI", on_click=clear_data, type="secondary", use_container_width=True)

with col_output:
    st.markdown("### KẾT QUẢ & PHÂN TÍCH")
    
    if submit_btn:
        is_valid, error_msg = validate_inputs(img, query, audio)
        
        if not is_valid:
            st.error(f"⚠️ **Validation Error:** {error_msg}")
        else:
            with st.spinner("Đang xử lý phân tích AI..."):
                start_time = time.time()
                res = process_request(img, text_query=query, audio_data=audio)
                
                status = res.get("status")
                if status == 200:
                    st.markdown("<div class='sub-header'>KẾT QUẢ NHẬN DIỆN XE:</div>", unsafe_allow_html=True)
                    
                    c_img, c_info = st.columns([0.8, 1.2])
                    with c_img:
                        st.image(img, use_container_width=True, caption="Heatmap XAI")
                    with c_info:
                        st.markdown(f"""
                        <div class="results-grid">
                            <div class="grid-row">
                                <span class="grid-label">Mô hình:</span>
                                <span class="grid-value">EfficientNet</span>
                            </div>
                            <div class="grid-row">
                                <span class="grid-label">Dòng xe:</span>
                                <span class="grid-value mint">{res['car_model']}</span>
                            </div>
                            <div class="grid-row">
                                <span class="grid-label">Xác suất:</span>
                                <span class="grid-value mint">{res['confidence']*100:.1f}%</span>
                            </div>
                            <div class="grid-row">
                                <span class="grid-label">Độ trễ:</span>
                                <span class="grid-value">{res.get('latency_ms', 0)} ms</span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.markdown("<br/>", unsafe_allow_html=True)
                    st.markdown("<div class='sub-header'>CÂU TRẢ LỜI CỦA TRỢ LÝ (RAG):</div>", unsafe_allow_html=True)
                    st.markdown(f"""
                    <div class='rag-answer'>
                        {res['rag_answer']}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("<div class='sub-header'>NGUỒN THAM KHẢO (PDF):</div>", unsafe_allow_html=True)
                    st.markdown("""
                    <a href="#" class="ref-link">
                        📄 Sổ tay Hướng dẫn Sử dụng (Trang 120, 123)
                    </a>
                    """, unsafe_allow_html=True)
                    
                elif status == 504:
                    st.error("🔌 **Lỗi Timeout:** Máy chủ AI (Node 2) đang quá tải.")
                else:
                    st.error(f"❌ **Lỗi {status}:** {res.get('error', 'Unknown Error')}")
    else:
        st.markdown("""
        <div style="text-align: center; padding: 100px 20px; color: #9ca3af;">
            <p>Vui lòng upload ảnh và đặt câu hỏi ở khung bên trái để bắt đầu truy vấn.</p>
        </div>
        """, unsafe_allow_html=True)
