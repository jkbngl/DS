import iterator
import query_builder
import trend_detector
import pandas as pd

columns = ['itemgroup__category', 'workcenter__category',
           'orgarea__category', 'site__category', 'nqc__val', 'scrap__val', 'nqcmonthly__date', 'nqcdaily__date']

categoryCombinations = iterator.combinations(
    [col for col in columns if col.endswith('__category')])

valCols = [col for col in columns if col.endswith('__val')]
dateCols = [col for col in columns if col.endswith('__date')]

timeframes = [5, 14, 21, 30, 60, 90, 180]

queries = query_builder.query_builder(
    categoryCombinations, timeframes, valCols, dateCols)

for query in queries:
    # print(query)

    vals = [2, 3, 4, 4, 5, 4, 3, 5, 6, 7, 7, 8, 8, 8, 9, 11, 15]

    vals2 = [17.966, 30.548, 42.592, 46.975, 65.461, 142.632, ]

    vals3 = [17966, 42592, 46975, 65461, 142632, 75091, 33586, 41817, 43846, 70457, 18365, 51940, 109312, 80297, 56499, 23636, 27310, 48839, 72328, 19953, 33686, 35293, 23430, 17084, 37962, 14949, 8998, 34404, 72573,
             75547, 13698, 11832, 25428, 7239, 13846, 13238, 53536, 30211, 18364, 13289, 19175, 13002, 19909, 35429, 67286, 8107, 4127, 8662, 26335, 12137, 12064, 8416, 8984, 6221, 38691, 8507, 2522, 10210, 10527, 10775]

    s = pd.Series(vals3)

    s = s.rolling(10).mean()

    trend, h, p, z, Tau, s, var_s, slope, intercept = trend_detector.trend_detector(
        s)

    print(trend)
