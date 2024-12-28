class CyberShieldProcessor:
    def __init__(self, base_value):
        self.base_value = base_value

    def calculate_shielding_factor(self):
        Mi = self.base_value * 0.1
        Mo = self.base_value * 0.2
        Fq = self.base_value * 0.3
        Fx = self.base_value * 0.4

        # Shielding Factor Calculation
        shielding_factor = Mi + Mo + Fq + Fx
        return shielding_factor

    def adjust_base_value(self, threat_level):
        if threat_level == "Low":
            self.base_value = 10**3
        elif threat_level == "Medium":
            self.base_value = 10**4
        elif threat_level == "High":
            self.base_value = 10**5
        else:
            raise ValueError("Invalid threat level")

# Example Usage
processor = CyberShieldProcessor(base_value=1000)
processor.adjust_base_value("High")
shielding_factor = processor.calculate_shielding_factor()

print(f"Shielding Factor: {shielding_factor}")