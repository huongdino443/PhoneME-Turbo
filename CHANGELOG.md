# PhoneME Turbo changelog

## 1.2.2 — bản phát hành hiện tại

PhoneME Turbo 1.2.2 gồm bản tiêu chuẩn cho Android API 18 trở lên và bản API 8 dành cho Android 2.2 trở lên.

### Thay đổi chính

- Thêm công tắc FPS và bộ đếm frame tại điểm gửi khung hình lên GL/HD.
- Thêm badge FPS 8dp trên lớp Android phía trên GL, co giãn theo mật độ màn hình.
- Giữ nguyên đường Canvas cũ và cách vẽ FPS hiện có trên thiết bị dùng Canvas.
- Tích hợp kích thước thật theo từng game, đồng bộ hình ảnh/vùng chạm và ba bố cục gamepad.
- Giữ bitmap-font preference và ẩn các hàng cài đặt monitor/camera không cần cho game.
- Bổ sung biến thể API 8 / Android 2.2 với xử lý title bar tương thích API thấp.

Chi tiết và checksum nằm tại [`releases/v1.2.2/`](releases/v1.2.2/).

## 1.2.1 — bản cập nhật trước đó

PhoneME Turbo 1.2.1 tiếp tục phát triển từ bản 1.2.0, tập trung vào xử lý bitmap font, gỡ game, import JAR và quản lý cache.

### Thay đổi chính

- Cập nhật một glyph trong atlas CoreBridge, giữ nguyên kích thước atlas và kênh alpha RGBA.
- Sửa luồng gỡ game để chỉ dọn dữ liệu thuộc game được chọn, không xóa RMS hoặc JAR nguồn bên ngoài ứng dụng.
- Sửa lỗi crash trong quá trình dọn dẹp game.
- Hỗ trợ import JAR nguồn và export có xét đến bản cache.
- Cải thiện xử lý đường dẫn JAD và URI `file://`.
- Tái sử dụng JAR đã chuẩn hóa khi hợp lệ và kiểm tra cache sau bước chuẩn hóa EXIF.
- Dọn cả WMA cache phát sinh từ JAR đã chuẩn hóa EXIF khi gỡ game.

APK, changelog và checksum nằm tại [`releases/v1.2.1/`](releases/v1.2.1/).

## 1.2.0

Bản 1.2.0 là dòng phát hành chính được phát triển từ **PhoneME Turbo 1.1.2** theo lineage v337–v340. Các thay đổi lớn gồm canvas theo từng game, FrameBuffer/touch routing, EdgeSwipe, gamepad, keyboard overlay, lifecycle Android, Nokia/WMA compatibility bridge, JAR processing và giao diện LCDUI dark theme.

Chi tiết nằm tại [`releases/v1.2.0/CHANGELOG.md`](releases/v1.2.0/CHANGELOG.md).

## 1.1.4 — mốc cuối của dòng Turbo thường/HEAP32M

1.1.4 là mốc stable cuối của dòng HEAP32M/PhoneME Turbo đời thấp. Dòng này dừng tại 1.1.4 và được giữ trong lịch sử để đối chiếu.

## 1.1.2 — mốc lineage của v1.2.x

PhoneME Turbo 1.1.2 là điểm phát triển trực tiếp của lineage v337–v340 và các bản 1.2.0, 1.2.1.

## Các mốc cũ

- `v1.1.3`: phát hành tiếp nối với quy trình ký tương thích legacy.
- `v1.1.0`: mốc nền trước các thay đổi phát hành sau đó.

Các artifact cũ được giữ trong Git history và tài liệu lịch sử để đối chiếu. Khi cài đặt hoặc tiếp tục phát triển, ưu tiên bản phát hành mới nhất trong [`releases/`](releases/).
