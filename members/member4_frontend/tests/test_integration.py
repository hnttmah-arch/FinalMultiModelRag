import pytest
from fastapi.testclient import TestClient
from app.gateway.main import app

client = TestClient(app)

def test_integration_missing_image():
    # Gọi API Gateway mà không có ảnh, Gateway phải trả về 400
    response = client.post("/api/v1/inference", data={"query": "test query"})
    assert response.status_code == 400
    assert "Thiếu dữ liệu ảnh đầu vào" in response.json()["detail"]

def test_integration_missing_query():
    # Gọi API Gateway có ảnh nhưng không có query/audio, Gateway trả về 400
    file_data = {"image": ("test.jpg", b"dummy image data", "image/jpeg")}
    response = client.post("/api/v1/inference", files=file_data)
    assert response.status_code == 400
    assert "Thiếu câu hỏi" in response.json()["detail"]

def test_integration_success():
    # Gọi API thành công
    file_data = {"image": ("test.jpg", b"dummy image data", "image/jpeg")}
    response = client.post("/api/v1/inference", files=file_data, data={"query": "đèn báo lỗi"})
    
    # Do gateway của chúng ta giả lập có tỷ lệ 10% trả về 504 Timeout
    # Nếu bị 504 thì ta cũng pass test vì đó là behavior mong muốn của Mock
    assert response.status_code in [200, 504]
    
    if response.status_code == 200:
        json_data = response.json()
        assert json_data["status"] == 200
        assert "car_model" in json_data
        assert "rag_answer" in json_data
