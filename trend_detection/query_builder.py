
columns = ['itemgroup__category', 'workcenter__category',
           'orgarea__category', 'site__category', 'nqc__val', 'scrap__val', 'nqcc__date']

timeframes = [5, 14, 21, 30, 60, 90, 180]

for col in columns:
    if col.endswith('__category'):
        for pos in columns:

            vals = [valCol for valCol in columns if valCol.endswith('__val')]
            dates = [valCol for valCol in columns if valCol.endswith('__date')]

            if pos.endswith('__category') and pos != col:

                for val in vals:

                    for date in dates:

                        for timeframe in timeframes:
                            print(
                                f'select {col}, {pos}, {val} from table group by {col}, {pos} order by {date} limit {timeframe}')
