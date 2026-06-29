# Bí Kíp Sinh Tồn Dành Cho Member 4 (DDM501)

Nếu bạn cảm thấy có quá nhiều thứ đang chạy cùng lúc và hơi "ngợp", đừng lo lắng! Tài liệu này được viết với ngôn ngữ bình dân nhất để giúp bạn hiểu tường tận "mình đang làm gì" chỉ trong 3 phút.

---

## 1. Nhiệm vụ của Bạn thực chất là gì?
Bạn (Member 4) là người nắm giữ **"Mặt tiền" (Giao diện)** và **"Bảo vệ" (Kiểm thử, Giám sát)** của hệ thống. 
Trong toàn bộ đống file của dự án, **BẠN CHỈ CẦN QUAN TÂM ĐẾN ĐÚNG 3 FILE NÀY LÀ ĐỦ:**
1. **`app/ui/main.py`**: Đây là file vẽ ra giao diện tuyệt đẹp mà bạn thấy trên trình duyệt.
2. **`app/ui/api_client.py`**: Đây là file "nhân viên giao hàng". Nó cầm bức ảnh từ giao diện và ném sang cho Backend.
3. **`app/tests/` (Các file Test)**: Đây là các kịch bản kiểm tra xem Code của bạn có bị lỗi không.

> Toàn bộ các file còn lại (Docker, Grafana, Prometheus) tôi đã thiết lập chuẩn xác 100%. Nhiệm vụ của bạn chỉ là BẬT CHÚNG LÊN ĐỂ DÙNG, không cần phải code thêm vào đó.

---

## 2. Luồng chạy của Code (Cái nào Thật, Cái nào Giả lập?)

Hãy hình dung luồng dữ liệu như quá trình bạn đi khám bệnh:

- **Bước 1 (THẬT 100%):** Bệnh nhân (Người dùng) vào phòng tiếp tân `localhost:8501`, nộp ảnh chụp X-Quang xe. (Nhiệm vụ UI của bạn).
- **Bước 2 (THẬT 100%):** Tiếp tân gọi điện thoại (`api_client.py`) gửi ảnh X-Quang sang cho Bác sĩ.
- **Bước 3 (GIẢ LẬP - MOCK):** Bác sĩ ở cổng `localhost:8000` (file `app/gateway/main.py`) nhận được ảnh. Đáng lẽ Bác sĩ phải mang ảnh đi phân tích bằng AI (Node 2 - RTX 5080). Nhưng vì mô hình AI chưa code xong, Bác sĩ **giả vờ suy nghĩ (delay) mất 2 giây**, rồi tự bịa ra một tờ kết quả GIẢ LẬP báo rằng "Đây là lỗi abc, xe Kia Seltos".
- **Bước 4 (THẬT 100%):** Tiếp tân (Giao diện của bạn) nhận được tờ kết quả giả lập kia và hiển thị lên màn hình rất đẹp. 
- **Bước 5 (THẬT 100%):** Camera giám sát (Grafana & Prometheus) luôn đứng trên trần nhà quay lại toàn bộ quá trình trên, bấm giờ xem Bác sĩ suy nghĩ mất bao lâu để vẽ ra biểu đồ.

**Tóm lại:** Chỉ có chức năng "Suy luận AI của Bác sĩ" là **Giả lập (Mock)**. Còn lại toàn bộ Giao diện, Quá trình kết nối mạng, Hệ thống tự động Test (Pytest) và Vẽ biểu đồ đo đạc (Grafana) của bạn đều là **Thật 100%**.

---

## 3. Câu Lệnh Nằm Lòng Khi Bắt Đầu Dự Án
Mỗi ngày mở máy tính lên làm việc, bạn KHÔNG CẦN phải nhớ nhiều lệnh, chỉ cần nhớ 3 thao tác sau:

**BƯỚC 1: Bật toàn bộ hệ thống lên (Start)**
Mở Terminal trong thư mục code và gõ:
```bash
docker-compose up -d
```
*(Chờ 2 giây, sau đó mở trình duyệt `localhost:8501` để làm việc. Khi bạn sửa file `app/ui/main.py`, trình duyệt sẽ tự động cập nhật ngay lập tức).*

**BƯỚC 2: Chạy kiểm thử (Lúc báo cáo Giảng viên)**
Để chứng minh code của mình chuẩn, bạn gõ lệnh chạy Test:
```bash
venv\Scripts\activate
python -m pytest app/tests/ -v
```

**BƯỚC 3: Tắt hệ thống khi làm xong (Stop)**
Để giải phóng RAM cho máy tính khi không code nữa:
```bash
docker-compose down
```
