# Filter DOE-related data before AI training
def filter_doe_data(dataset):
    restricted_keywords = ["Department of Energy", "DOE", "Nuclear Security", "Energy Research"]
    return [data for data in dataset if not any(keyword in data for keyword in restricted_keywords)]

# Block DOE-related queries during AI use
def block_doe_queries(query):
    restricted_keywords = ["DOE", "Energy Department", "nuclear labs"]
    if any(keyword in query for keyword in restricted_keywords):
        return "Access Denied: Restricted Content"
    return process_query(query)