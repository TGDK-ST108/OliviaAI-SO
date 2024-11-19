import logging
from typing import Dict, Any

class ExpressedObjectAttention:
    def __init__(self):
        logging.info("ExpressedObjectAttention initialized.")
    
    def apply_eight_vector_paraphrase(self, text: str, context_flags: Dict[str, bool]) -> str:
        """
        Apply an 8-vector paraphrase sequence based on context flags.
        
        Parameters:
        - text: The text to paraphrase.
        - context_flags: Dictionary of context flags that influence the paraphrase.
        
        Returns:
        - The paraphrased text.
        """
        logging.info(f"Applying 8-vector paraphrase to text: '{text}' with context flags: {context_flags}.")
        
        # Apply transformations based on context flags
        transformed_text = text
        for flag, is_active in context_flags.items():
            if is_active:
                transformed_text = self.vector_transformation(transformed_text, flag)
        
        return transformed_text
    
    def vector_transformation(self, text: str, flag: str) -> str:
        """
        Transform text based on a specific context flag.
        
        Parameters:
        - text: The text to transform.
        - flag: The context flag that determines the transformation.
        
        Returns:
        - The transformed text.
        """
        transformations = {
            'user': lambda t: f"[User] {t} - Enhanced",
            'request': lambda t: f"[Request] {t} - Urgent",
            'command': lambda t: f"[Command] {t} - Immediate",
            'implicitive': lambda t: f"[Implicitive] {t} - Consider",
            'directive': lambda t: f"[Directive] {t} - Follow",
            'suggestion': lambda t: f"[Suggestion] {t} - Consideration",
            'feedback': lambda t: f"[Feedback] {t} - Review",
            'observation': lambda t: f"[Observation] {t} - Note"
        }
        
        # Default transformation if flag is not found
        transform_func = transformations.get(flag, lambda t: f"[Generic] {t}")
        return transform_func(text)

# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    attention = ExpressedObjectAttention()
    
    # Context flags for paraphrasing
    context_flags = {
        'user': True,
        'request': False,
        'command': True,
        'implicitive': False,
        'directive': False,
        'suggestion': True,
        'feedback': False,
        'observation': False
    }
    
    # Apply 8-vector paraphrase
    original_text = "This needs immediate attention."
    paraphrased_text = attention.apply_eight_vector_paraphrase(original_text, context_flags)
    
    print("Paraphrased Text:", paraphrased_text)