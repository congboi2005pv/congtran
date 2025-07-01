import socket
from datetime import datetime
from crypto_utils import decrypt_and_verify, encrypt_and_sign

HOST = '0.0.0.0'
PORT = 9003

PRIVATE_KEY = r'rsa_keys/receiver_private.pem'
CLIENT_PUBLIC_KEY = r'rsa_keys/client_public.pem'

def handle(conn):
    try:
        while True:
            data = conn.recv(4096)
            if not data:
                break
            plain = decrypt_and_verify(data, PRIVATE_KEY, CLIENT_PUBLIC_KEY)
            if plain.startswith("__RFILE__:"):
                _, filename, content = plain.split("\n", 2)
                with open("client_" + filename, "w") as f:
                    f.write(content)
                print(f"📥 File từ Client: {filename}")
            else:
                print(f"[Client]: {plain}")

            reply = input("Bạn (Receiver): ")
            if reply.startswith("sendfile "):
                fname = reply.split(" ", 1)[1]
                with open(fname, "r") as f:
                    content = f.read()
                reply = f"__RFILE__:\nreceiver_{fname}\n{content}"
            encrypted = encrypt_and_sign(reply, CLIENT_PUBLIC_KEY, PRIVATE_KEY)
            conn.sendall(encrypted)
    except Exception as e:
        print("❌ Lỗi:", e)
    finally:
        conn.close()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("🎯 Receiver sẵn sàng.")
    conn, addr = s.accept()
    print(f"[{datetime.now()}] ✅ Kết nối từ Server2: {addr}")
    handle(conn)
