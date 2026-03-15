from Crypto.Cipher import DES3
from Crypto.Util.Padding import pad, unpad
import base64
from django.conf import settings

# Use directly from settings (already parity-adjusted)
KEY = settings.THREE_DES_KEY

def encrypt_message(message):
    cipher = DES3.new(KEY, DES3.MODE_ECB)
    padded = pad(message.encode('utf-8'), DES3.block_size)
    encrypted = cipher.encrypt(padded)
    return base64.b64encode(encrypted).decode('utf-8')

def decrypt_message(encrypted_message):
    cipher = DES3.new(KEY, DES3.MODE_ECB)
    decoded = base64.b64decode(encrypted_message)
    decrypted = unpad(cipher.decrypt(decoded), DES3.block_size)
    return decrypted.decode('utf-8')
