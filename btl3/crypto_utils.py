from Crypto.Cipher import DES
from Crypto.Hash import SHA512
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Util.Padding import pad, unpad
import base64

# DES key: 8 byte
KEY_DES = b'8bytekey'  # Bạn có thể thay bằng bất kỳ khóa 8 byte nào khác

def encrypt_and_sign(plaintext, receiver_public_key_path, sender_private_key_path):
    # Mã hóa bằng DES
    des = DES.new(KEY_DES, DES.MODE_ECB)
    padded = pad(plaintext.encode(), 8)
    encrypted = des.encrypt(padded)

    # Tạo chữ ký bằng RSA SHA-512
    h = SHA512.new(encrypted)
    with open(sender_private_key_path, 'rb') as f:
        private_key = RSA.import_key(f.read())
    signature = pkcs1_15.new(private_key).sign(h)

    # Ghép signature + encrypted, rồi mã hóa base64
    combined = signature + encrypted
    return base64.b64encode(combined)  # Dạng bytes

def decrypt_and_verify(ciphertext_b64, receiver_private_key_path, sender_public_key_path):
    # Giải mã base64
    raw = base64.b64decode(ciphertext_b64)
    signature = raw[:256]  # Giả định RSA 2048-bit => chữ ký 256 byte
    encrypted = raw[256:]

    # Xác minh chữ ký
    h = SHA512.new(encrypted)
    with open(sender_public_key_path, 'rb') as f:
        sender_key = RSA.import_key(f.read())
    pkcs1_15.new(sender_key).verify(h, signature)  # Gây lỗi nếu không hợp lệ

    # Giải mã DES
    des = DES.new(KEY_DES, DES.MODE_ECB)
    decrypted = des.decrypt(encrypted)
    return unpad(decrypted, 8).decode()
