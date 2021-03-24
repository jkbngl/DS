import iterator
import query_builder
import trend_detector
import pandas as pd
import connector
import utils

table = '-'

columns = ['-', '-']
categoryCombinations = iterator.combinations([col for col in columns if col.endswith('__category')])

valCol = '-'
aggregationType = 'sum'
dateCol = '-'

condition = "where - = '-'"

timeframes = [5, 14, 21, 30, 60, 90, 180]

queries = query_builder.query_builder(
   categoryCombinations, timeframes, valCol, aggregationType, dateCol, table, condition)

for query in queries:
    print(query)

    cursor = connector.getConnection()

    cursor.execute(query)
    record = cursor.fetchall()
    result = utils.transformToKeyValue(cursor, record)

    cursor.close()

    vals = [float(res.get(valCol)) for res in result]
    s = pd.Series(vals)
    #s = s.rolling(10, min_periods=1).mean()

    trend, h, p, z, Tau, s, var_s, slope, intercept = trend_detector.trend_detector(s)

    print(s)
    print(trend)
