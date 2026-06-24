import streamlit as st
import requests

st.set_page_config(page_title="Multimodal RAG Assistant", layout="wide")

st.title("🚗 Trợ lý Ảo Nhận diện Xe & Tra cứu Sổ tay (Multimodal RAG)")
st.write("Hệ thống trợ lý ảo đa phương thức giúp nhận dạng dòng xe và trả lời các thắc mắc về kỹ thuật dựa trên sổ tay hướng dẫn sử dụng.")

# Layout
col1, col2 = st.columns([1, 1])

with col1:
    st.header("📸 Tải lên hình ảnh xe & Nhập câu hỏi")
    uploaded_file = st.file_uploader("Chọn ảnh xe...", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        st.image(uploaded_file, caption="Ảnh xe đã tải lên", use_container_width=True)
        
    query_type = st.radio("Phương thức nhập câu hỏi:", ["Văn bản (Text)", "Giọng nói (Voice)"])
    
    if query_type == "Văn bản (Text)":
        user_query = st.text_input("Nhập câu hỏi của bạn tại đây...", placeholder="Ví dụ: Làm sao để thay cầu chì tẩu sạc?")
    else:
        st.info("Tính năng thu âm trực tiếp đang được cấu hình...")
        user_query = st.text_input("Hoặc nhập câu hỏi tạm thời...")

    submit_btn = st.button("Gửi yêu cầu", type="primary")

with col2:
    st.header("💡 Phản hồi từ Trợ lý Ảo")
    if submit_btn:
        st.info("Đang xử lý yêu cầu qua API Gateway...")
        # Placeholder call to gateway
        # response = requests.post("http://gateway:8000/api/query", files=...)
        st.success("Nhận dạng dòng xe thành công!")
        st.markdown("**Kết quả nhận diện**: *Toyota Camry 2023 (Độ tin cậy: 98.5%)*")
        st.markdown("**Trả lời**: *Đang chờ tích hợp API thực tế...*")
    else:
        st.write("Kết quả truy vấn và sơ đồ hướng dẫn sẽ hiển thị tại đây sau khi bạn nhấn nút 'Gửi yêu cầu'.")
