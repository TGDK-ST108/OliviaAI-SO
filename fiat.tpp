// T++ - Hybrid Crypto-Fiat Debit Card Transaction System

class HybridDebitCard {
    var cardID;
    var fiatBalance;
    var cryptoBalance;

    // Initialize Card with Unique Encrypted ID
    def HybridDebitCard(cardHash) {
        this.cardID = cardHash;
        this.fiatBalance = 0;
        this.cryptoBalance = 0;
    }

    // Deposit Fiat Funds
    def depositFiat(amount) {
        this.fiatBalance += amount;
        return "Fiat Deposited: " + amount + " USD. New Balance: " + this.fiatBalance + " USD";
    }

    // Deposit Crypto Funds
    def depositCrypto(amount, currency) {
        this.cryptoBalance += amount;
        return "Crypto Deposited: " + amount + " " + currency + ". New Balance: " + this.cryptoBalance + " " + currency;
    }

    // Convert Crypto to Fiat in Real-Time
    def convertCryptoToFiat(amount, exchangeRate) {
        fiatEquivalent = amount * exchangeRate;
        this.cryptoBalance -= amount;
        this.fiatBalance += fiatEquivalent;
        return "Converted " + amount + " Crypto to " + fiatEquivalent + " USD";
    }

    // Execute Payment (Selects Best Currency)
    def pay(receiver, amount, securityCode) {
        if (this.fiatBalance >= amount && QuantumSecurity.validateSecurity(securityCode)) {
            this.fiatBalance -= amount;
            return "Fiat Payment Confirmed: " + amount + " USD sent to " + receiver;
        } 
        else if (this.cryptoBalance > 0) {
            convertedAmount = this.convertCryptoToFiat(this.cryptoBalance, 32000); // Example BTC rate
            if (this.fiatBalance >= amount) {
                this.fiatBalance -= amount;
                return "Crypto Payment Converted & Confirmed: " + amount + " USD sent to " + receiver;
            }
        }
        return "Transaction Failed - Insufficient Funds or Security Error";
    }
}

// Initialize Hybrid Debit Card with Teraqit Encrypted ID
cardHash = "defghiijjkkllmmn"; // Unique Card ID from Snell + Cycling + Mushi
UserCard = new HybridDebitCard(cardHash);

// Transactions
print(UserCard.depositFiat(500));  // Deposit 500 USD
print(UserCard.depositCrypto(0.01, "BTC")); // Deposit 0.01 BTC (~$320 USD)
print(UserCard.pay("Merchant123", 100, "SECURE_ACCESS_144")); // Pay $100