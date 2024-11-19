import logging
from collections import deque

class ButtonSequencer:
    def __init__(self, sequence_length=10):
        self.sequence_length = sequence_length
        self.sequence = deque(maxlen=sequence_length)
        logging.info(f"ButtonSequencer initialized with sequence length: {sequence_length}")

    def add_button_press(self, button_id):
        """Add a button press to the sequence."""
        self.sequence.append(button_id)
        logging.info(f"Button press added: {button_id}")

    def get_sequence(self):
        """Get the current button sequence."""
        logging.info(f"Retrieved button sequence: {list(self.sequence)}")
        return list(self.sequence)

    def reset_sequence(self):
        """Reset the button sequence."""
        self.sequence.clear()
        logging.info("Button sequence reset.")

    def analyze_sequence(self):
        """Analyze the button sequence."""
        # Placeholder for sequence analysis logic
        analysis_result = {
            "sequence": list(self.sequence),
            "length": len(self.sequence),
            "unique_buttons": len(set(self.sequence))  # Example additional analysis
        }
        logging.info(f"Sequence analysis result: {analysis_result}")
        return analysis_result

    def set_sequence_length(self, new_length):
        """Set a new length for the button sequence."""
        if new_length <= 0:
            logging.error("Attempted to set a non-positive sequence length.")
            raise ValueError("Sequence length must be positive.")
        self.sequence_length = new_length
        self.sequence = deque(self.sequence, maxlen=new_length)  # Adjust deque size
        logging.info(f"Button sequence length updated to: {new_length}")

    def get_sequence_length(self):
        """Get the current length of the button sequence."""
        logging.info(f"Current button sequence length: {self.sequence_length}")
        return self.sequence_length