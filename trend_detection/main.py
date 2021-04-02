import iterator
import query_builder
import trend_detector
import pandas as pd
import connector
import utils


config = {
    'table': '-',
    'columns': ['-', '-'],
    'columns_level': [{'level': 1, 'key': '-'}, {'level': 2, 'key': '-'}],
    'valCol': '-',
    'aggregationType': 'sum',
    'dateCol': '-',
    'condition': "where - = '-'",
    'timeframes': [5, 14, 21, 30, 60, 90, 180],
    'db_type': 'postgres'
}

categoryCombinations = iterator.combinations(
    [col for col in config.get('columns') if col.endswith('__category')])


queries = query_builder.query_builder(
    categoryCombinations, config.get('timeframes'), config.get('valCol'), config.get('aggregationType'), config.get('dateCol'), config.get('table'), config.get('condition'))

for query in queries:
    print(query)

    cursor = connector.getConnection(config.get('db_type'))

    cursor.execute(query)
    record = cursor.fetchall()
    result = utils.transformToKeyValue(cursor, record)

    cursor.close()

    vals = [float(res.get(config.get('valCol'))) for res in result]
    s = pd.Series(vals)
    #s = s.rolling(10, min_periods=1).mean()

    trend, h, p, z, Tau, s, var_s, slope, intercept = trend_detector.trend_detector(
        s)

    print(s)
    print(trend)
