import pytest

# Dummy class để giả lập UploadedFile của Streamlit
class DummyUploadedFile:
    def __init__(self, size_bytes):
        self.size = size_bytes

def test_validate_inputs_missing_image():
    from app.ui.main import validate_inputs
    is_valid, msg = validate_inputs(None, "lỗi", None)
    assert is_valid is False
    assert "tải lên Hình ảnh" in msg

def test_validate_inputs_size_exceeded():
    from app.ui.main import validate_inputs
    large_file = DummyUploadedFile(6 * 1024 * 1024) # 6MB
    is_valid, msg = validate_inputs(large_file, "lỗi", None)
    assert is_valid is False
    assert "quá lớn" in msg

def test_validate_inputs_missing_query():
    from app.ui.main import validate_inputs
    normal_file = DummyUploadedFile(2 * 1024 * 1024) # 2MB
    is_valid, msg = validate_inputs(normal_file, "", None)
    assert is_valid is False
    assert "nhập câu hỏi" in msg

def test_validate_inputs_success():
    from app.ui.main import validate_inputs
    normal_file = DummyUploadedFile(2 * 1024 * 1024) # 2MB
    is_valid, msg = validate_inputs(normal_file, "lỗi", None)
    assert is_valid is True
    assert msg == ""
