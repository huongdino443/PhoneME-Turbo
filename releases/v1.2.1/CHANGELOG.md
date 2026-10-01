# PhoneME Turbo 1.2.1

## Thay đổi so với 1.2.0

### Tiếng Việt

- **Bitmap font:** cập nhật một glyph trong atlas CoreBridge theo bản vẽ mới, giữ nguyên kích thước atlas và kênh alpha RGBA.
- **Gỡ game an toàn hơn:** chỉ dọn dữ liệu thuộc game được chọn; không xóa RMS hoặc JAR nguồn bên ngoài ứng dụng. Sửa lỗi crash trong luồng dọn dẹp.
- **Import JAR trực tiếp:** hỗ trợ import JAR nguồn và export có xét đến bản cache; sửa xử lý đường dẫn JAD và URI `file://`.
- **Khởi chạy và cache WMA:** tái sử dụng JAR đã chuẩn hóa khi hợp lệ, kiểm tra cache sau bước chuẩn hóa EXIF và rút ngắn đường khởi chạy lại.
- **Dọn cache khi gỡ game:** bao gồm cache WMA phát sinh từ JAR đã chuẩn hóa EXIF, tránh để lại cache của game đã gỡ.

### English

- **Bitmap font:** updates one glyph in the CoreBridge atlas while preserving the atlas dimensions and RGBA alpha channel.
- **Safer game uninstall:** removes only data owned by the selected game; RMS and external source JARs remain untouched. Fixes a crash in the cleanup flow.
- **Direct JAR import:** supports importing source JARs and cache-aware export; fixes JAD path handling and `file://` URI launches.
- **Launch and WMA caching:** reuses validated normalized JARs, checks the cache after EXIF normalization, and speeds up repeat launches.
- **Uninstall cache cleanup:** also removes WMA caches derived from EXIF-normalized JARs so removed games do not leave those cache files behind.

## Thông tin build

- Version name: `1.2.1`
- Android version code: `26`
- APK release-signed sử dụng cùng certificate PhoneME Turbo với bản `1.2.0-15`.
- Bản public chỉ phân phối APK release-signed; không đưa bản unsigned vào repository hoặc GitHub Release.
- Chữ ký APK và package contents đã được kiểm tra. Việc kiểm tra hiển thị glyph trên thiết bị thực tế chưa được thực hiện trong release này.
