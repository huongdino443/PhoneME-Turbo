# PhoneME-Turbo

**PhoneME-Turbo** là dự án PhoneME-MOD cho Android, phát triển từ các nhánh HEAP32M và HEAP64M/R39. Bản phát hành 1.1.0 tập trung vào khả năng chạy ổn định, nhập liệu Unicode tiếng Việt, giao diện quản lý game gọn hơn và cài game Java trực tiếp bằng file JAR.

> Đây là dự án cộng đồng và là các APK đã được chỉnh sửa từ PhoneME. Hãy sao lưu dữ liệu trước khi cài đặt, chỉ cài APK từ nguồn mà bạn tin cậy và tự chịu trách nhiệm về việc sử dụng trên thiết bị của mình.

## Tải xuống

Các APK đã ký và mã SHA-256 được công bố trong [GitHub Release v1.1.0](../../releases/tag/v1.1.0). Hai bản có hậu tố `cbSIP` là lựa chọn stable chính; hai bản có hậu tố `NetworkKeep` là biến thể thử nghiệm đã tích hợp cơ chế giữ tiến trình/kết nối khi đưa game xuống nền.

| Bản | Thiết bị mục tiêu | minSdk / targetSdk | SHA-256 |
|---|---|---:|---|
| `PhoneME-Turbo-cbSIP.apk` | Android đời thấp, cấu hình khiêm tốn | 8 / 8 | `428d12b58ab0c30b382e84c38147022ed0b9b40ad03ccfd7a0f9f8ded21b96f8` |
| `PhoneME-Turbo-nHD-cbSIP.apk` | Android mới hơn, màn hình nHD hoặc độ phân giải cao | 18 / 22 | `3182c6c01fb944e5edfe32dd7d42e65ed5f7a65b7a759dfb8989dbb726815427` |
| `PhoneME-Turbo-NetworkKeep.apk` | Turbo thường, có giữ tiến trình/kết nối khi đa nhiệm | 8 / 8 | `aa42e5979b5bb7ce75d51a131b3888311b0c26b91f57cfeb3219078a83d260cb` |
| `PhoneME-Turbo-nHD-NetworkKeep.apk` | Turbo nHD, có giữ tiến trình/kết nối khi đa nhiệm | 18 / 22 | `fd1a2fb7d83731970a226d2456f1aefba47840569e244882ace3861bd67cdd22` |

**Khuyến nghị:** nếu chỉ cần bản stable thông thường, hãy chọn `PhoneME-Turbo-cbSIP.apk` hoặc `PhoneME-Turbo-nHD-cbSIP.apk`. Nếu thường chơi game online và hay chuyển qua ứng dụng khác, có thể thử biến thể `NetworkKeep`; biến thể này có thể tiêu thụ pin cao hơn trong lúc game đang chạy.

## Tính năng chính

So với các bản PhoneME-MOD sơ khai HEAP32M và HEAP64M/R39, PhoneME-Turbo có giao diện danh sách game dạng lưới, tối ưu cho cả màn hình dọc và ngang. Game mới cài được đưa lên đầu danh sách, và game Java có thể được cài trực tiếp bằng file `.jar` mà không cần chuẩn bị thêm file `.jad`.

Phần nhập liệu được gia cố để xử lý tốt hơn bàn phím ảo, bàn phím vật lý, trạng thái Shift/Alt, xóa, xuống dòng và Telex. Bộ native Unicode bridge cho phép chuyển các ký tự BMP tiếng Việt mở rộng như `ă`, `ạ`, `ư`, `đ`, `â`, `ê` và `ô` vào CVM theo giao thức key event 16-bit của PhoneME. Bàn phím ảo SIP được bật mặc định thông qua `cbSIP`.

Bản Turbo thường giữ mức tương thích Android cũ với `minSdkVersion 8` và `targetSdkVersion 8`; bản nHD dùng nền HEAP64M/R39, có lớp OpenGL/co giãn hình ảnh và yêu cầu Android mới hơn với `minSdkVersion 18`, `targetSdkVersion 22`. Font game ở nhánh Turbo thường được thu nhỏ khoảng 66% để giao diện gọn hơn. Audio R39 và các guard vòng đời được giữ lại trong bản stable.

Hai biến thể `NetworkKeep` bổ sung `PARTIAL_WAKE_LOCK` và `WifiLock` trong `PhoneMEMonitorService`, đồng thời thêm các quyền `WAKE_LOCK`, `ACCESS_WIFI_STATE` và `CHANGE_WIFI_STATE`. Các lock được acquire khi service game bắt đầu và release khi service kết thúc. Android đời cao vẫn có thể giới hạn mạng nền do chế độ tiết kiệm pin hoặc chính game đóng phiên, vì vậy đây không phải cam kết reconnect cho mọi game.

## Cài đặt

Trước khi cài, hãy gỡ hoặc sao lưu bản PhoneME cũ nếu thiết bị báo xung đột chữ ký. Tải đúng APK từ Release, kiểm tra SHA-256 nếu cần, bật quyền cài ứng dụng từ nguồn phù hợp trên thiết bị, sau đó mở APK và hoàn tất cài đặt. Khi nâng cấp, nên giữ cùng một package và ký hiệu APK; nếu Android báo gói không hợp lệ, hãy kiểm tra lại file tải xuống và bản Android có đáp ứng `minSdk` hay không.

Sau khi mở ứng dụng, dùng chức năng cài game để chọn file `.jar`. Với game online, nên thử riêng Wi‑Fi và dữ liệu di động; trên Android đời cao, có thể cần cho phép PhoneME-Turbo chạy nền và tắt tối ưu pin cho ứng dụng nếu hệ thống tự ngắt mạng.

## Cấu trúc repository

| Thư mục | Nội dung |
|---|---|
| `scripts/` | Các patch script đã làm sạch đường dẫn, không chứa keystore hoặc lệnh ký APK |
| `docs/` | Báo cáo kỹ thuật và phạm vi thay đổi của Unicode bridge và NetworkKeep |
| `releases/` | Ghi chú về các file APK được phát hành dưới GitHub Releases |
| `CHANGELOG.md` | Changelog ở mức người dùng và kỹ thuật cần thiết |

Repository **không** chứa workspace giải mã đầy đủ, file tạm, log cá nhân, khóa ký, mật khẩu hoặc APK unsigned. Các patch script cần một cây PhoneME đã giải mã và các công cụ Android tương ứng; chúng không tự tải hay chứa các thành phần nền gốc có bản quyền.

## Xây dựng và patch

Các script trong `scripts/` được thiết kế theo nguyên tắc fail-closed: kiểm tra nền đầu vào, thay đổi tối thiểu và dừng nếu cấu trúc smali/ELF không khớp. Quy trình tổng quát là giải mã APK nền, áp dụng patch, build lại bằng apktool, zipalign, ký bằng **keystore riêng của người xây dựng** và xác minh bằng `apksigner`. Keystore không được lưu trong repository.

`build_v13_native_unicode_bridge.py` chỉ thay đổi hai chunk native `libcvm.so.2` và `libcvm.so.4` tại các offset đã được kiểm tra; `apply_network_keepalive.py` chỉ chỉnh `PhoneMEMonitorService.smali` và `AndroidManifest.xml`. Do patch native phụ thuộc đúng bố cục ELF của nền R39, hãy đọc tài liệu trong `docs/` trước khi chạy trên một nền khác.

## Trạng thái phát hành

`v1.1.0` là bản stable đầu tiên được công bố dưới tên PhoneME-Turbo. Bản phát hành đã được build, zipalign, ký và kiểm tra chữ ký APK; các APK stable đã được người dùng kiểm thử thực tế trước khi chia sẻ. Những vấn đề âm thanh riêng biệt của một số game cụ thể không được coi là đã giải quyết tuyệt đối cho mọi game, vì hành vi loop còn phụ thuộc vào game và thiết bị.

## Giấy phép và nguồn gốc

PhoneME-Turbo là một bản mod/phân phối lại phục vụ mục đích nghiên cứu và sử dụng cá nhân. Các thành phần nguồn gốc PhoneME, Android và thư viện liên quan vẫn chịu giấy phép tương ứng của chúng. Repository này chỉ công bố patch, quy trình và artifact phát hành cần thiết; hãy kiểm tra giấy phép của thành phần gốc trước khi tái phân phối hoặc sử dụng thương mại.

## Tài liệu tham khảo

[1]: https://developer.android.com/guide/topics/manifest/uses-sdk "Android Developers — <uses-sdk> manifest element"
[2]: https://developer.android.com/reference/android/os/PowerManager.WakeLock "Android Developers — PowerManager.WakeLock"
[3]: https://developer.android.com/reference/android/net/wifi/WifiManager.WifiLock "Android Developers — WifiManager.WifiLock"
[4]: https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases "GitHub Docs — About releases"
