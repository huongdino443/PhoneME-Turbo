# Kỹ thuật

Thư mục này chứa các báo cáo về phạm vi patch, input Unicode, vòng đời ứng dụng và kiểm tra đầu ra của hai APK PhoneME-Turbo phát hành cuối. Báo cáo mô tả các thay đổi ở mức có thể tái hiện, nhưng không chứa keystore, mật khẩu, log cá nhân hoặc toàn bộ cây giải mã PhoneME.

Các offset native chỉ áp dụng cho đúng nền ELF đã kiểm tra trong dự án. Không nên áp dụng trực tiếp lên một APK khác nếu chưa xác minh kích thước chunk, branch site và vùng helper.

## Báo cáo tương thích

- [Đánh giá khả năng dùng source phoneME Sun để mở rộng tương thích Turbo](PhoneME-Sun-Turbo-general-compatibility.md)
- SHA-256: `b6e40c3bdcf13c90d1f877fb6acf513c3f049de5ae6815b8e2961ee35960e72d`
