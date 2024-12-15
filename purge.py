def purge_data_sources(database, blacklist_keywords):
    for keyword in blacklist_keywords:
        database.remove_entries(keyword)
    database.optimize()