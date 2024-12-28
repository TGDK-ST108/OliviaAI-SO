def block_doe_queries(query):
    restricted_keywords = ["DOE", "Energy Department", "nuclear", "labs"]
    if any(keyword in query.lower() for keyword in restricted_keywords):
        return "Access Denied: Restricted Content"
    return process_query(query)

def block_doe_queries(query):
    restricted_keywords = ["DOE", "Energy Department", "nuclear", "labs"]
    if any(keyword in query.lower() for keyword in restricted_keywords):
        return "Access Denied: Restricted Content"
    return process_query(query)