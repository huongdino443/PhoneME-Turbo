# Patch scripts

Các script trong thư mục này là phần tái hiện những thay đổi cốt lõi của PhoneME-Turbo. Chúng chỉ xử lý cây giải mã hoặc APK đầu vào mà người dùng tự cung cấp; không tải mã nguồn PhoneME, không chứa keystore, không chứa mật khẩu và không thực hiện upload lên GitHub.

## Thành phần

| Script | Phạm vi |
|---|---|
| `build_font66ui_integrated.py` | Ghép pipeline audio ổn định, input bridge, logger có điều kiện và guard lifecycle vào nền Font66-UI; giữ nguyên renderer/font bitmap và native assets của nền |
| `build_v13_native_unicode_bridge.py` | Kiểm tra kích thước/offset ELF và thay đúng branch/helper của native Unicode bridge trong `libcvm.so.2` và `libcvm.so.4` |

## Quy trình khái quát

Trước tiên cần có một APK nền phù hợp, apktool, zipalign, apksigner và cây giải mã tương ứng. Hai APK phát hành hiện tại đều bắt đầu từ APK PhoneME sơ khai chung, sau đó được phát triển theo hướng HEAP32M hoặc HEAP64M. Với patch smali, chạy script trên cây giải mã. Với native bridge, chuẩn bị patch ELF có đúng bố cục các CVM chunk của nền tương ứng rồi chạy script với các tham số đầu vào được mô tả trong phần trợ giúp của script.

Sau khi patch, hãy build lại bằng apktool, zipalign và ký bằng một keystore riêng nằm ngoài repository. Dùng `apksigner verify` để kiểm tra artifact cuối cùng. Các script này không tự ký APK vì việc chia sẻ khóa hoặc mật khẩu là không an toàn.

## Kiểm tra an toàn

Script native dừng nếu branch site không đúng `0c0000ea`, vùng helper không còn zero-filled, kích thước chunk không đúng hoặc số chunk thay đổi ngoài dự kiến. Không bỏ qua các kiểm tra này để ép patch lên nền APK khác.

Các patch là những thay đổi phụ thuộc nền. Một APK khác package, phiên bản CVM, bố cục smali hoặc target Android có thể cần quy trình kiểm tra riêng.
