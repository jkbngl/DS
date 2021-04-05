import connector
import utils
import pandas as pd


def query_builder(categories, timeframes, valCol, aggregationType, dateCol, table, condition):

    queries = []

    for col in categories:

        for timeframe in timeframes:
            queries.append(
                f'select {", ".join(col)}, {dateCol}, {aggregationType}({valCol}) as {valCol}  from {table} {condition} group by {", ".join(col)}, {dateCol} order by {dateCol} limit {timeframe}')
    return queries


def get_wheres(cols, table, where_condition, db_type):
    cursor = connector.getConnection(db_type)

    query = f'select distinct {", ".join(cols)} from {table} {where_condition}'

    print(query)

    cursor.execute(query)
    record = cursor.fetchall()
    result = utils.transformToKeyValue(cursor, record)

    cursor.close()

    return result


def where_builder(cols, table, where_condition, db_type):

    combinations_ = get_wheres(cols, table, where_condition, db_type)

    combinations = [
        {'site': 'BRU', 'orgarea': 'PMS', 'machinegroup': 'APH150'},
        {'site': 'BRU', 'orgarea': 'FTT', 'machinegroup': 'APH150'},
    ]

    keys = []
    queries = []

    for i in range(0, len(combinations[0].keys())):
        res = list(combinations[0].keys())[i]

        keys.append(res)

        df = pd.DataFrame(combinations)

        vals = df.drop_duplicates(keys)
        print('+++++++++')
        print(vals[keys])

        for index, row in vals.iterrows():
            query = 'where 1 = 1'

            print('~~~~~~~~~')
            print(row)

            for j, key in enumerate(keys):
                query += f" and {key} = '{row.get(key)}'"

            queries.append(query)

    print(queries)

    return queries
