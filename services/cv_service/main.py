from fastapi import FastAPI, UploadFile, File
import uvicorn

app = FastAPI(title="Computer Vision Service (Node 2)", version="1.0.0")

@app.get("/")
def read_root():
    return {"message": "CV Service is running!"}

@app.post("/predict")
async def predict_car_model(image: UploadFile = File(...)):
    # Đọc file ảnh đầu vào
    # Tiến hành suy luận qua mô hình PyTorch (ResNet/EfficientNet)
    # Trả về nhãn dự báo và độ tin cậy
    
    return {
        "car_model": "Toyota Camry 2023",
        "confidence": 0.985,
        "class_id": 4
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8001)
