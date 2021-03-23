import iterator


columns = ['itemgroup__category', 'workcenter__category',
           'orgarea__category', 'site__category', 'nqc__val', 'scrap__val', 'nqcc__date']

categoryCombinations = iterator.combinations(
    [col for col in columns if col.endswith('__category')])

print(categoryCombinations)

timeframes = [5, 14, 21, 30, 60, 90, 180]

for col in categoryCombinations:

    vals = [valCol for valCol in columns if valCol.endswith('__val')]
    dates = [valCol for valCol in columns if valCol.endswith('__date')]

    for val in vals:

        for date in dates:

            for timeframe in timeframes:
                print(
                    f'select {", ".join(col)}, {val} from table group by {", ".join(col)} order by {date} limit {timeframe}')
