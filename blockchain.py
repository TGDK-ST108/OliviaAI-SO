import hashlib
import random
import json
import base64
import time

# Blockchain simulation
class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_block(previous_hash="1", proof=100)
    
    def create_block(self, proof, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time.time(),
            'proof': proof,
            'previous_hash': previous_hash,
            'transactions': []
        }
        self.chain.append(block)
        return block
    
    def add_transaction(self, sender, receiver, amount, transaction_id):
        self.chain[-1]['transactions'].append({
            'sender': sender,
            'receiver': receiver,
            'amount': amount,
            'transaction_id': transaction_id,
            'timestamp': time.time()
        })

    def get_last_block(self):
        return self.chain[-1]
    
    def validate_chain(self):
        # Simulate chain validation (hash comparison)
        for i in range(1, len(self.chain)):
            prev_block = self.chain[i - 1]
            curr_block = self.chain[i]
            if curr_block['previous_hash'] != prev_block['previous_hash']:
                return False
            curr_block_hash = self.hash_block(curr_block)
            if curr_block_hash[:5] != "00000":  # Simulating difficulty
                return False
        return True

    def hash_block(self, block):
        block_str = json.dumps(block, sort_keys=True)
        return hashlib.sha256(block_str.encode()).hexdigest()

# Step 1: Define the Mushi Particle (Transaction)
class MushiParticle:
    def __init__(self, sender, receiver, amount, transaction_id):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.transaction_id = transaction_id
        self.encrypted_data = None
        self.encrypted_key = None

    def generate_encryption_key(self):
        # Simulate a quantum encryption key (using base64 encoding for simplicity)
        key = base64.b64encode(bytes(str(random.randint(1000, 9999)), 'utf-8'))
        self.encrypted_key = key
        return key

    def encrypt_transaction(self):
        # Simulating the encryption of the transaction data
        transaction_data = json.dumps(self.__dict__, sort_keys=True)
        encrypted_data = base64.b64encode(bytes(transaction_data, 'utf-8'))
        self.encrypted_data = encrypted_data
        return encrypted_data

# Step 2: Fraud Detection Simulation
def detect_fraud(transaction, last_transactions):
    # Simulate fraud detection by comparing transaction patterns
    typical_amount = sum([t['amount'] for t in last_transactions]) / len(last_transactions) if last_transactions else 0
    if abs(transaction.amount - typical_amount) > 100:  # Arbitrary fraud detection threshold
        print("Fraud detected: Transaction deviates significantly from typical amount.")
        return True
    return False

# Step 3: Transaction Validation and Blockchain Integration
def process_transaction(sender, receiver, amount, blockchain):
    # Create a Mushi particle (transaction)
    transaction_id = hashlib.sha256(f"{sender}-{receiver}-{amount}".encode()).hexdigest()
    mushi_particle = MushiParticle(sender, receiver, amount, transaction_id)
    
    # Encrypt the transaction data
    encrypted_data, encryption_key = mushi_particle.encrypt_transaction()
    
    # Simulate fraud detection
    last_transactions = blockchain.chain[-1]['transactions']
    is_fraud = detect_fraud(mushi_particle, last_transactions)
    if is_fraud:
        print("Transaction rejected due to fraud.")
        return None

    # Add the transaction to the blockchain
    blockchain.add_transaction(sender, receiver, amount, transaction_id)

    # Validate blockchain (mock validation)
    if not blockchain.validate_chain():
        print("Blockchain validation failed!")
        return None

    print(f"Transaction {transaction_id} successfully added to the blockchain.")
    return encrypted_data

# Simulate Blockchain
blockchain = Blockchain()

# Run an example transaction
sender = "Alice"
receiver = "Bob"
amount = 100.0

processed_transaction = process_transaction(sender, receiver, amount, blockchain)
if processed_transaction:
    print(f"Processed Transaction: {processed_transaction}")
else:
    print("Transaction failed.")