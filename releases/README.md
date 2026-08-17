# Release artifacts

Các APK phát hành không được commit trực tiếp vào lịch sử Git để giữ repository gọn và dễ clone. Hai file APK cuối được đính kèm trong [GitHub Release v1.1.0](https://github.com/huongdino443/PhoneME-Turbo/releases/tag/v1.1.0), kèm SHA-256 trong `README.md` và `CHANGELOG.md`.

| Bản | File |
|---|---|
| PhoneME-Turbo | `PhoneME-Turbo.apk` |
| PhoneME-Turbo(nHD) | `PhoneME-Turbo-nHD.apk` |

Không đặt keystore hoặc mật khẩu ký APK trong thư mục này. Nếu tự build lại, hãy dùng keystore riêng và không commit nó.
