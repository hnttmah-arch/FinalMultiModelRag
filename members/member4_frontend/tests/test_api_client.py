import pytest
import requests
from unittest.mock import patch

# Gateway URL for tests
GATEWAY_URL = "http://localhost:8000/api/v1/inference"

# Note: Since tests need the Gateway to be running, we can mock the `requests.post` call
# or write Integration tests that assume the Gateway is up.
# Here we write Integration Tests that mock `requests.post` for CI/CD simplicity.

@patch('app.ui.api_client.requests.post')
def test_process_request_success(mock_post):
    from app.ui.api_client import process_request
    
    # Setup mock response
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {
        "status": 200, "car_model": "Kia", "confidence": 0.99, "rag_answer": "Test", "latency_ms": 1000
    }
    
    # We pass a dummy class to mock `image_data`
    class DummyFile:
        name = "test.png"
        type = "image/png"
        def getvalue(self): return b"dummy"
        
    res = process_request(image_data=DummyFile(), text_query="Lỗi")
    
    assert res["status"] == 200
    assert res["car_model"] == "Kia"

@patch('app.ui.api_client.requests.post')
def test_process_request_timeout(mock_post):
    from app.ui.api_client import process_request
    
    # Simulate timeout
    mock_post.side_effect = requests.exceptions.Timeout("Timeout")
    
    class DummyFile:
        name = "test.png"
        type = "image/png"
        def getvalue(self): return b"dummy"
        
    res = process_request(image_data=DummyFile(), text_query="Lỗi")
    assert res["status"] == 504
    assert "Timeout" in res["error"]

@patch('app.ui.api_client.requests.post')
def test_process_request_connection_error(mock_post):
    from app.ui.api_client import process_request
    
    # Simulate completely down server (ConnectionError)
    mock_post.side_effect = requests.exceptions.ConnectionError("Connection refused")
    
    class DummyFile:
        name = "test.png"
        type = "image/png"
        def getvalue(self): return b"dummy"
        
    res = process_request(image_data=DummyFile(), text_query="Lỗi")
    assert res["status"] == 500
    assert "Lỗi kết nối mạng" in res["error"]
