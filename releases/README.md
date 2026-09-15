# Release artifacts

Các APK phát hành không được commit trực tiếp vào lịch sử Git để giữ repository gọn và dễ clone. APK Turbo stable 1.1.4 được đính kèm trong [GitHub Release v1.1.4](https://github.com/huongdino443/PhoneME-Turbo/releases/tag/v1.1.4), kèm SHA-256 trong `README.md` và `CHANGELOG.md`.

| Bản | File | SHA-256 |
|---|---|---|
| PhoneME-Turbo | `PhoneME-Turbo-1.1.4.apk` | `d5fc5b06bc74727537b33fc3ee446f002dce2f43d56c197f6d05b1e0a210424e` |
| PhoneME-Turbo(nHD) | `PhoneME-Turbo-nHD-1.1.2.apk` | `51e60854b35955e0ce30bbd4e2cfd699c7da575b858127cd7f966075ec5d9aec` |

Bản Turbo 1.1.4 dùng release certificate ổn định và quy trình ký v1/v2/v3 đã kiểm tra trên Android 2.3. Không đặt keystore hoặc mật khẩu ký APK trong thư mục này. Nếu tự build lại, hãy dùng keystore riêng và không commit nó.
