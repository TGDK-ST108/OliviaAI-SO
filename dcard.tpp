// T++ - Smart Contract for Debit Card Transactions

class DebitCard {
    var cardID;
    var balance;

    // Initialize Card with Unique Encrypted ID
    def DebitCard(cardHash) {
        this.cardID = cardHash;
        this.balance = 0;
    }

    // Deposit Funds
    def deposit(amount) {
        this.balance += amount;
        return "Deposited: " + amount + " BTC. New Balance: " + this.balance + " BTC";
    }

    // Secure Payment Transaction
    def pay(receiver, amount, securityCode) {
        if (this.balance >= amount && QuantumSecurity.validateSecurity(securityCode)) {
            this.balance -= amount;
            return "Payment Confirmed: " + amount + " BTC sent to " + receiver;
        }
        return "Transaction Failed - Insufficient Funds or Security Error";
    }
}

// Initialize Debit Card with Encrypted ID
cardHash = "defghiijjkkllmmn"; // Unique Card ID from Snell + Cycling + Mushi
UserCard = new DebitCard(cardHash);

// Transactions
print(UserCard.deposit(0.5)); // Deposit 0.5 BTC
print(UserCard.pay("Merchant123", 0.1, "SECURE_ACCESS_144")); // Pay 0.1 BTC