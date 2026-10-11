# PhoneME Turbo 1.2.3

## Changes compared with 1.2.2

### Tiếng Việt
- Giữ toàn bộ tính năng của 1.2.2: FPS GL/HD, kích thước thật, bố cục gamepad và cài đặt tập trung cho game.
- Cải thiện phát JSR-135: giữ player khi `stop`, xử lý EOM/hủy callback và hỗ trợ luồng AMR.
- Sửa sắp xếp/truy cập file gần đây trong trình duyệt JAR và cập nhật thời gian thư mục khi ghi tệp.
- Thoát EdgeSwipe có dừng callback khung hình trước khi dọn player.
- Ghi log chẩn đoán theo tùy chọn debug; tránh tự bật bàn phím khi mở cài đặt Canvas.

### English
- Carries forward all 1.2.2 features: GL/HD FPS, true-size rendering, gamepad layouts, and game-focused settings.
- Improves JSR-135 playback: retain players on `stop`, handle EOM/callback cancellation, and support AMR streams.
- Fixes recent-file sorting/access and updates directory timestamps when files are written.
- EdgeSwipe exit stops framebuffer callbacks before releasing players.
- Makes diagnostic logging opt-in through debug settings and prevents the Canvas settings screen from opening the keyboard unexpectedly.

## Build information
- Version: `1.2.3`; version code `28`; minimum SDK `18`; target SDK `22`.
- Signed with the existing PhoneME Turbo release identity.
