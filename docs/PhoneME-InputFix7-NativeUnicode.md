# PhoneME InputFix7 Native Unicode v13

## Kết quả thực hiện

Bản v13 được xây dựng từ `PhoneME-GridJar-Prepend-Font66-UI-Integrated-v2.apk`, là baseline đã chạy ổn định trên Android 2.3/4.4 và Vivo. Baseline này thuộc chuỗi phát triển bắt đầu từ APK PhoneME sơ khai chung `be.preuveneers.phoneme.fpmidp`, sau đó được tổ chức theo các hướng HEAP32M và HEAP64M. Khác với các bản v8–v12 trước đó, bản này không ép `Typeface`, không ánh xạ ký tự sang Latin-1, không sửa `keyboardEvent` theo UTF-8 và không thay toàn bộ native library.

Bản vá phục hồi native bridge từ chuỗi InputFix7 của nền PhoneME tương ứng thuộc hướng HEAP64M/nHD. Giao thức keyboard của PhoneME không phải UTF-8: Java gửi hai byte của giá trị 16-bit trong sự kiện key-down, sau đó gửi sự kiện key-up đặc biệt kèm hai byte giá trị đó. Vấn đề nằm ở nhánh native xử lý keycode không có mapping. Nhánh cũ có sentinel mapping không ghi được; native bridge lịch sử tạo một `KeyMapping` tạm trong vùng BSS có thể ghi, đặt codepoint Unicode BMP cùng raw key-down/key-up rồi quay lại common path. Vì vậy các codepoint như U+0103, U+0111, U+01B0 và U+1EA1 không bị loại bỏ trước khi vào CVM.

## Phạm vi thay đổi

Chỉ hai entry native được thay đổi:

| Entry | Thay đổi |
|---|---|
| `assets/foundation/bin/libcvm.so.2` | Thay branch tại offset `0x2a80a4` để gọi helper Unicode |
| `assets/foundation/bin/libcvm.so.4` | Đặt helper 40 byte tại vùng executable zero-fill offset `0x468c14` |

Các thành phần sau được giữ nguyên từ v2: `libjniphoneme.so`, các chunk CVM còn lại, Java/smali InputFix63, pipeline audio đã được kiểm thử ổn định, bitmap assets, manifest, Grid 3/4 cột, JAR-only, prepend và hệ số font 66%.

Branch gốc tại `0x2a80a4` là `0c 00 00 ea`; branch sau vá là `da 02 07 ea`. Helper dùng vùng scratch writable tại `0x6d9da0`, theo đúng bố cục ELF của nền `InputFix7-nativeUnicodeTextCave` thuộc hướng HEAP64M. Script build từ chối chạy nếu nền ELF không đúng branch hoặc vùng helper không còn zero-filled, nhằm tránh ghi nhầm native code.

## Xác minh đóng gói và chữ ký

APK đầu ra đã được zipalign, ký lại bằng keystore dự án và kiểm tra bằng `apksigner`. Kết quả xác minh: chữ ký v1, v2 và v3 đều hợp lệ. Lỗi “gói có vẻ không hợp lệ” của v12 đã được xử lý; v12 trước đó bị bàn giao nhầm file aligned chưa ký.

| Mục | Giá trị |
|---|---|
| APK | `PhoneME-GridJar-Prepend-Font66-UI-Integrated-InputFix7-NativeUnicode-v13.apk` |
| SHA-256 | `9012db9b0028e57e40cd5a2a3194a277c21749c0160263f5e7a5538c392cf08f` |
| Kích thước | 4,103,569 bytes |
| Native entries thay đổi | `libcvm.so.2`, `libcvm.so.4` |
| Chữ ký | v1/v2/v3 hợp lệ |

## Quy trình test đề nghị

Trước tiên hãy cài v13 thay cho bản v2 bằng cùng keystore. Trong phần cài đặt, tắt bitmap font để kiểm tra riêng đường System Font. Mở ô nhập liệu và dán lần lượt các ký tự `ă ạ ư ứ ừ ự đ â ê ô`, sau đó thử chuỗi `aw`, `uw`, `dd`, `ạ`, `ứ` nếu bàn phím có thể tạo chúng. Nếu v13 đã đưa codepoint qua được CVM, ký tự sẽ không còn biến mất ngay sau khi dán; đường vẽ System Font mới là phần được đánh giá ở bước này.

Sau đó có thể bật lại bitmap font để kiểm tra hành vi cũ. Bản v13 không thêm glyph bitmap mới; do đó việc bitmap có vẽ được một codepoint hay không phụ thuộc bộ glyph hiện có của Font66-UI. Đây là chủ ý để tách lỗi truyền Unicode khỏi giới hạn glyph bitmap.

Nếu v13 vẫn mất ký tự khi bitmap đã tắt, xin gửi log mới kèm đúng ba thao tác: mở ô nhập, dán `ăạưđ`, chụp kết quả. Khi đó cần đối chiếu tiếp nhánh renderer/font, không nên quay lại sửa UTF-8 vì protocol nội bộ của PhoneME là 16-bit, không phải UTF-8.

## Căn cứ lịch sử

Chuỗi artifact cũ ghi nhận bản `InputFix7-nativeUnicodeTextCave` thay đổi đúng hai chunk `libcvm.so.2` và `libcvm.so.4`, giữ nguyên `classes.dex` của InputFix7 stateful Telex và dùng helper scratch BSS. Các bản InputFix8–InputFix20 về sau tiếp tục tái sử dụng cùng native ELF, chỉ thay đổi Java-side reset/composition/Gboard và logging. Điều này cho thấy native Unicode bridge là lớp nền độc lập với các sửa lỗi Telex về sau.
