import iterator
import query_builder
import trend_detector
import pandas as pd
import connector
import utils


config = {
    'table': 'ffd.act_data',
    'columns_level': [{'level': 1, 'key': 'level1'}, {'level': 2, 'key': 'level2'}, {'level': 3, 'key': 'level3'}],
    'valCols': [{'col': 'bobo', 'agg': 'sum'}, {'col': 'amount', 'agg': 'sum'}],
    'dateCol': "data_date",
    'condition': "where year > 2018",
    'timeframes': [5, 30, 90],
    'db_type': 'postgres',
    'columns': ['level1', 'level2'],
}


cols = config.get('columns')
table = config.get('table')
condition = config.get('condition')
dateCol = config.get('dateCol')
valCols = config.get('valCols')
timeframes = config.get('timeframes')
db_type = config.get('db_type')


queries = query_builder.where_builder(
    cols, table, condition, dateCol, valCols, timeframes, db_type)


print('#')
print(queries)

for query in queries:

    cursor = connector.getConnection(config.get('db_type'))

    cursor.execute(query)
    record = cursor.fetchall()
    result = utils.transformToKeyValue(cursor, record)

    cursor.close()

    # Check this for change in valcol
    for i, col in enumerate(valCols):
        key = result[0].get(col.get('col'))

        if key:
            vals = [float(key) for res in result]
            break

    s = pd.Series(vals)
    s = s.rolling(10, min_periods=1).mean()

    if len(s) > 1:
        try:
            trend, h, p, z, Tau, s, var_s, slope, intercept = trend_detector.trend_detector(
                s)

            if h:
                print(query)
                print(trend)
        except Exception as e:
            print(f"ERROR {e} with {len(s)} records for query {query}")
    else:
        # Cant calculate any trend with 1 record
        pass
