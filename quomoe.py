from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

def encrypt_quomo_file(data, key):
    cipher = Cipher(algorithms.AES(key), modes.GCM())
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(data) + encryptor.finalize()
    return encrypted_data, encryptor.tag