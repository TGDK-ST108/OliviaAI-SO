def categorize_willpower(data_list):
    """
    Categorize data based on willpower levels ('lower', 'upper', 'major').
    
    Arguments:
    - data_list: List of tuples, where each tuple contains the data and its willpower score.
                 Example: [("data1", 10), ("data2", 50), ("data3", 90)]
    
    Returns:
    - Categorized data with priority levels assigned ('lower', 'upper', 'major').
    """
    categorized_data = []
    
    # Define thresholds for willpower levels
    lower_threshold = 20
    upper_threshold = 60
    
    for data, score in data_list:
        if score <= lower_threshold:
            priority = "lower"
        elif score <= upper_threshold:
            priority = "upper"
        else:
            priority = "major"
        
        # Add the categorized data to the result
        categorized_data.append((data, priority, score))
    
    return categorized_data

# Example usage
data_input = [("data1", 10), ("data2", 50), ("data3", 90)]
categorized_data = categorize_willpower(data_input)

# Display categorized data
for data, priority, score in categorized_data:
    print(f"{data} - Priority: {priority}, Score: {score}")

def duoplex_algorithm(data_list):
    """
    Update DuoPlex algorithm to prioritize 'major' category data.
    
    Arguments:
    - data_list: List of tuples where each tuple contains data and its priority level
                 (e.g., [("data1", "major"), ("data2", "upper"), ("data3", "lower")])

    Returns:
    - Processed data based on priority.
    """
    # Define priority levels
    priority_order = {'major': 3, 'upper': 2, 'lower': 1}
    
    # Sort data based on priority, with 'major' having the highest priority
    sorted_data = sorted(data_list, key=lambda x: priority_order[x[1]], reverse=True)
    
    # Process data in sorted order (major first, then upper, then lower)
    processed_data = []
    for data, priority in sorted_data:
        # Simulating some processing on the data
        processed_data.append(f"Processed: {data} (Priority: {priority})")
    
    return processed_data

# Example usage
data_input = [("data1", "major"), ("data2", "upper"), ("data3", "lower")]
processed_data = duoplex_algorithm(data_input)
print(processed_data)

def duo_fold_algorithm(data_list):
    """
    Update Duo fold algorithm to prioritize 'major' category data.
    
    Arguments:
    - data_list: List of tuples where each tuple contains data and its priority level
                 (e.g., [("data1", "major"), ("data2", "upper"), ("data3", "lower")])

    Returns:
    - Folded data with priority-based processing.
    """
    # Define priority levels
    priority_order = {'major': 3, 'upper': 2, 'lower': 1}
    
    # Sort data based on priority
    sorted_data = sorted(data_list, key=lambda x: priority_order[x[1]], reverse=True)
    
    # Implement folding logic
    folded_data = []
    for data, priority in sorted_data:
        # Simulate folding logic by combining data iteratively
        folded_data.append(f"{data} folded (Priority: {priority})")
    
    return folded_data

# Example usage
data_input = [("data1", "major"), ("data2", "upper"), ("data3", "lower")]
folded_data = duo_fold_algorithm(data_input)
print(folded_data)