class EarningsStatement:
    def __init__(self, revenue, cogs, operating_expenses, taxes, interest):
        self.revenue = revenue
        self.cogs = cogs
        self.operating_expenses = operating_expenses
        self.taxes = taxes
        self.interest = interest

    def calculate_gross_profit(self):
        return self.revenue - self.cogs

    def calculate_operating_income(self):
        gross_profit = self.calculate_gross_profit()
        return gross_profit - self.operating_expenses

    def calculate_net_income(self):
        operating_income = self.calculate_operating_income()
        return operating_income - self.taxes - self.interest

    def generate_statement(self):
        gross_profit = self.calculate_gross_profit()
        operating_income = self.calculate_operating_income()
        net_income = self.calculate_net_income()

        statement = f"""
        ------------------ TGDK Earnings Statement ------------------
        Revenue: ${self.revenue:,.2f}
        Cost of Goods Sold (COGS): ${self.cogs:,.2f}
        Gross Profit: ${gross_profit:,.2f}

        Operating Expenses: ${self.operating_expenses:,.2f}
        Operating Income: ${operating_income:,.2f}

        Taxes: ${self.taxes:,.2f}
        Interest: ${self.interest:,.2f}
        Net Income: ${net_income:,.2f}
        -------------------------------------------------------------
        """
        return statement

# Example Usage
tgdk_financials = {
    "revenue": 1200000.00,
    "cogs": 400000.00,
    "operating_expenses": 300000.00,
    "taxes": 100000.00,
    "interest": 50000.00
}

tgdk_statement = EarningsStatement(
    revenue=tgdk_financials["revenue"],
    cogs=tgdk_financials["cogs"],
    operating_expenses=tgdk_financials["operating_expenses"],
    taxes=tgdk_financials["taxes"],
    interest=tgdk_financials["interest"]
)

print(tgdk_statement.generate_statement())