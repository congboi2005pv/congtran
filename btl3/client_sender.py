import socket, threading, os
from datetime import datetime
from crypto_utils import encrypt_and_sign, decrypt_and_verify

HOST = 'localhost'
PORT = 9001

PRIVATE_KEY = r'rsa_keys/client_private.pem'
RECEIVER_PUBLIC_KEY = r'rsa_keys/receiver_public.pem'

def receive_messages(sock):
    while True:
        try:
            data = sock.recv(4096)
            if not data:
                break
            plain = decrypt_and_verify(data, PRIVATE_KEY, RECEIVER_PUBLIC_KEY)
            if plain.startswith("__RFILE__:"):
                _, filename, content = plain.split("\n", 2)
                with open("receiver_" + filename, "w") as f:
                    f.write(content)
                print(f"📥 File từ Receiver: {filename}")
            else:
                print(f"[Receiver]: {plain}")
        except Exception as e:
            print("❌ Lỗi nhận:", e)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    threading.Thread(target=receive_messages, args=(s,), daemon=True).start()
    while True:
        msg = input("Bạn (Client): ")
        if msg.startswith("sendfile "):
            fname = msg.split(" ", 1)[1]
            if os.path.isfile(fname):
                with open(fname, "r") as f:
                    content = f.read()
                msg = f"__RFILE__:\nclient_{fname}\n{content}"
        encrypted = encrypt_and_sign(msg, RECEIVER_PUBLIC_KEY, PRIVATE_KEY)
        s.sendall(encrypted)
