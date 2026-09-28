# PhoneME-Turbo changelog

## 1.2.0 — bản phát hành chính hiện tại

Bản 1.2.0 là dòng phát hành chính duy nhất hiện tại của repository và được phát triển từ **PhoneME-Turbo nHD 1.1.2** theo lineage v337–v340. Đây không phải là bản trộn binary giữa Turbo thường 1.1.4 và nHD 1.1.2.

### Thay đổi chính

- Điều khiển riêng theo từng game với gamepad J2ME, key mapping và tùy chọn display/touch/GL/Canvas.
- EdgeSwipe có Exit, Settings, Virtual Keyboard và Gamepad.
- Bàn phím launcher hiển thị dạng overlay, không làm co vùng nội dung.
- Cải thiện touch pass-through quanh gamepad và vùng ngoài framebuffer.
- Điều chỉnh EdgeSwipe cho màn hình nhỏ tới nhóm nHD.
- Xử lý lại layout launcher sau xoay màn hình và duy trì runtime/GL theo chính sách của ứng dụng.
- Bổ sung có chọn lọc Nokia API shim và xử lý class/JAR cũ bằng bản sao suite riêng khi cần.
- Cải thiện LCDUI menu nhiều mục, scrolling và dark theme.

APK, source/provenance, checksum và verification nằm tại [`releases/v1.2.0/`](releases/v1.2.0/).

### Giới hạn đã biết

Bản 1.2.0 không tuyên bố bổ sung tổng quát cho MMAPI music playback, tự động chuyển playlist hoặc M3G rendering. Hành vi game vẫn có thể khác theo thiết bị, Android version, native capability và server của game.

## 1.1.4 — mốc cuối của dòng Turbo thường/HEAP32M

1.1.4 là mốc stable cuối của dòng HEAP32M/PhoneME-Turbo đời thấp. Dòng này dừng tại 1.1.4; không được hiểu là nền trực tiếp của binary v1.2.0.

Các cải tiến lịch sử gồm giao diện LCDUI dark theme, File Manager tích hợp, Unicode tiếng Việt, native input bridge và các thay đổi lifecycle/network được ghi trong Git history và tài liệu cũ.

## 1.1.2 — mốc lineage trực tiếp của v1.2.0

PhoneME-Turbo nHD 1.1.2 là điểm phát triển trực tiếp của lineage v337–v340 và bản phát hành 1.2.0. Các patch về giao diện, EdgeSwipe, gamepad, lifecycle, Nokia compatibility và layout nHD được tiếp tục xử lý trên dòng này.

## Các mốc cũ

- `v1.1.3`: phát hành tiếp nối với quy trình ký tương thích legacy.
- `v1.1.0`: mốc nền trước các thay đổi phát hành sau đó.

Các artifact cũ được giữ trong Git history và tài liệu lịch sử để đối chiếu. Khi cần cài đặt hoặc tiếp tục phát triển, ưu tiên bundle `releases/v1.2.0/`.
