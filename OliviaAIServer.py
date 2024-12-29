class OliviaAIServer:
    def __init__(self, blockchain):
        self.blockchain = blockchain
        self.olivia_ai_1 = OliviaAI1()

    def process_transaction(self, sender, receiver, amount):
        # Step 1: Create transaction
        transaction_id = hashlib.sha256(f"{sender}-{receiver}-{amount}".encode()).hexdigest()
        transaction = {'sender': sender, 'receiver': receiver, 'amount': amount, 'transaction_id': transaction_id}

        # Step 2: Detect fraud using OliviaAI1
        if self.olivia_ai_1.detect_anomalies(transaction):
            print("Fraud detected!")
            return None

        # Step 3: Record transaction and add it to the blockchain
        self.blockchain.add_transaction(sender, receiver, amount, transaction_id)

        # Step 4: Validate blockchain after the transaction
        if not self.blockchain.validate_chain():
            print("Blockchain validation failed!")
            return None

        # Step 5: Return successful transaction
        print(f"Transaction {transaction_id} processed successfully.")
        return transaction_id

# Initialize server and blockchain
blockchain = Blockchain()
server = OliviaAIServer(blockchain)

# Process a new transaction
transaction_id = server.process_transaction("Alice", "Bob", 100.0)