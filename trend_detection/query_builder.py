
def query_builder(categories, timeframes, valCols, dateCols):

    queries = []

    for col in categories:

        for val in valCols:
            for date in dateCols:
                for timeframe in timeframes:
                    queries.append(
                        f'select {", ".join(col)}, {", ".join(col)} from table group by {", ".join(col)} order by {date} limit {timeframe}')
    return queries
