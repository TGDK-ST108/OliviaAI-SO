def detect_anomaly(access_pattern, modification_trail, context_history):
    """Enhanced anomaly detection."""
    access_score = sum(access_pattern)
    suspicious_modifications = modification_trail.count("delete")

    # Context-aware threshold adjustment
    threshold = 20 + len(context_history) * 0.5  # Example: dynamic adjustment based on history

    if access_score > threshold or suspicious_modifications > 1:
        return True  # Anomaly detected
    return False