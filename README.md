# PhoneME Turbo

**PhoneME Turbo** là một trình giả lập Java ME dành cho Android, cho phép chạy các ứng dụng và trò chơi Java ME thông qua tệp JAD/JAR. Dự án được phát triển mở rộng từ một biến thể APK **PhoneME Advanced** nguyên thủy do **Davy Preuveneers** phát triển, với mục tiêu cải thiện khả năng tương thích game, giao diện, điều khiển và trải nghiệm sử dụng trên nhiều thiết bị Android.

Repository này lưu trữ các bản phát hành, tài liệu kỹ thuật và những thành phần cần thiết để nghiên cứu, đánh giá và tiếp tục phát triển PhoneME Turbo.

> Đây là dự án cộng đồng và các APK được chỉnh sửa/phân phối lại từ PhoneME. Hãy sao lưu dữ liệu trước khi cài, tải file từ nguồn tin cậy và tự chịu trách nhiệm về việc sử dụng trên thiết bị của mình.

## PhoneME Converter — xử lý lỗi VerifyError

Nếu game Java ME không khởi động trên PhoneME Turbo và log xuất hiện `VerifyError`, `bad typematch`, lỗi StackMap hoặc lỗi xác minh class tương tự, bạn có thể thử [PhoneME Converter](https://huongdino443.github.io/PhoneME-Turbo/tools/phoneme-converter/). Đây là công cụ chuẩn hóa và kiểm tra JAR chạy trực tiếp trong trình duyệt; JAR được xử lý cục bộ và không được tải lên máy chủ.

Đây **không phải bước bắt buộc cho mọi game** và không sửa được mọi lỗi runtime, lỗi API còn thiếu, lỗi mạng hoặc lỗi logic riêng của game. Công cụ chỉ nhận file `.jar` tối đa 64 MB, không nhận `.jad` hay APK. Hãy giữ lại JAR gốc, đọc báo cáo JSON và kiểm tra kết quả trước khi cài. Nếu JAR đã ký bị thay đổi, chữ ký cũ sẽ không còn khớp.

Đọc thêm [hướng dẫn và giới hạn của PhoneME Converter](tools/phoneme-converter/README.md) trước khi sử dụng.

## Bản phát hành hiện tại

**PhoneME Turbo 1.2.5** được phát hành với hai APK cùng dòng phiên bản:

| Biến thể | APK | Version code | Minimum SDK | SHA-256 |
|---|---|---:|---:|---|
| Tiêu chuẩn | [`PhoneME-Turbo-1.2.5.apk`](releases/v1.2.5/PhoneME-Turbo-1.2.5.apk) | `34` | `18` | `dba81bc1822f0d387ae12b583f263f2e2a1e499b12afdaa94ae2703586e1a29f` |
| API 8 | [`PhoneME-Turbo-1.2.5-api8.apk`](releases/v1.2.5/PhoneME-Turbo-1.2.5-api8.apk) | `48` | `8` | `bfb61991f500b35d27f61a79b0c8929b00fd35e2eb764f66192399751bb76a6e` |

Cả hai APK dùng package `be.preuveneers.phoneme.fpmidp`, target SDK `22`, native ABI `armeabi` và cùng certificate phát hành PhoneME Turbo. Tài liệu release nằm trong [`releases/v1.2.5/`](releases/v1.2.5/). Bản unsigned không được phân phối.

## Thay đổi chính trong 1.2.5

- Bổ sung Mẫu 4 (Joystick) và hỗ trợ joystick cho mẫu gamepad tùy chỉnh; chỉnh sửa mẫu đã lưu cập nhật đúng mẫu thay vì tạo bản trùng, đồng thời giữ bố cục riêng cho màn hình dọc/ngang.
- Khắc phục VolumeControl và cải thiện điều khiển âm thanh khi phát lại; âm thanh có thể chưa hoạt động đầy đủ trên Android 2.3–4.0.
- Thêm nút chuyển nhanh giữa sắp xếp file theo tên và theo thời gian mới nhất trong File Manager.
- Chuyển cách vẽ bitmap font sang native.
- Thêm tùy chọn khóa hướng xoay hiện tại và áp dụng lựa chọn khi chuyển màn hình trong ứng dụng.

Chi tiết nằm trong [`releases/v1.2.5/CHANGELOG.md`](releases/v1.2.5/CHANGELOG.md).

Các thay đổi của các phiên bản trước được lưu trong từng trang [GitHub Releases](https://github.com/huongdino443/PhoneME-Turbo/releases).

## Cài đặt và nâng cấp

1. Sao lưu game, RMS và dữ liệu quan trọng.
2. Kiểm tra SHA-256 của APK nếu file được tải qua kênh khác.
3. Nếu Android báo xung đột chữ ký, gỡ bản cũ trước khi cài. Việc gỡ ứng dụng có thể xóa dữ liệu private của app.
4. Hai APK 1.2.5 sử dụng cùng certificate phát hành PhoneME Turbo; hãy chọn biến thể phù hợp với API Android của thiết bị.
5. Sau khi cài, dùng File Manager trong app để chọn JAR/JAD và kiểm tra quyền truy cập theo Android/thiết bị.

Chữ ký và checksum của cả hai APK 1.2.5 đã được kiểm tra. Bản API 8 giữ minimum SDK 8 để hỗ trợ Android 2.2.

## Source và khả năng tái tạo

Bundle source công khai là **APK-level patch/recovery source**, không phải toàn bộ source tree của Turbo CVM. Nó gồm:

- Baseline v340 dùng làm input lịch sử cho release 1.2.0.
- Script đổi version metadata và kiểm tra DEX/payload.
- Các script lineage v337–v340 để review provenance.
- Build notes và source-scope declaration.

Không có trong repository: private signing key, keystore, mật khẩu, full Turbo CVM/native build graph, ROMizer hoàn chỉnh hoặc toàn bộ input lịch sử cần để dựng lại v340 từ đầu. Không nên hiểu các script lineage là một quy trình from-source hoàn chỉnh.

Xem [`releases/v1.2.0/SOURCE/BUILDING.md`](releases/v1.2.0/SOURCE/BUILDING.md) và [`releases/v1.2.0/SOURCE/SOURCE_SCOPE.md`](releases/v1.2.0/SOURCE/SOURCE_SCOPE.md) để đọc tài liệu source/provenance lịch sử.

## Công cụ APK cho cộng đồng

Đã bổ sung một bộ nhỏ các công cụ APK-level có thể dùng lại: căn chỉnh APK, ký APK thử bằng chứng thư tạm và patch JSR-135 có kiểm tra cấu trúc bytecode. Bộ này không phải source tree đầy đủ và không kèm khóa ký. Xem hướng dẫn, phạm vi áp dụng và lưu ý license tại [tools/apk-patch-kit/](tools/apk-patch-kit/README.md).

## Cấu trúc repository

| Đường dẫn | Nội dung |
|---|---|
| `releases/v1.2.5/` | Snapshot phát hành mới nhất: hai APK release-signed, changelog và checksum. |
| `releases/v1.2.4/` | Snapshot lịch sử: hai APK release-signed, changelog và checksum. |
| `releases/v1.2.3/` | Snapshot lịch sử: hai APK release-signed, changelog và checksum. |
| `releases/v1.2.2/` | Snapshot lịch sử: hai APK release-signed, changelog và checksum. |
| `releases/v1.2.0/` | Snapshot lịch sử: APK, source, notices, checksum và verification. |
| `docs/` | Tài liệu kỹ thuật và các assessment lịch sử cần giữ để tham khảo. |
| `tools/phoneme-converter/` | Công cụ web độc lập để kiểm tra và chuẩn hóa JAR Java ME gặp lỗi xác minh trên PhoneME Turbo. |
| `scripts/` | Script patch lịch sử từ các phiên bản trước; không phải release pipeline 1.2.0. |
| `CHANGELOG.md` | Lịch sử phát hành và thay đổi ở mức dự án. |
| `NOTICE.md` | Ghi chú license/provenance ở cấp repository. |

Các file lịch sử ngoài `releases/v1.2.2/` được giữ để provenance; khi cài đặt, ưu tiên biến thể 1.2.5 phù hợp với thiết bị.

## Giấy phép và provenance

PhoneME Turbo là một dự án phát triển mở rộng dựa trên PhoneME, phục vụ nghiên cứu và sử dụng cá nhân. PhoneME, Android và các thư viện liên quan vẫn chịu license tương ứng. Đọc [`releases/v1.2.0/NOTICES/`](releases/v1.2.0/NOTICES/) trước khi tái phân phối hoặc sử dụng thương mại.

## Liên kết

- [GitHub Releases](https://github.com/huongdino443/PhoneME-Turbo/releases)
- [PhoneME upstream](https://github.com/magicus/phoneME)
- [Tài liệu kỹ thuật](docs/README.md)
