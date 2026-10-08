# Tài liệu kỹ thuật

Thư mục này chứa các báo cáo kỹ thuật và provenance của PhoneME Turbo. Bản phát hành hiện tại là **PhoneME Turbo 1.2.2**, gồm biến thể tiêu chuẩn và biến thể tương thích API 8. Bản 1.2.0 là mốc nền lịch sử được phát triển từ dòng 1.1.2 qua các mốc v337–v340. Các tài liệu cũ có thể còn dùng tên nHD/HEAP64M để mô tả baseline, nhưng đó không phải tên sản phẩm hiện tại.

## Báo cáo chính

- [Đối chiếu v1.2.0 với 1.1.2](V1.2.0-VS-1.1.2-AUDIT.md)
- [Đánh giá khả năng dùng source phoneME Sun cho tương thích Turbo](PhoneME-Sun-Turbo-general-compatibility.md)
- [Native Unicode/InputFix7](PhoneME-InputFix7-NativeUnicode.md)
- [Tài liệu tương thích lịch sử](PhoneME-Turbo-compatibility.md)

Các offset native chỉ áp dụng cho đúng nền ELF đã kiểm tra. Không áp dụng trực tiếp lên APK khác nếu chưa xác minh chunk, branch site và vùng helper. Repository không chứa full Turbo CVM/native build tree hoặc private signing key.
