import random
import hashlib
from cryptography.fernet import Fernet

class ShuffleModule:
    def __init__(self, encryption_key: bytes):
        self.cipher = Fernet(encryption_key)
    
    def hectuplineate(self, sequence: str) -> list:
        """
        Breaks the sequence into 100-line groups and shuffles them.
        """
        lines = sequence.split('\n')
        hectuplineated = [lines[i:i + 100] for i in range(0, len(lines), 100)]
        random.shuffle(hectuplineated)
        return hectuplineated

    def encrypt_segment(self, segment: list) -> str:
        """
        Encrypts a segment of lines.
        """
        joined_segment = "\n".join(segment)
        return self.cipher.encrypt(joined_segment.encode()).decode()

    def decrypt_segment(self, encrypted_segment: str) -> str:
        """
        Decrypts an encrypted segment of lines.
        """
        return self.cipher.decrypt(encrypted_segment.encode()).decode()

    def hash_segment(self, segment: list) -> str:
        """
        Creates a hash of the segment for validation.
        """
        joined_segment = "\n".join(segment)
        return hashlib.sha256(joined_segment.encode()).hexdigest()

    def obfuscate_sequence(self, sequence: str) -> dict:
        """
        Breaks, shuffles, encrypts, and hashes the sequence.
        """
        segments = self.hectuplineate(sequence)
        obfuscated = []
        for segment in segments:
            encrypted_segment = self.encrypt_segment(segment)
            segment_hash = self.hash_segment(segment)
            obfuscated.append({"encrypted": encrypted_segment, "hash": segment_hash})
        return obfuscated

    def reconstruct_sequence(self, obfuscated: list) -> str:
        """
        Decrypts and reconstructs the original sequence.
        """
        decrypted_segments = [
            self.decrypt_segment(segment["encrypted"]) for segment in obfuscated
        ]
        return "\n".join(decrypted_segments)

# Example Usage
if __name__ == "__main__":
    # Generate a secure encryption key
    key = Fernet.generate_key()
    shuffle_module = ShuffleModule(encryption_key=key)

    # Example sequence
    sequence = "\n".join([f"Line {i}" for i in range(1, 501)])  # Example with 500 lines

    # Obfuscate the sequence
    obfuscated = shuffle_module.obfuscate_sequence(sequence)

    # Reconstruct the sequence
    reconstructed = shuffle_module.reconstruct_sequence(obfuscated)

    # Validation
    assert sequence == reconstructed, "Reconstruction failed!"
    print("Sequence obfuscation and reconstruction successful.")