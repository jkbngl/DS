
def query_builder(categories, timeframes, valCol, aggregationType, dateCol, table, condition):

    queries = []

    for col in categories:

        for timeframe in timeframes:
            queries.append(
                f'select {", ".join(col)}, {dateCol}, {aggregationType}({valCol}) as {valCol}  from {table} {condition} group by {", ".join(col)}, {dateCol} order by {dateCol} limit {timeframe}')
    return queries


def where_builder(cols, table, where_condition):

    query = f'select distinct {", ".join(cols)} from {table} {where_condition}'

    return []
