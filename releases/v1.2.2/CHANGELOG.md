# PhoneME Turbo 1.2.2

## Thay đổi so với 1.2.1

### Chung

- **FPS trên GL/HD:** bổ sung công tắc FPS và cập nhật bộ đếm tại điểm gửi khung hình lên GL.
- **Nhãn FPS theo dp:** hiển thị badge 8dp trên lớp Android phía trên GL, co giãn theo mật độ màn hình.
- **Giữ đường Canvas cũ:** thiết bị dùng đường Canvas tiếp tục cách vẽ FPS hiện có; thay đổi badge GL được cô lập.
- **Điều khiển game:** tích hợp chế độ kích thước thật đồng bộ hình ảnh và vùng chạm, cùng ba bố cục gamepad.
- **Cài đặt gọn cho game:** giữ tùy chọn bitmap font và ẩn các hàng cài đặt monitor/camera.

### Bản API 8

- Bổ sung APK riêng cho thiết bị Android API 8 / Android 2.2.
- Ẩn title bar riêng của `PhoneMEActivity` trước khi tạo giao diện, giữ nguyên status bar và theme mặc định của thiết bị.
- Sử dụng `Activity.requestWindowFeature(FEATURE_NO_TITLE)`, API có từ Android API 1, không thêm thư viện hoặc API mới.
- Giữ nguyên các màn hình duyệt file, cài đặt, game và payload còn lại ngoài phần thay đổi cần thiết.
- Tiếp tục các cải tiến bố cục Game Settings và thanh Canvas scale của nhánh API 8.

## Thông tin build

- Bản tiêu chuẩn: version name `1.2.2`, version code `27`, minimum SDK `18`, target SDK `22`.
- Bản API 8: version name `1.2.2-api8`, version code `44`, minimum SDK `8`, target SDK `22`.
- Cả hai APK sử dụng native ABI `armeabi` và certificate release PhoneME Turbo hiện có.
- Chỉ phân phối APK release-signed; không phát hành bản unsigned.
