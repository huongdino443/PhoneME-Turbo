# Changelog

## [1.1.0] — PhoneME-Turbo stable

### Tóm tắt

Bản 1.1.0 là bản nâng cấp stable bắt đầu từ APK PhoneME-MOD sơ khai `be.preuveneers.phoneme.fpmidp` do người dùng cung cấp làm nền tham chiếu chung. Từ nền đó, dự án được phát triển thành hai hướng: HEAP32M cho Turbo thường và HEAP64M cho bản nHD. Tên hiển thị của dự án và bản Turbo thường là **PhoneME-Turbo**; bản nHD giữ tên phân biệt **PhoneME-Turbo(nHD)** trong tài liệu và tên file phát hành.

### Nền tham chiếu và quan hệ các nhánh

APK sơ khai được dùng làm nền đối chiếu có package `be.preuveneers.phoneme.fpmidp`, version `1.0.0`, `minSdkVersion 8`, `targetSdkVersion 8`, SHA-256 `1d02bc4de2730a7255c49bddd3f9d784c7dc52d4795840c7e1dcc401e739a185`. Từ nền này, hướng HEAP32M và hướng HEAP64M được phát triển song song theo mục tiêu thiết bị khác nhau.

### Thay đổi dùng chung

Danh sách game được chuyển sang giao diện lưới, gồm bố cục 3 cột dọc và 4 cột ngang. Game cài sau được đưa lên đầu danh sách. Trình cài hỗ trợ chọn file `.jar` trực tiếp, không yêu cầu file `.jad` đi kèm. Ô nhập đường dẫn được giới hạn một dòng để tránh xuống dòng ngoài ý muốn.

Bàn phím ảo SIP được bật mặc định bằng `cbSIP=true`. Lớp xử lý input được gia cố cho SIP, bàn phím vật lý, Shift/Alt, Telex, xóa và xuống dòng. Native Unicode bridge dựa trên nhánh InputFix7 được tích hợp để các ký tự Unicode BMP tiếng Việt đi qua CVM theo giao thức key event nội bộ của PhoneME.

Logging được tiết chế: bản thường không tự ghi một lượng lớn log nền; phần ghi log chẩn đoán chỉ hoạt động khi chế độ debug phù hợp được bật. Các guard vòng đời được giữ ở mức hẹp để giảm rủi ro khi surface hoặc input connection chưa sẵn sàng.

### PhoneME-Turbo

Bản Turbo thường sử dụng hướng nền HEAP32M phát triển từ APK sơ khai chung, duy trì `minSdkVersion 8` và `targetSdkVersion 8` nhằm giữ khả năng tương thích với Android cũ. Font game của nhánh này được thu nhỏ khoảng 66% để bố cục gọn hơn. Pipeline audio ổn định cùng các thay đổi input/Unicode đã được giữ trong bản stable sau quá trình kiểm thử.

### PhoneME-Turbo(nHD)

Bản Turbo(nHD) sử dụng hướng nền HEAP64M phát triển từ APK sơ khai chung. Bản này nhắm tới màn hình 360×640/nHD và Android mới hơn với `minSdkVersion 18`, `targetSdkVersion 22`, đồng thời có lớp OpenGL/co giãn hình ảnh nhằm hiển thị tốt hơn trên màn hình độ phân giải cao và ưu tiên đường font hệ thống ở nhánh nHD.

### Biến thể NetworkKeep

Hai APK NetworkKeep được xây dựng từ hai bản `cbSIP` stable tương ứng. `PhoneMEMonitorService` được bổ sung `PARTIAL_WAKE_LOCK` để giữ tiến trình/CVM tiếp tục hoạt động khi Activity bị đưa xuống nền; khi thiết bị dùng Wi‑Fi, service đồng thời giữ `WifiLock`. Lock được tạo khi monitor service bắt đầu và được kiểm tra/release an toàn trong `onDestroy`.

Manifest của biến thể này thêm `WAKE_LOCK`, `ACCESS_WIFI_STATE` và `CHANGE_WIFI_STATE`. Bản vá không nâng minSdk/targetSdk và không thay đổi package, giao diện, audio hay native Unicode bridge. Người dùng đã kiểm thử bản Turbo thường trong tình huống chơi game online, đưa ứng dụng xuống nền bằng đa nhiệm rồi quay lại, và xác nhận kết nối vẫn được giữ tốt. Android đời cao vẫn có thể cắt mạng do tối ưu pin, giới hạn dữ liệu nền, timeout của game hoặc máy chủ.

### SHA-256

| File | SHA-256 |
|---|---|
| `PhoneME-Turbo-cbSIP.apk` | `428d12b58ab0c30b382e84c38147022ed0b9b40ad03ccfd7a0f9f8ded21b96f8` |
| `PhoneME-Turbo-nHD-cbSIP.apk` | `3182c6c01fb944e5edfe32dd7d42e65ed5f7a65b7a759dfb8989dbb726815427` |
| `PhoneME-Turbo-NetworkKeep.apk` | `aa42e5979b5bb7ce75d51a131b3888311b0c26b91f57cfeb3219078a83d260cb` |
| `PhoneME-Turbo-nHD-NetworkKeep.apk` | `fd1a2fb7d83731970a226d2456f1aefba47840569e244882ace3861bd67cdd22` |

### Lưu ý

Bản phát hành không tuyên bố mọi game đều có cùng hành vi âm thanh hoặc reconnect. Một số game có cách loop âm thanh riêng và có thể khác nhau theo thiết bị. Người dùng nên thử bản stable thông thường trước, sau đó mới thử biến thể NetworkKeep nếu nhu cầu đa nhiệm mạng là quan trọng.

[1.1.0]: https://github.com/huongdino443/PhoneME-Turbo/releases/tag/v1.1.0 "PhoneME-Turbo 1.1.0"
