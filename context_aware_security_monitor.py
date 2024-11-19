import logging

class ContextAwareSecurityModule:
    def __init__(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def assess_context(self, user, action):
        """Assess the security context based on user and action."""
        logging.info(f"Assessing context for user: {user}, action: {action}")
        if self.is_high_risk_action(action):
            logging.warning(f"High-risk action detected for user: {user}!")
            return False
        return True

    def is_high_risk_action(self, action):
        """Determine if the action is high risk."""
        high_risk_actions = ["delete", "modify"]
        return action in high_risk_actions

# Example usage
if __name__ == "__main__":
    security_module = ContextAwareSecurityModule()
    is_safe = security_module.assess_context(user="Alice", action="delete")
    print("Is action safe?", is_safe)
