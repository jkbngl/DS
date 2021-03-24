def transformToKeyValue(cursor, record):
    
    data = []
    
    columnnames = [desc[0] for desc in cursor.description]

    # Create from the value array a key value object
    for row in record:
        cache = {}

        for i, columnname in enumerate(columnnames):
            cache[columnname] = row[i]

        data.append(cache)

    return data
