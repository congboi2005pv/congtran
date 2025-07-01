import socket
import threading
from datetime import datetime

HOST = '0.0.0.0'
PORT = 9001

LOG_FILE = "server1.txt"
FORWARD_HOST = 'localhost'
FORWARD_PORT = 9002

def log(message):
    print(f"[{datetime.now()}] {message}")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now()}] {message}\n")


def handle_client(conn, addr):
    log(f"🔌 Kết nối từ Client: {addr}")
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as forward:
            forward.connect((FORWARD_HOST, FORWARD_PORT))
            while True:
                data = conn.recv(4096)
                if not data:
                    break
                log(f"📨 Nhận: {data[:50].hex()}...")
                forward.sendall(data)

                reply = forward.recv(4096)
                conn.sendall(reply)
                log(f"📤 Trả lời: {reply[:50].hex()}...")
    except Exception as e:
        log(f"⚠️ Lỗi: {e}")
    finally:
        conn.close()
        log(f"❌ Ngắt kết nối từ Client: {addr}")


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("🚀 Server1 sẵn sàng...")
    while True:
        conn, addr = s.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
