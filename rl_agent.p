import numpy as np
from collections import defaultdict

class SecurityRLAgent:
    def __init__(self, adaptive_tuner):
        self.adaptive_tuner = adaptive_tuner
        self.q_table = defaultdict(lambda: np.zeros(2))  # Actions: [Block, Allow]
        self.learning_rate = 0.1
        self.discount_factor = 0.9

    def choose_action(self, state):
        return np.argmax(self.q_table[state])

    def update_policy(self, state, action, reward, next_state):
        old_value = self.q_table[state][action]
        next_max = np.max(self.q_table[next_state])
        self.q_table[state][action] = old_value + self.learning_rate * (reward + self.discount_factor * next_max - old_value)
        logger.info(f"Updated Q-table for state-action pair ({state}, {action})")

    def adaptive_defense(self, state, action):
        if action == 0:  # Block action
            self.adaptive_tuner.base_threshold += 0.05
        else:  # Allow action
            self.adaptive_tuner.base_threshold -= 0.05
        return self.adaptive_tuner.base_threshold
