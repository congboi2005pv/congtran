from flask import Flask, request, render_template
import socket, threading, os
from crypto_utils import decrypt_and_verify, encrypt_and_sign

app = Flask(__name__)
HOST = '0.0.0.0'
PORT = 9013
PRIVATE_KEY = r'rsa_keys/receiver_private.pem'
CLIENT_PUBLIC_KEY = r'rsa_keys/client_public.pem'
messages = []
conn = None

def wait_for_connection():
    global conn
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    conn, _ = server.accept()
    while True:
        try:
            data = conn.recv(4096)
            if not data:
                break
            plain = decrypt_and_verify(data, PRIVATE_KEY, CLIENT_PUBLIC_KEY)
            if plain.startswith("__RFILE__:"):
                _, filename, content = plain.split("\\n", 2)
                save_path = os.path.join("static", "downloads", "client_" + filename)
                os.makedirs(os.path.dirname(save_path), exist_ok=True)
                with open(save_path, "w") as f:
                    f.write(content)
                messages.append(f'📥 File từ Client: <a href="/static/downloads/client_{filename}" download>{filename}</a>')
            else:
                messages.append(f"[Client]: {plain}")
        except Exception as e:
            messages.append(f"❌ Lỗi: {e}")

threading.Thread(target=wait_for_connection, daemon=True).start()

@app.route("/")
def index():
    return render_template("receiver.html")

@app.route("/reply", methods=["POST"])
def reply():
    if conn:
        data = request.get_json()
        msg = data["message"]
        if msg.startswith("sendfile "):
            fname = msg.split(" ", 1)[1]
            if os.path.isfile(fname):
                with open(fname, "r") as f:
                    content = f.read()
                msg = f"__RFILE__:\\nreceiver_{fname}\\n{content}"
        encrypted = encrypt_and_sign(msg, CLIENT_PUBLIC_KEY, PRIVATE_KEY)
        conn.sendall(encrypted)
    return "", 204

@app.route("/incoming")
def incoming():
    return "<br>".join(messages[-10:])

if __name__ == "__main__":
    app.run(port=5001)