1. Cấu trúc hệ thống
Client → Server1 → Server2 → Receiver

Server1 và Server2 chỉ ghi log và chuyển tiếp, không giải mã.

Receiver sẽ giải mã và kiểm tra chữ ký.

2. Bảo mật dữ liệu
Mã hóa DES (khóa đối xứng): mã hóa nội dung file.

Ký số RSA (2048-bit): ký dữ liệu đã mã hóa, đảm bảo tính xác thực.

Hàm băm SHA-512: tạo chuỗi định danh để xác minh toàn vẹn nội dung.

Socket TCP: đảm bảo kênh truyền ổn định.

 Chức năng chính của các thành phần
Client
Gửi file/tin nhắn.

Mã hóa + ký số nội dung.

Giao diện web (Flask + Bootstrap).

Server1 và Server2
Không đọc nội dung.

Ghi log (thời gian, địa chỉ IP, dữ liệu mã hóa).

Chuyển tiếp dữ liệu.

Receiver
Giải mã dữ liệu.

Kiểm tra chữ ký số.

Hiển thị nội dung hoặc lưu file.

Có giao diện web phản hồi lại cho client.

Mã nguồn chính
client_sender.py, receiver.py: xử lý truyền tin socket.

server1.py, server2.py: chuyển tiếp và ghi log.

crypto_utils.py: chứa hàm mã hóa DES, ký số RSA, kiểm tra SHA-512.

generate_keys.py: sinh khóa RSA cho 4 thực thể.

app_client.py, app_receiver.py: Flask backend xử lý web.

Giao diện Web
Giao diện Client: nhập tin nhắn hoặc lệnh gửi file (sendfile <filename>).

Giao diện Receiver: phản hồi hoặc gửi lại file.
