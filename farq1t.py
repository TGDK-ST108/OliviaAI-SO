import csv
import re
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

# Generate AES key and Farqit parameter
AES_KEY = os.urandom(32)  # 256-bit AES key
FARQIT_PARAMETER = 13  # Unique transposition parameter for Farqit

# AES Encryption Function
def aes_encrypt(data, key):
    iv = os.urandom(16)  # 128-bit IV
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(data.encode()) + encryptor.finalize()
    return iv + ciphertext  # Return IV + Ciphertext for decryption

# AES Decryption Function
def aes_decrypt(encrypted_data, key):
    iv = encrypted_data[:16]  # Extract IV
    ciphertext = encrypted_data[16:]
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    return decryptor.update(ciphertext) + decryptor.finalize()

# Farqit Transposition (Encrypt)
def farqit_transpose_encrypt(data, parameter):
    segments = [data[i : i + parameter] for i in range(0, len(data), parameter)]
    transposed = ''.join(segment[::-1] for segment in segments)  # Reverse each segment
    return transposed

# Farqit Transposition (Decrypt)
def farqit_transpose_decrypt(data, parameter):
    segments = [data[i : i + parameter] for i in range(0, len(data), parameter)]
    reversed_transposed = ''.join(segment[::-1] for segment in segments)  # Reverse each segment back
    return reversed_transposed

# Encrypt SSN with AES + Farqit Transposition
def encrypt_ssn_with_farqit(ssn):
    aes_encrypted = aes_encrypt(ssn, AES_KEY)  # AES encryption
    farqit_encrypted = farqit_transpose_encrypt(aes_encrypted.hex(), FARQIT_PARAMETER)  # Farqit transposition
    return farqit_encrypted

# Decrypt SSN with AES + Farqit Transposition
def decrypt_ssn_with_farqit(encrypted_ssn):
    farqit_decrypted = farqit_transpose_decrypt(encrypted_ssn, FARQIT_PARAMETER)  # Reverse Farqit transposition
    aes_decrypted = aes_decrypt(bytes.fromhex(farqit_decrypted), AES_KEY)  # AES decryption
    return aes_decrypted.decode()

# Validate SSN Format
def validate_ssn_format(ssn):
    pattern = r"^\d{3}-\d{2}-\d{4}$"
    return re.match(pattern, ssn) is not None

# Process SSN Upload
def process_ssn_upload(file_path):
    valid_ssns = []
    try:
        with open(file_path, mode="r") as file:
            reader = csv.reader(file)
            for row in reader:
                ssn = row[0].strip()
                if validate_ssn_format(ssn):
                    encrypted_ssn = encrypt_ssn_with_farqit(ssn)
                    valid_ssns.append(encrypted_ssn)
                else:
                    print(f"Invalid SSN format: {ssn}")
        return valid_ssns
    except Exception as e:
        print(f"Error processing SSN upload: {e}")
        return []

# Distribute Functionalities Securely
def distribute_to_users(encrypted_ssns):
    for encrypted_ssn in encrypted_ssns:
        try:
            decrypted_ssn = decrypt_ssn_with_farqit(encrypted_ssn)
            if validate_ssn_format(decrypted_ssn):
                print(f"Distributing functionalities to user with SSN: {decrypted_ssn}")
            else:
                print(f"Decryption failed or unauthorized SSN: {decrypted_ssn}")
        except Exception as e:
            print(f"Error during distribution: {e}")

# Example Usage
# Replace 'ssn_upload.csv' with the actual file path for SSN uploads
# uploaded_ssns = process_ssn_upload("ssn_upload.csv")
# distribute_to_users(uploaded_ssns)