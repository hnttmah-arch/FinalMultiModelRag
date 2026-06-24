import os
import requests
import sys

# Cấu hình stdout sử dụng UTF-8 để hỗ trợ in ký tự Tiếng Việt trên Windows console
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def run_test():
    url = "http://localhost:8000/api/query"
    print(f"[TEST] Bat dau gui request kiem thu toi API Gateway tai: {url}")
    
    # 1. Tao file anh gia lap (dummy image) de gui kem request
    dummy_image_path = "temp_test_car.jpg"
    with open(dummy_image_path, "wb") as f:
        # Ghi mot so bytes gia dinh cau truc JPG co ban
        f.write(b"\xFF\xD8\xFF" + b"\x00" * 97) 
        
    # 2. Tao file am thanh gia lap (dummy audio WAV)
    dummy_voice_path = "temp_test_voice.wav"
    with open(dummy_voice_path, "wb") as f:
        f.write(b"RIFF" + b"\x00" * 36 + b"WAVEfmt " + b"\x00" * 18 + b"data" + b"\x00" * 4)

    try:
        # Chuan bi file gui len dang multipart/form-data
        files = {
            "image": ("test_car.jpg", open(dummy_image_path, "rb"), "image/jpeg"),
            "voice_file": ("test_voice.wav", open(dummy_voice_path, "rb"), "audio/wav")
        }
        
        # Gui them truong query_text
        data = {
            "query_text": "Lam sao de thay cau chi tau sac xe Toyota Camry 2023?"
        }
        
        print("[SEND] Dang gui yeu cau (bao gom anh xe, file ghi am)...")
        response = requests.post(url, files=files, data=data)
        
        print(f"[RECEIVE] Ma trang thai phan hoi (HTTP Status): {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print("\n================= KET QUA TRA VE =================")
            print(f"- Trang thai: {result.get('status')}")
            print(f"- Dong xe nhan dang: {result.get('car_model')} (Do tin cay: {result.get('confidence')*100:.1f}%)")
            print(f"- Cau hoi (da convert/nhan duoc): {result.get('query')}")
            print(f"- Cau tra loi tu AI (VLM): \n{result.get('answer')}")
            print(f"- So do dinh kem tim thay: {result.get('retrieved_diagrams')}")
            print("==================================================\n")
        else:
            print(f"[ERROR] Loi phan hoi tu Gateway: {response.text}")
            
    except Exception as e:
        print(f"[ERROR] Loi ket noi toi Gateway: {e}")
        print("[INFO] Hay dam bao rang ban da khoi chay API Gateway truoc khi chay script test nay (vi du: python main.py).")
    finally:
        # Dong cac file dang mo truoc khi xoa
        for key in files:
            files[key][1].close()
        # Don dep cac file tam
        if os.path.exists(dummy_image_path):
            os.remove(dummy_image_path)
        if os.path.exists(dummy_voice_path):
            os.remove(dummy_voice_path)

if __name__ == "__main__":
    run_test()
