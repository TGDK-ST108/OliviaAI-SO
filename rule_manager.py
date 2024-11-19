class RuleManager:
    def __init__(self):
        self.rules = []

    def add_rule(self, rule):
        """Adds a new firewall rule."""
        self.rules.append(rule)

    def update_rule(self, rule_id, new_rule):
        """Updates an existing rule."""
        self.rules[rule_id] = new_rule

    def remove_rule(self, rule_id):
        """Removes a firewall rule."""
        del self.rules[rule_id]

    def get_rules(self):
        """Returns the current set of rules."""
        return self.rules

# Example usage
rule_manager = RuleManager()
rule_manager.add_rule({"src_ip": "192.168.1.1", "action": "block"})
print("Current rules:", rule_manager.get_rules())
