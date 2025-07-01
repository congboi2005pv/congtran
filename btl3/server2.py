import socket
import threading
from datetime import datetime

HOST = '0.0.0.0'
PORT = 9002

LOG_FILE = "server2.txt"
FORWARD_HOST = 'localhost'
FORWARD_PORT = 9013

def log(message):
    print(f"[{datetime.now()}] {message}")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now()}] {message}\n")


def handle_server1(conn, addr):
    log(f"🔌 Kết nối từ Server1: {addr}")
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as receiver_conn:
            receiver_conn.connect((FORWARD_HOST, FORWARD_PORT))
            while True:
                data = conn.recv(4096)
                if not data:
                    break
                log(f"📨 Nhận: {data[:50].hex()}...")
                receiver_conn.sendall(data)

                reply = receiver_conn.recv(4096)
                conn.sendall(reply)
                log(f"📤 Trả lời: {reply[:50].hex()}...")
    except Exception as e:
        log(f"⚠️ Lỗi: {e}")
    finally:
        conn.close()
        log(f"❌ Ngắt kết nối từ Server1: {addr}")


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("🚀 Server2 sẵn sàng...")
    while True:
        conn, addr = s.accept()
        threading.Thread(target=handle_server1, args=(conn, addr), daemon=True).start()
