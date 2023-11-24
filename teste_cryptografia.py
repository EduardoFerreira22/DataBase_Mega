from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad


def encrypt_password(password, key):
    cipher = AES.new(key, AES.MODE_CBC, iv=get_random_bytes(16))
    encrypted_password = cipher.encrypt(pad(password.encode('utf-8'), 16))
    return cipher.iv + encrypted_password

def decrypt_password(encrypted_password, key):
    iv = encrypted_password[:16]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_password = unpad(cipher.decrypt(encrypted_password[16:]), 16)
    return decrypted_password.decode('utf-8')

# Exemplo de uso
encryption_key = get_random_bytes(16)
password = "C22@07eF"

encrypted_password = encrypt_password(password, encryption_key)
print(f"Senha criptografada: {encrypted_password}")

decrypted_password = decrypt_password(encrypted_password, encryption_key)
print(f"Senha descriptografada: {decrypted_password}")
