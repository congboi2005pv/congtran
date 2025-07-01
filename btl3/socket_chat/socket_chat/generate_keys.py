from Crypto.PublicKey import RSA
import os

def generate_rsa_keys(name, directory="rsa_keys"):
    os.makedirs(directory, exist_ok=True)
    key = RSA.generate(2048)

    private_key_path = os.path.join(directory, f"{name}_private.pem")
    public_key_path = os.path.join(directory, f"{name}_public.pem")

    with open(private_key_path, "wb") as f:
        f.write(key.export_key())
    with open(public_key_path, "wb") as f:
        f.write(key.publickey().export_key())

# Tạo khóa cho các thực thể trong hệ thống
for entity in ["client", "server1", "server2", "receiver"]:
    generate_rsa_keys(entity)

print("✅ Đã tạo đủ 4 cặp khóa trong thư mục rsa_keys/")
