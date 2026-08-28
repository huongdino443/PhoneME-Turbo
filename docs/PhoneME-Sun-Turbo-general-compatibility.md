# Đánh giá khả năng mở rộng tương thích phoneME-Turbo bằng source phoneME Sun

## Kết luận ngắn

Có thể dùng source phoneME Sun để nâng độ hỗ trợ game của phoneME-Turbo, nhưng theo hướng **phục hồi và port từng subsystem**, không phải thay toàn bộ runtime Turbo bằng binary Sun. Source Sun có giá trị vì chứa đầy đủ nhiều lớp CLDC/MIDP, JavaCall, PCSL, AMS/lifecycle, input/event, LCDUI/Canvas, RMS, security, network và các JSR. Tuy nhiên phần lớn mã native/platform của source Sun phụ thuộc KNI/JavaCall và các target Linux/ARM/x86 cũ; trong khi Turbo hiện có Android JNI/framebuffer/bitmap bridge riêng. Vì vậy cần giữ Android bridge và ABI của Turbo, rồi đưa behavior hoặc implementation phù hợp từ Sun vào từng lớp.

## Bằng chứng về phạm vi source Sun

Repository [magicus/phoneME](https://github.com/magicus/phoneME) là archive lớn được chuyển từ SVN, gồm các cây `cldc`, `midp`, `javacall`, `pcsl`, `cdc`, `jpeg`, `pisces` và nhiều JSR. Inventory local ghi nhận các nhóm chính:

| Nhóm | Số file source xấp xỉ | Ý nghĩa đối với tương thích |
|---|---:|---|
| `cldc` | 1.398 | VM/API nền, class library và runtime behavior |
| `midp` | 2.975 | AMS, lifecycle, LCDUI, Canvas, input, RMS, security, protocol |
| `javacall` | 430 | Porting contract giữa VM/MIDP và nền tảng |
| `pcsl` | 191 | File, memory, network, time và các dịch vụ nền |
| `cdc` | 4.623 | Runtime/profile CDC/Advanced, không nên nhập thẳng vào nhánh CLDC/MIDP |
| `jsr120` | 159 | Wireless messaging |
| `jsr135` | 139 | Mobile Media API |
| `jsr172` | 42 | Web services/XML-related API |
| `jsr177` | 276 | SATSA/smart-card/crypto-related API |
| `jsr211` | 92 | Content handler/lifecycle integration |
| `jsr239` | 63 | OpenGL ES 1.0 binding, tiềm năng cho game 3D |
| `jsr280` | 114 | Optional API trong cây phoneME lịch sử |

Các khu vực có giá trị tham khảo trực tiếp gồm `midp/src/events`, `midp/src/highlevelui`, `midp/src/lowlevelui`, `midp/src/rms`, `midp/src/security`, `midp/src/core`, `midp/src/ams`, `javacall` và `pcsl`. Đây là bằng chứng source Sun hữu ích cho tương thích tổng quát, không chỉ riêng image.

## Những gì Turbo hiện đã có

Inventory APK Turbo hiện tại cho thấy gói Foundation đang chứa `abstractions.jar`, `abstractions_agent.jar`, `jsr75.jar`, `jsr135.jar`, `jsr179.jar`, các công cụ `Romizer`, `SkinRomizationTool`, `ImageToRawTool`, skin `midp_linux_fb_gcc`, `libcvm.so` cùng các thư viện native `armeabi` và `arm64-v8a`.

Điều này cho thấy Turbo không phải một runtime Sun nguyên bản chưa đóng gói; nó đã chọn một tập component và đóng gói theo mô hình Foundation/MIDP riêng. Inventory hiện tại không thấy các JAR implementation độc lập tương ứng cho `jsr120`, `jsr172`, `jsr177`, `jsr211`, `jsr239` hoặc `jsr280`. Đây là các khoảng trống có thể khảo sát, nhưng việc thiếu JAR không tự động có nghĩa mọi API đó đều hoàn toàn không tồn tại trong `libcvm.so` hoặc trong các lớp khác.

Turbo cũng có các asset skin chuẩn cho menu, soft button, keyboard, choice, alert, gauge, progress bar, ticker, screen và font. Vì vậy source Sun có thể giúp khôi phục behavior/lifecycle và mapping skin; không cần mặc định port lại toàn bộ skin.

## Ranh giới không thể ghép thẳng

Native bridge Turbo hiện đi qua Android JNI và `AndroidBitmap`: các hàm khởi tạo framebuffer, resize, render, copy buffer, chuyển RGB565, đặt busy state và gọi VM đều nằm trong ABI Android riêng. Source Sun lại tổ chức port native quanh KNI/JavaCall, framebuffer Linux/QTE/FB và các target lịch sử. Do đó các file `.so` hoặc thư viện VM build sẵn từ source Sun không thể thay trực tiếp vào Turbo mà không phá ABI, entry point, thread/mutex, pixel format hoặc lifecycle Android.

Cách an toàn là giữ nguyên:

1. Android Activity/Service và JNI entry points của Turbo.
2. VM family, calling convention, ARM64 ABI và memory/thread boundary đang chạy ổn.
3. Framebuffer/Bitmap bridge, input dispatch tới Android và cơ chế đóng gói APK.
4. Các module đã chứng minh đang PASS, đặc biệt lifecycle UI và các game đã chạy ổn.

Có thể port hoặc so sánh:

1. Java-side API behavior và class implementation tương thích.
2. State machine AMS/lifecycle, Display/Canvas/Input, Form/TextBox và event queue.
3. RMS/file/network/security semantics ở lớp portable trước khi chạm native.
4. JSR class/API còn thiếu, sau đó mới viết platform adapter Android tương ứng.
5. Compatibility quirks có test chứng minh, thay vì force-advance hoặc nuốt mọi exception.

## Các hướng có khả năng tăng độ tương thích game

### Ưu tiên 1: Canvas, Display, input và lifecycle

Đây là nhóm có tác động rộng nhất tới game J2ME. Cần đối chiếu behavior của source Sun cho `Display`, `Canvas`, `GameCanvas`, repaint/paint callback, clipping, `flushGraphics`, key mapping, pointer events, show/hide màn hình, suspend/resume và chuyển Canvas/Form/TextBox. Những game mới thường không chỉ phụ thuộc vào API tồn tại mà còn phụ thuộc vào thứ tự callback, vùng clip, key repeat, thread timing và việc reset framebuffer khi đổi Displayable.

Turbo đã có nhiều lớp host UI và gamepad riêng, nên hướng đúng là lấy source Sun làm behavioral reference, lập test nhỏ cho từng contract, rồi sửa Java/bridge Turbo ở điểm sai. Không nên sao chép cả port Linux framebuffer.

### Ưu tiên 2: RMS, file, Connector và security

Nhiều game dùng RMS để lưu cấu hình, profile, unlock, trạng thái loading hoặc cache. Source Sun có implementation và port rõ cho RMS/PCSL/file/security. Có thể dùng để so sánh việc tạo, mở, đóng, enumerate, commit và xử lý lỗi store; đồng thời kiểm tra Connector/file path, permissions, charset và stream semantics. Đây là nhóm phù hợp để port từng method vì có thể kiểm thử offline bằng các game nhỏ và không nhất thiết đụng renderer.

### Ưu tiên 3: Mobile Media và audio

Turbo đã chứa `jsr135.jar`, nhưng native backend/behavior thực tế cần kiểm tra riêng. Source Sun có JSR-135 Java/native boundary và các build target audio. Có thể cải thiện khả năng tương thích bằng adapter Android cho Player lifecycle, MIME/content-type, repeated `start/stop`, volume, duration, tone/MIDI và giải phóng tài nguyên. Không nên thay backend bằng code Sun nguyên bản; cần giữ Android audio implementation.

### Ưu tiên 4: JSR còn thiếu và networking

Source Sun có các nhánh JSR bổ sung, nhưng cần phân loại theo game thực tế. `jsr120`/`jsr172` có thể hữu ích cho game có messaging hoặc web-service API; `jsr177` chủ yếu liên quan security/SATSA; `jsr211` liên quan content handler; `jsr239` đáng chú ý nếu mục tiêu là game dùng OpenGL ES 1.0. Mỗi API cần kiểm tra class reference của game, permission, native calls và behavior tối thiểu trước khi thêm.

Việc thêm một JAR stub chỉ giúp qua bước class loading; nếu game thật sự gọi network, media, 3D hoặc callback bất đồng bộ thì vẫn cần implementation và adapter Android. Vì vậy không nên coi “đã thêm class” là “đã tương thích”.

### Ưu tiên 5: 3D/OpenGL ES

`jsr239` trong source Sun là hướng tiềm năng để mở rộng nhóm game 3D, nhưng đây là dự án riêng có độ rủi ro cao. Cần xác định Turbo đang có EGL/GLES context nào, thread render nào, surface lifecycle nào và pixel/swap semantics ra sao. Không thể chỉ đưa `jsr239.jar` vào APK rồi kỳ vọng game chạy.

## Quy trình port được khuyến nghị

| Giai đoạn | Việc cần làm | Artifact kiểm chứng |
|---|---|---|
| A | Lập class/API matrix giữa game mẫu, Turbo và source Sun | Bảng thiếu API + log class loading |
| B | Chọn một subsystem có phạm vi hẹp, ưu tiên RMS hoặc input/lifecycle | Unit/probe và một APK thử nghiệm |
| C | Port Java-side trước, giữ nguyên native bridge | DEX/JAR diff, smoke test |
| D | Chỉ khi cần mới viết adapter Android/JNI tương ứng | Một native change có symbol/ABI manifest |
| E | Test trên nhiều nhóm game đại diện | Bảng PASS/FAIL theo Canvas, Form, audio, RMS, network, 3D |
| F | Chỉ tiếp nhận patch khi không hồi quy game đã PASS | Hash, log test, rollback artifact |

## Kết luận thực tế

Source phoneME Sun **có thể trở thành kho nền để nâng độ tương thích của phoneME-Turbo với nhiều game mới hơn**. Giá trị lớn nhất nằm ở implementation MIDP/CLDC và các port contract: lifecycle, Canvas/LCDUI, input/event, RMS, security, Connector, media và optional JSR. Nó không phải bản Turbo hoàn chỉnh, cũng không cho phép thay native binary trực tiếp.

Nếu làm đúng, hướng có triển vọng nhất là xây dựng một nhánh Turbo compatibility theo từng subsystem, bắt đầu từ Canvas/input/lifecycle và RMS/Connector, sau đó mới tới media/networking và cuối cùng là OpenGL ES/JSR tùy nhu cầu. Mỗi thay đổi cần một artifact độc lập và một nhóm game kiểm chứng; không nên chỉnh tất cả subsystem cùng lúc vì sẽ không biết thay đổi nào tạo ra tương thích hoặc hồi quy nào.

## Nguồn

[1]: https://github.com/magicus/phoneME
[2]: https://phonej2me.github.io/
[3]: https://phonej2me.github.io/content/phoneme_platforms.html
[4]: https://phonej2me.github.io/content/mr3/index_feature.html
[5]: https://minexew.github.io/2021/04/10/phoneme.html
