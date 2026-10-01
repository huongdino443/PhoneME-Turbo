# PhoneME Turbo

**PhoneME Turbo** là một trình giả lập Java ME dành cho Android, cho phép chạy các ứng dụng và trò chơi Java ME thông qua tệp JAD/JAR. Dự án được phát triển mở rộng từ APK PhoneME nguyên thủy do **Davy Preuveneers** phát triển, với mục tiêu cải thiện khả năng tương thích, giao diện, điều khiển và trải nghiệm sử dụng trên nhiều thiết bị Android.

Repository này lưu trữ các bản phát hành, tài liệu kỹ thuật và những thành phần cần thiết để nghiên cứu, đánh giá và tiếp tục phát triển PhoneME Turbo.

> Đây là dự án cộng đồng và các APK được chỉnh sửa/phân phối lại từ PhoneME. Hãy sao lưu dữ liệu trước khi cài, tải file từ nguồn tin cậy và tự chịu trách nhiệm về việc sử dụng trên thiết bị của mình.

## Bản phát hành hiện tại

| Mục | Giá trị |
|---|---|
| Phiên bản | **1.2.1** |
| APK | [`releases/v1.2.1/PhoneME-Turbo-1.2.1.apk`](releases/v1.2.1/PhoneME-Turbo-1.2.1.apk) |
| Version code | `26` |
| Package | `be.preuveneers.phoneme.fpmidp` |
| SHA-256 APK | `f7e692cede497e0118af04f4b840b735cdbdc4b239cdeff13b996cc634973f6f` |
| Certificate SHA-256 | `1C:7E:35:CC:46:1E:96:1C:CA:67:5B:E8:C2:33:05:91:11:D4:75:59:0A:4E:01:55:E3:77:A9:CB:86:6B:A0:17` |

Tài liệu của release nằm trong [`releases/v1.2.1/`](releases/v1.2.1/), gồm APK release-signed, changelog và checksum. Bản unsigned không được phân phối.

## Thay đổi chính trong 1.2.1

- Cập nhật một glyph trong atlas CoreBridge, giữ nguyên kích thước atlas và kênh alpha RGBA.
- Sửa luồng gỡ game an toàn hơn, không xóa RMS hoặc JAR nguồn bên ngoài ứng dụng.
- Cải thiện import JAR, export có xét cache, đường dẫn JAD và URI `file://`.
- Tái sử dụng JAR đã chuẩn hóa hợp lệ và dọn WMA cache khi gỡ game.

Chi tiết nằm trong [`releases/v1.2.1/CHANGELOG.md`](releases/v1.2.1/CHANGELOG.md).

## Nền tảng tính năng của 1.2.0

- Điều khiển riêng theo từng game: gamepad J2ME, key mapping và tùy chọn display/touch/GL/Canvas theo MIDlet.
- EdgeSwipe với Exit, Settings, Virtual Keyboard và Gamepad.
- Bàn phím launcher chạy dạng overlay thay vì làm co vùng nội dung.
- Cải thiện touch pass-through quanh gamepad và vùng ngoài framebuffer.
- Điều chỉnh EdgeSwipe cho màn hình nhỏ và nhiều tỷ lệ hiển thị.
- Xử lý lại layout launcher sau xoay màn hình và giữ runtime/GL theo chính sách hiện có.
- Bổ sung có chọn lọc một số Nokia API shim và xử lý một số class/JAR cũ bằng bản sao suite riêng.
- Cải thiện LCDUI menu nhiều mục, scrolling và giao diện LCDUI dark theme.

Chi tiết song ngữ nằm trong [`releases/v1.2.0/CHANGELOG.md`](releases/v1.2.0/CHANGELOG.md).

Bản phát hành **không tuyên bố** bổ sung tổng quát cho MMAPI music playback, tự động chuyển playlist hoặc M3G rendering.

## Cài đặt và nâng cấp

1. Sao lưu game, RMS và dữ liệu quan trọng.
2. Kiểm tra SHA-256 của APK nếu file được tải qua kênh khác.
3. Nếu Android báo xung đột chữ ký, gỡ bản cũ trước khi cài. Việc gỡ ứng dụng có thể xóa dữ liệu private của app.
4. Bản 1.2.1 sử dụng cùng certificate phát hành với PhoneME Turbo 1.2.0-15; các bản dùng cùng certificate có thể cập nhật trực tiếp cho nhau.
5. Sau khi cài, dùng File Manager trong app để chọn JAR/JAD và kiểm tra quyền truy cập theo Android/thiết bị.

Chữ ký và tính toàn vẹn ZIP của APK 1.2.1 đã được kiểm tra. Việc hiển thị glyph mới trên thiết bị thực tế chưa được kiểm tra trong release này.

## Source và khả năng tái tạo

Bundle source công khai là **APK-level patch/recovery source**, không phải toàn bộ source tree của Turbo CVM. Nó gồm:

- Baseline v340 dùng làm input lịch sử cho release 1.2.0.
- Script đổi version metadata và kiểm tra DEX/payload.
- Các script lineage v337–v340 để review provenance.
- Build notes và source-scope declaration.

Không có trong repository: private signing key, keystore, mật khẩu, full Turbo CVM/native build graph, ROMizer hoàn chỉnh hoặc toàn bộ input lịch sử cần để dựng lại v340 từ đầu. Không nên hiểu các script lineage là một quy trình from-source hoàn chỉnh.

Xem [`releases/v1.2.0/SOURCE/BUILDING.md`](releases/v1.2.0/SOURCE/BUILDING.md) và [`releases/v1.2.0/SOURCE/SOURCE_SCOPE.md`](releases/v1.2.0/SOURCE/SOURCE_SCOPE.md) để đọc tài liệu source/provenance lịch sử.

## Cấu trúc repository

| Đường dẫn | Nội dung |
|---|---|
| `releases/v1.2.1/` | Snapshot phát hành mới nhất: APK release-signed, changelog và checksum. |
| `releases/v1.2.0/` | Snapshot lịch sử: APK, source, notices, checksum và verification. |
| `docs/` | Tài liệu kỹ thuật và các assessment lịch sử cần giữ để tham khảo. |
| `scripts/` | Script patch lịch sử từ các phiên bản trước; không phải release pipeline 1.2.0. |
| `CHANGELOG.md` | Lịch sử phát hành và thay đổi ở mức dự án. |
| `NOTICE.md` | Ghi chú license/provenance ở cấp repository. |

Các file lịch sử ngoài `releases/v1.2.1/` được giữ để provenance; khi cài đặt, ưu tiên artifact 1.2.1.

## Giấy phép và provenance

PhoneME Turbo là một dự án phát triển mở rộng dựa trên PhoneME, phục vụ nghiên cứu và sử dụng cá nhân. PhoneME, Android và các thư viện liên quan vẫn chịu license tương ứng. Đọc [`releases/v1.2.0/NOTICES/`](releases/v1.2.0/NOTICES/) trước khi tái phân phối hoặc sử dụng thương mại.

## Liên kết

- [GitHub Releases](https://github.com/huongdino443/PhoneME-Turbo/releases)
- [PhoneME upstream](https://github.com/magicus/phoneME)
- [Tài liệu kỹ thuật](docs/README.md)
