import connector
import utils
import pandas as pd


def get_wheres(cols, table, where_condition, db_type):
    cursor = connector.getConnection(db_type)

    query = f'select distinct {", ".join(cols)} from {table} {where_condition}'

    print(query)

    cursor.execute(query)
    record = cursor.fetchall()
    result = utils.transformToKeyValue(cursor, record)

    cursor.close()

    return result


def where_builder(cols, table, condition, dateCol, valCols, timeframes, db_type):

    combinations = get_wheres(cols, table, condition, db_type)

    print(combinations)

    keys = []
    queries = []

    # All possible columns, start with 1 and go up to the last, always adding columns
    for i in range(0, len(combinations[0].keys())):
        res = list(combinations[0].keys())[i]

        keys.append(res)

        df = pd.DataFrame(combinations)

        vals = df.drop_duplicates(keys)

        print(f'UNIQUE on level ({len(keys)})')
        print(len(vals))

        # The unique vals per key have been calculated, create the queries per combinatio
        for index, row in vals.iterrows():

            print(index)

            for timeframe in timeframes:

                for vcol in valCols:
                    query = f'select {", ".join(keys)}, {dateCol}, {vcol.get("agg")}({vcol.get("col")}) as {vcol.get("col")} from {table} {condition} '

                # Add multiple and conditions for multiple keys
                for j, key in enumerate(keys):
                    query += f" and {key} = '{row.get(key)}'"

                query += f' group by {", ".join(keys)}, {dateCol} order by {dateCol} limit {timeframe}'

            queries.append(query)

    return queries
