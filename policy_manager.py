# PolicyManager.py
class PolicyManager:
    def __init__(self):
        self.policies = []

    def add_policy(self, policy):
        """Add a new policy."""
        self.policies.append(policy)

    def evaluate_policies(self, packet, user_info):
        """Evaluate policies against a packet and user information."""
        for policy in self.policies:
            if policy.matches(packet, user_info):
                return policy.action
        return "allow"
