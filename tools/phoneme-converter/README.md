# PhoneME Converter

Trình chuyển đổi và kiểm tra JAR Java ME chạy ngay trong trình duyệt, dành cho người dùng PhoneME Turbo. Công cụ làm việc ở phía trình duyệt; file game được chọn không được gửi lên máy chủ.

## Khi nào nên dùng?

Đây không phải bước bắt buộc cho mọi game. Hãy giữ JAR gốc và chạy công cụ khi game Java ME gặp lỗi tương thích hoặc không khởi động trên PhoneME Turbo, nhất là khi có một trong các dấu hiệu sau:

- Nhật ký PhoneME báo lỗi xác minh lớp như `VerifyError`, `bad typematch`, lỗi StackMap hoặc từ chối class version.
- Game có các lớp Java mới hơn mức mà PhoneME chấp nhận. Công cụ dò mục tiêu bằng verifier tích hợp và chỉ hạ những lớp có thể sửa an toàn.
- Game chứa một mẫu class Java 8/obfuscator Army2D đã nhận diện.
- Có cấu trúc class cũ mà công cụ biết cách sửa an toàn: cờ `ACC_ABSTRACT` bị thiếu ở interface, lời gọi `Object.clone()` cũ trên mảng, một số mẫu bytecode/typeflow và trường hợp header HTTP `Content-Length` trùng.

Nếu game đã chạy bình thường, không cần chuyển đổi. Công cụ chỉ áp dụng các sửa đổi khi phát hiện mẫu tương thích đã hỗ trợ; nếu không thấy gì cần sửa, kết quả có thể giống JAR nguồn.

## Không sửa được mọi lỗi

Công cụ không phải trình giả lập và không bổ sung API còn thiếu cho PhoneME. Nó thường không giải quyết được lỗi do API Java/Java ME không có trên thiết bị, lỗi máy chủ/mạng, lỗi logic hoặc tài nguyên riêng của game, hay lỗi runtime không liên quan đến các mẫu class được hỗ trợ.

Một JAR đầu ra có thể được tạo nhưng chỉ xác minh một phần. Đọc trạng thái và danh sách class chưa xác minh trong báo cáo JSON trước khi thử. Ngay cả trạng thái “đã xác minh” cũng chỉ nói rằng bộ phoneME preverifier tích hợp chấp nhận các class; đó không phải chứng nhận rằng mọi màn chơi hoạt động trên mọi thiết bị.

## Cách dùng

1. Mở `index.html` trên GitHub Pages hoặc mở trực tiếp file HTML đã giải nén trong trình duyệt hiện đại.
2. Chọn một file game `.jar` (không chọn `.jad` hay APK).
3. Chọn **Kiểm tra và xử lý** và giữ trang mở đến khi hoàn tất.
4. Đọc trạng thái xác minh, các thay đổi và class chưa xác minh.
5. Tải JAR kết quả và báo cáo JSON. Thử bản kết quả trên thiết bị, giữ lại file gốc để khôi phục.

## Giới hạn và riêng tư

- JAR đầu vào tối đa 64 MB; ZIP64 và ZIP nhiều đĩa không được hỗ trợ.
- Quá trình xử lý chạy cục bộ trong trình duyệt bằng JavaScript/WebAssembly. Trang tĩnh không cần API server.
- Khi đăng lên GitHub Pages, trình duyệt cần mạng để tải trang lần đầu; sau khi mở trang, dữ liệu JAR không được tải lên.
- Nếu converter thay đổi nội dung JAR đã ký, chữ ký gốc không còn khớp; đừng coi kết quả là JAR còn chữ ký hợp lệ.
- Giữ trang đang mở khi chạy. Trên điện thoại, việc xử lý JAR lớn có thể chậm hoặc thiếu bộ nhớ.

## Gói GitHub Pages

Tệp `index.html` trong gói ZIP là bản độc lập: CSS, converter, phoneME verifier WebAssembly và API classpath đều được nhúng trong cùng một file. Giải nén ZIP vào thư mục xuất bản của GitHub Pages để `index.html` nằm ở thư mục gốc; `README.md` là tài liệu đi kèm.
