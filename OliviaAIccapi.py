from fastapi import FastAPI
from pydantic import BaseModel

# Initialize FastAPI app
app = FastAPI(title="OliviaAI Cybersecurity API", description="API for Cyber Threat Analysis", version="1.0")

# Input models
class ThreatInput(BaseModel):
    data_stream: list[float]

class EncryptionInput(BaseModel):
    plaintext: str
    key: float

class DecryptionInput(BaseModel):
    ciphertext: str
    key: float

# Endpoints
@app.post("/analyze-threats")
def analyze_threats(input: ThreatInput):
    """
    Analyze data streams for cybersecurity threats.
    """
    threat_scores = [data_point * 1.5 for data_point in input.data_stream]  # Example scaling factor for threat analysis
    return {"threat_scores": threat_scores}

@app.post("/encrypt-data")
def encrypt_data(input: EncryptionInput):
    """
    Encrypt plaintext data using a quantum-inspired algorithm.
    """
    encrypted_text = ''.join([chr((ord(char) + int(input.key)) % 256) for char in input.plaintext])
    return {"encrypted_text": encrypted_text}

@app.post("/decrypt-data")
def decrypt_data(input: DecryptionInput):
    """
    Decrypt ciphertext data using the same quantum-inspired algorithm.
    """
    decrypted_text = ''.join([chr((ord(char) - int(input.key)) % 256) for char in input.ciphertext])
    return {"decrypted_text": decrypted_text}