from flask import Flask, request, render_template
import socket, threading, os
from crypto_utils import encrypt_and_sign, decrypt_and_verify

app = Flask(__name__)
HOST = 'localhost'
PORT = 9001
PRIVATE_KEY = r'rsa_keys/client_private.pem'
RECEIVER_PUBLIC_KEY = r'rsa_keys/receiver_public.pem'
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))
messages = []

def receive():
    while True:
        try:
            data = sock.recv(4096)
            if not data:
                break
            plain = decrypt_and_verify(data, PRIVATE_KEY, RECEIVER_PUBLIC_KEY)
            if plain.startswith("__RFILE__:"):
                _, filename, content = plain.split("\\n", 2)
                save_path = os.path.join("static", "downloads", "receiver_" + filename)
                os.makedirs(os.path.dirname(save_path), exist_ok=True)
                with open(save_path, "w") as f:
                    f.write(content)
                messages.append(f'📥 File từ Receiver: <a href="/static/downloads/receiver_{filename}" download>{filename}</a>')
            else:
                messages.append(f"[Receiver]: {plain}")
        except Exception as e:
            messages.append(f"❌ Lỗi nhận: {e}")

threading.Thread(target=receive, daemon=True).start()

@app.route("/")
def index():
    return render_template("client.html")

@app.route("/send", methods=["POST"])
def send():
    data = request.get_json()
    msg = data["message"]
    if msg.startswith("sendfile "):
        fname = msg.split(" ", 1)[1]
        if os.path.isfile(fname):
            with open(fname, "r") as f:
                content = f.read()
            msg = f"__RFILE__:\\nclient_{fname}\\n{content}"
    encrypted = encrypt_and_sign(msg, RECEIVER_PUBLIC_KEY, PRIVATE_KEY)
    sock.sendall(encrypted)
    return "", 204

@app.route("/messages")
def get_messages():
    return "<br>".join(messages[-10:])

if __name__ == "__main__":
    app.run(port=5000)
