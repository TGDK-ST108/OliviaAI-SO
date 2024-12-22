import math

def compute_sequence(r, underfold=1):
    # Constants
    factor = (9 - underfold) / 4
    scaling = 512
    adjust = -3
    
    # Calculation
    result = math.pi * (r ** 144) * factor
    result *= scaling
    result += adjust
    
    # Relinquish dead vectors (threshold example: < 0)
    if result < 0:
        return "Dead Vector", result
    
    # Return modular successionary sequence
    return "Active Vector", result

# Example with radius 2
radius = 2
status, sequence_value = compute_sequence(radius)
print(status, sequence_value)