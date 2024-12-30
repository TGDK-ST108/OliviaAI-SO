class FinancialReport:
    def __init__(self, revenue, expenses, assets, liabilities, cash_flows):
        self.revenue = revenue
        self.expenses = expenses
        self.assets = assets
        self.liabilities = liabilities
        self.cash_flows = cash_flows

    def calculate_net_income(self):
        return self.revenue - self.expenses

    def calculate_equity(self):
        return self.assets - self.liabilities

    def generate_report(self):
        net_income = self.calculate_net_income()
        equity = self.calculate_equity()
        
        report = f"""
        ------------------ Financial Report ------------------
        Income Statement:
        - Revenue: ${self.revenue:,.2f}
        - Expenses: ${self.expenses:,.2f}
        - Net Income: ${net_income:,.2f}

        Balance Sheet:
        - Assets: ${self.assets:,.2f}
        - Liabilities: ${self.liabilities:,.2f}
        - Equity: ${equity:,.2f}

        Cash Flow Statement:
        - Cash Flow (Operating): ${self.cash_flows['operating']:,.2f}
        - Cash Flow (Investing): ${self.cash_flows['investing']:,.2f}
        - Cash Flow (Financing): ${self.cash_flows['financing']:,.2f}

        ------------------------------------------------------
        """
        return report

# Example Usage
financial_data = {
    "revenue": 500000.00,
    "expenses": 300000.00,
    "assets": 700000.00,
    "liabilities": 200000.00,
    "cash_flows": {
        "operating": 150000.00,
        "investing": -50000.00,
        "financing": 25000.00
    }
}

report = FinancialReport(
    revenue=financial_data["revenue"],
    expenses=financial_data["expenses"],
    assets=financial_data["assets"],
    liabilities=financial_data["liabilities"],
    cash_flows=financial_data["cash_flows"]
)

print(report.generate_report())