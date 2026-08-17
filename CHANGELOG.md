# Changelog

## [1.1.0] — PhoneME-Turbo stable

### Tóm tắt

Bản 1.1.0 là bản nâng cấp stable bắt đầu từ APK PhoneME-MOD sơ khai `be.preuveneers.phoneme.fpmidp` do người dùng cung cấp làm nền tham chiếu chung. Từ nền đó, dự án được phát triển thành hai hướng: HEAP32M cho **PhoneME-Turbo** và HEAP64M cho **PhoneME-Turbo(nHD)**.

### Nền tham chiếu và quan hệ các nhánh

APK sơ khai được dùng làm nền đối chiếu có package `be.preuveneers.phoneme.fpmidp`, version `1.0.0`, `minSdkVersion 8`, `targetSdkVersion 8`, SHA-256 `1d02bc4de2730a7255c49bddd3f9d784c7dc52d4795840c7e1dcc401e739a185`. Từ nền này, hướng HEAP32M và hướng HEAP64M được phát triển song song theo mục tiêu thiết bị khác nhau.

### Thay đổi dùng chung

Danh sách game được chuyển sang giao diện lưới, gồm bố cục 3 cột dọc và 4 cột ngang. Game cài sau được đưa lên đầu danh sách. Trình cài hỗ trợ chọn file `.jar` trực tiếp, không yêu cầu file `.jad` đi kèm. Ô nhập đường dẫn được giới hạn một dòng để tránh xuống dòng ngoài ý muốn.

Lớp xử lý input được gia cố cho bàn phím ảo, bàn phím vật lý, Shift/Alt, Telex, xóa và xuống dòng. Native Unicode bridge dựa trên InputFix7 được tích hợp để các ký tự Unicode BMP tiếng Việt đi qua CVM theo giao thức key event nội bộ của PhoneME.

Logging được tiết chế: bản phát hành không tự ghi một lượng lớn log nền; phần ghi log chẩn đoán chỉ hoạt động khi chế độ debug phù hợp được bật. Các guard vòng đời được giữ ở mức hẹp để giảm rủi ro khi surface hoặc input connection chưa sẵn sàng.

### PhoneME-Turbo

Bản thường sử dụng hướng nền HEAP32M phát triển từ APK sơ khai chung, duy trì `minSdkVersion 8` và `targetSdkVersion 8` nhằm giữ khả năng tương thích với Android cũ. Font game của nhánh này được thu nhỏ khoảng 66% để bố cục gọn hơn. Các thay đổi input, Unicode, audio, giao diện và vòng đời đã được giữ trong bản stable sau quá trình kiểm thử.

### PhoneME-Turbo(nHD)

Bản nHD sử dụng hướng nền HEAP64M phát triển từ APK sơ khai chung. Bản này nhắm tới màn hình 360×640/nHD và Android mới hơn với `minSdkVersion 18`, `targetSdkVersion 22`, đồng thời có lớp OpenGL/co giãn hình ảnh nhằm hiển thị tốt hơn trên màn hình độ phân giải cao.

### Tối ưu hoạt động mạng khi đa nhiệm

Hai APK phát hành có thay đổi ở vòng đời dịch vụ để game online có cơ hội duy trì hoạt động mạng tốt hơn khi Activity bị đưa xuống nền. Với thiết bị dùng Wi‑Fi, phần theo dõi kết nối được xử lý thận trọng trong thời gian dịch vụ hoạt động và được giải phóng khi dịch vụ kết thúc. Android đời cao vẫn có thể cắt mạng do tối ưu pin, giới hạn dữ liệu nền, timeout của game hoặc máy chủ.

### SHA-256

| File | SHA-256 |
|---|---|
| `PhoneME-Turbo.apk` | `aa42e5979b5bb7ce75d51a131b3888311b0c26b91f57cfeb3219078a83d260cb` |
| `PhoneME-Turbo-nHD.apk` | `fd1a2fb7d83731970a226d2456f1aefba47840569e244882ace3861bd67cdd22` |

### Lưu ý

Bản phát hành không tuyên bố mọi game đều có cùng hành vi âm thanh hoặc kết nối mạng. Một số game có cách loop âm thanh và cơ chế phiên mạng riêng, có thể cho kết quả khác nhau theo thiết bị. Người dùng nên sao lưu dữ liệu trước khi cài đặt và kiểm tra SHA-256 nếu cần xác minh file tải xuống.

[1.1.0]: https://github.com/huongdino443/PhoneME-Turbo/releases/tag/v1.1.0 "PhoneME-Turbo 1.1.0"
