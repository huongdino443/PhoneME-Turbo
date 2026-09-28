# PhoneME Turbo 1.2.0

Bản 1.2.0 là release hiện tại của **PhoneME Turbo**, phát triển từ dòng lịch sử 1.1.2 qua lineage v337–v340. Tên sản phẩm hiện tại không còn dùng nhãn nHD riêng.

## Thay đổi chính

- **Canvas theo từng game:** thêm Game Settings với width/height, giữ tỷ lệ, vị trí canvas và preset `240×320`, `320×240`, `320×480`, `360×640`, `480×800`.
- **FrameBuffer/touch routing:** thêm resolve target, destination sizing, clamp tọa độ và hit-testing riêng cho canvas/GL; giữ touch hoạt động đúng quanh vùng framebuffer.
- **GL pipeline:** bổ sung draw-frame path và truyền source size theo frame/bitmap để shader có thể xử lý kích thước nguồn; preset mặc định `360×640` vẫn tồn tại nhưng không phải tên sản phẩm hay giới hạn duy nhất.
- **EdgeSwipe:** thêm vùng swipe mở rộng, đưa menu đang hoạt động lên trước và điều chỉnh icon/cell/gap cho màn hình nhỏ.
- **Gamepad và bàn phím:** cải thiện pointer move/hit-test, touch pass-through và bàn phím launcher dạng overlay không làm co vùng nội dung.
- **Lifecycle Android:** cập nhật config thay đổi màn hình, hỗ trợ activity resizeable, foreground notification và wakelock có acquire/release cho runtime nền.
- **Compatibility bridge:** thêm/điều chỉnh Nokia `DeviceControl`, `FullCanvas`, `DirectGraphics`, `DirectUtils`, `Sound`, nhóm WMA message classes và một số lớp hỗ trợ game cũ. Sound shim chỉ đáp ứng API call, không tuyên bố phát Nokia Sound đầy đủ.
- **JAR processing:** thêm `SuiteCompatibilityNormalizer`, `JarExporter`, `ExportPathStore`, tên lưu JAR an toàn và các bản sao suite có chọn lọc; đây không phải một verifier CVM mới.
- **UI và nhận diện:** dark UI/LCDUI, bitmap-font option, các asset EdgeSwipe và toàn bộ nhãn runtime đổi thành `PhoneME Turbo`.
- **Logging/export:** bổ sung crash-handler path và các thay đổi console/log/export.

## Đối chiếu native

Core `assets/foundation/bin/libcvm.so`, `libcvm.so.1` và `libcvm.so.2` giữ nguyên so với APK 1.1.2 được kiểm tra. Native wrapper `lib/armeabi/libjniphoneme.so` có thay đổi. Vì vậy bản 1.2.0 không được mô tả là đã sửa CVM Split Verifier.

## Không tuyên bố hỗ trợ tổng quát

Release không tuyên bố thêm MMAPI music playback tổng quát, tự động chuyển playlist hoặc M3G rendering. Hành vi game còn phụ thuộc thiết bị, Android version, native capability và server game.

Chi tiết định lượng nằm trong [`../../docs/V1.2.0-VS-1.1.2-AUDIT.md`](../../docs/V1.2.0-VS-1.1.2-AUDIT.md).
