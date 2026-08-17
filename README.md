# PhoneME-Turbo

**PhoneME-Turbo** là dự án PhoneME-MOD cho Android, bắt đầu từ APK PhoneME sơ khai `be.preuveneers.phoneme.fpmidp` do người dùng cung cấp làm nền tham chiếu chung. Từ nền này, dự án được phát triển thành hai bản phát hành: **PhoneME-Turbo** theo hướng HEAP32M và **PhoneME-Turbo(nHD)** theo hướng HEAP64M. Bản 1.1.0 tập trung vào khả năng chạy ổn định, nhập liệu Unicode tiếng Việt, giao diện quản lý game gọn hơn, cài game Java trực tiếp bằng file JAR và duy trì hoạt động mạng tốt hơn khi đa nhiệm.

> Đây là dự án cộng đồng và là các APK đã được chỉnh sửa từ PhoneME. Hãy sao lưu dữ liệu trước khi cài đặt, chỉ cài APK từ nguồn mà bạn tin cậy và tự chịu trách nhiệm về việc sử dụng trên thiết bị của mình.

## Tải xuống

Hai APK đã ký và mã SHA-256 được công bố trong [GitHub Release v1.1.0](https://github.com/huongdino443/PhoneME-Turbo/releases/tag/v1.1.0).

| Bản | Thiết bị mục tiêu | minSdk / targetSdk | SHA-256 |
|---|---|---:|---|
| `PhoneME-Turbo.apk` | Android đời thấp, cấu hình khiêm tốn | 8 / 8 | `aa42e5979b5bb7ce75d51a131b3888311b0c26b91f57cfeb3219078a83d260cb` |
| `PhoneME-Turbo-nHD.apk` | Android mới hơn, màn hình nHD hoặc độ phân giải cao | 18 / 22 | `fd1a2fb7d83731970a226d2456f1aefba47840569e244882ace3861bd67cdd22` |

Hai bản trên là các bản phát hành cuối được chia sẻ trong repository. Bản thường phù hợp với thiết bị Android cũ; bản nHD phù hợp hơn với thiết bị Android mới và màn hình độ phân giải cao.

## Tính năng chính

So với APK PhoneME sơ khai dùng làm nền tham chiếu, PhoneME-Turbo có giao diện danh sách game dạng lưới, tối ưu cho cả màn hình dọc và ngang. Game mới cài được đưa lên đầu danh sách, và game Java có thể được cài trực tiếp bằng file `.jar` mà không cần chuẩn bị thêm file `.jad`. Ô nhập đường dẫn được giữ trên một dòng để tránh xuống dòng ngoài ý muốn.

Phần nhập liệu được gia cố để xử lý tốt hơn bàn phím ảo, bàn phím vật lý, trạng thái Shift/Alt, xóa, xuống dòng và Telex. Native Unicode bridge cho phép chuyển các ký tự BMP tiếng Việt mở rộng như `ă`, `ạ`, `ư`, `đ`, `â`, `ê` và `ô` vào CVM theo giao thức key event 16-bit của PhoneME.

Bản Turbo thường duy trì khả năng tương thích với Android cũ ở `minSdkVersion 8` và `targetSdkVersion 8`, đồng thời thu nhỏ font game khoảng 66% để bố cục gọn hơn. Bản nHD phát triển theo hướng HEAP64M, có lớp OpenGL/co giãn hình ảnh phù hợp màn hình nHD và yêu cầu Android mới hơn với `minSdkVersion 18`, `targetSdkVersion 22`. Hai bản đã tích hợp các thay đổi về vòng đời dịch vụ nhằm giúp game online giữ hoạt động mạng tốt hơn khi người dùng chuyển sang ứng dụng khác; kết quả thực tế vẫn có thể phụ thuộc vào thiết bị, hệ điều hành và máy chủ game.

Logging mặc định được tiết chế, chỉ giữ lại các thông tin cần thiết cho hoạt động và chẩn đoán khi bật chế độ phù hợp. Pipeline audio và các guard vòng đời được giữ ở mức thận trọng để giảm nguy cơ treo hoặc crash trong quá trình sử dụng.

## Cài đặt

Trước khi cài, hãy gỡ hoặc sao lưu bản PhoneME cũ nếu thiết bị báo xung đột chữ ký. Tải đúng APK từ Release, kiểm tra SHA-256 nếu cần, bật quyền cài ứng dụng từ nguồn phù hợp trên thiết bị, sau đó mở APK và hoàn tất cài đặt. Khi nâng cấp, nên giữ cùng một package và ký hiệu APK; nếu Android báo gói không hợp lệ, hãy kiểm tra lại file tải xuống và bản Android có đáp ứng `minSdk` hay không.

Sau khi mở ứng dụng, dùng chức năng cài game để chọn file `.jar`. Với game online, nên thử riêng Wi‑Fi và dữ liệu di động; trên Android đời cao, có thể cần cho phép PhoneME-Turbo chạy nền và tắt tối ưu pin cho ứng dụng nếu hệ thống tự ngắt mạng.

## Cấu trúc repository

| Thư mục | Nội dung |
|---|---|
| `scripts/` | Các patch script đã làm sạch đường dẫn, không chứa keystore hoặc lệnh ký APK |
| `docs/` | Báo cáo kỹ thuật về Unicode bridge, input và các thay đổi tương thích |
| `releases/` | Ghi chú về hai APK được phát hành dưới GitHub Releases |
| `CHANGELOG.md` | Changelog ở mức người dùng và kỹ thuật cần thiết |

Repository **không** chứa workspace giải mã đầy đủ, file tạm, log cá nhân, khóa ký, mật khẩu hoặc APK unsigned. Các patch script cần một cây PhoneME đã giải mã và các công cụ Android tương ứng; chúng không tự tải hay chứa các thành phần nền gốc có bản quyền.

## Xây dựng và patch

Các script trong `scripts/` được thiết kế theo nguyên tắc fail-closed: kiểm tra nền đầu vào, thay đổi tối thiểu và dừng nếu cấu trúc smali/ELF không khớp. Quy trình tổng quát là giải mã APK nền, áp dụng patch, build lại bằng apktool, zipalign, ký bằng **keystore riêng của người xây dựng** và xác minh bằng `apksigner`. Keystore không được lưu trong repository.

Patch native phụ thuộc vào đúng bố cục ELF của nền PhoneME tương ứng. Hãy đọc tài liệu trong `docs/` trước khi chạy trên một nền khác và luôn tạo bản sao lưu của APK/cây giải mã trước khi patch.

## Trạng thái phát hành

`v1.1.0` là bản stable đầu tiên được công bố dưới tên PhoneME-Turbo. Hai APK đã được build, zipalign, ký và kiểm tra chữ ký; chúng đã được người dùng kiểm thử thực tế trước khi chia sẻ. Một số game có cách loop âm thanh riêng và có thể cho kết quả khác nhau theo thiết bị, vì vậy bản phát hành không tuyên bố mọi game đều có cùng hành vi âm thanh.

## Nền tham chiếu

APK sơ khai được dùng làm điểm xuất phát có các thông tin đã kiểm tra như sau:

| Thuộc tính | Giá trị |
|---|---|
| Tên file tham chiếu | `be.preuveneers.phoneme.fpmidp--1.apk` |
| Package | `be.preuveneers.phoneme.fpmidp` |
| Version | `1.0.0` (`versionCode=1`) |
| minSdk / targetSdk | `8 / 8` |
| SHA-256 | `1d02bc4de2730a7255c49bddd3f9d784c7dc52d4795840c7e1dcc401e739a185` |

APK này là nền sơ khai được người dùng cung cấp để đối chiếu. Trong lịch sử phát triển của repository, HEAP32M và HEAP64M là hai hướng phát triển từ cùng nền đó.

## Giấy phép và nguồn gốc

PhoneME-Turbo là một bản mod/phân phối lại phục vụ mục đích nghiên cứu và sử dụng cá nhân. Các thành phần nguồn gốc PhoneME, Android và thư viện liên quan vẫn chịu giấy phép tương ứng của chúng. Repository này chỉ công bố patch, quy trình và artifact phát hành cần thiết; hãy kiểm tra giấy phép của thành phần gốc trước khi tái phân phối hoặc sử dụng thương mại.

## Tài liệu tham khảo

[1]: https://developer.android.com/guide/topics/manifest/uses-sdk "Android Developers — <uses-sdk> manifest element"
[2]: https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases "GitHub Docs — About releases"
