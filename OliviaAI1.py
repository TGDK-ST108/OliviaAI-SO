import random
import numpy as np

# Example of a fraud detection algorithm (using simplified statistical checks for now)
class OliviaAI1:
    def __init__(self):
        self.transaction_history = []

    def detect_anomalies(self, new_transaction):
        # Calculate the average amount from previous transactions
        amounts = [t['amount'] for t in self.transaction_history]
        average_amount = np.mean(amounts) if amounts else 0

        # If the new transaction deviates significantly, flag as fraudulent
        if abs(new_transaction['amount'] - average_amount) > 100:  # Threshold for fraud detection
            print(f"Suspicious activity detected: {new_transaction}")
            return True
        return False

    def record_transaction(self, transaction):
        self.transaction_history.append(transaction)

# Simulate transactions and fraud detection
olivia_ai = OliviaAI1()

# Example transaction data (with randomly simulated amounts)
new_transaction = {'sender': 'Alice', 'receiver': 'Bob', 'amount': random.randint(50, 500)}
if olivia_ai.detect_anomalies(new_transaction):
    print("Fraud detected!")
else:
    olivia_ai.record_transaction(new_transaction)
    print(f"Transaction recorded: {new_transaction}")