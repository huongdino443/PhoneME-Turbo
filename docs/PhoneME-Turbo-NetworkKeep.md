# PhoneME-Turbo NetworkKeep

## Phạm vi

Hai APK thử nghiệm được tạo từ các bản `PhoneME-Turbo-cbSIP.apk` và `PhoneME-Turbo-nHD-cbSIP.apk`. Bản vá không thay đổi native Unicode bridge, giao diện, audio, font, package name, version code hoặc target SDK.

## Thay đổi

`PhoneMEMonitorService` được bổ sung một `PARTIAL_WAKE_LOCK` để giữ tiến trình/CVM tiếp tục chạy khi Activity bị đưa xuống nền. Khi thiết bị dùng Wi‑Fi, service đồng thời giữ một `WifiLock` chế độ tương thích Android cũ. Hai lock được tạo khi monitor service bắt đầu chạy trong phiên game và được kiểm tra, release an toàn trong `onDestroy` để không giữ CPU hoặc Wi‑Fi sau khi thoát game.

Manifest được bổ sung ba permission cần thiết: `WAKE_LOCK`, `ACCESS_WIFI_STATE` và `CHANGE_WIFI_STATE`. Không sử dụng API `WIFI_MODE_FULL_HIGH_PERF`, nhằm giữ khả năng biên dịch/chạy với nhánh Android cũ.

## Kiểm tra tĩnh

Cả hai APK đã được build, zipalign và ký hợp lệ bằng APK Signature Scheme v1, v2 và v3. Package vẫn là `be.preuveneers.phoneme.fpmidp`; label vẫn là `PhoneME-Turbo`.

| APK | minSdk | targetSdk | SHA-256 |
|---|---:|---:|---|
| `PhoneME-Turbo-NetworkKeep.apk` | 8 | 8 | `aa42e5979b5bb7ce75d51a131b3888311b0c26b91f57cfeb3219078a83d260cb` |
| `PhoneME-Turbo-nHD-NetworkKeep.apk` | 18 | 22 | `fd1a2fb7d83731970a226d2456f1aefba47840569e244882ace3861bd67cdd22` |

## Cách test

Mở một game online, đăng nhập hoặc vào trận, đưa ứng dụng xuống nền bằng nút đa nhiệm trong khoảng 30–60 giây, mở một ứng dụng khác rồi quay lại PhoneME-Turbo. Kiểm tra xem game còn giữ phiên mạng hay có thể tiếp tục mà không phải đăng nhập lại. Nên thử riêng trên Wi‑Fi và dữ liệu di động.

## Kết quả kiểm thử thực tế

Người dùng đã kiểm thử bản **PhoneME-Turbo-NetworkKeep** và xác nhận kết quả hoạt động tốt: sau khi đưa game xuống nền bằng đa nhiệm rồi quay lại, kết nối mạng của game vẫn được giữ. Bản vá không gây lỗi quan sát được trên bản Turbo thường.

Trên Android gốc, bản vá vẫn giữ nguyên khả năng tương thích của nhánh Turbo vì không nâng `minSdkVersion`, không nâng `targetSdkVersion` và chỉ sử dụng các API khóa nguồn có từ các phiên bản Android cũ. Tác động phụ dự kiến chỉ là mức tiêu thụ pin cao hơn trong lúc game online đang chạy; ngoài thời gian đó các lock được giải phóng.

Đây là bản vá giữ process/CVM và Wi‑Fi ở mức ứng dụng. Android đời cao vẫn có thể cắt mạng do chế độ tiết kiệm pin, giới hạn dữ liệu nền, game tự timeout hoặc máy chủ đóng phiên; khi đó cần cho phép PhoneME-Turbo chạy nền và tắt tối ưu pin cho ứng dụng. Tính năng reconnect của từng game vẫn do chính game quyết định.
