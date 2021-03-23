import itertools

stuff = ['itemgroup__category', 'workcenter__category',
         'orgarea__category', 'site__category', 'nqc__val', 'scrap__val', 'nqcc__date']
for L in range(0, len(stuff)+1):
    for subset in itertools.combinations(stuff, L):
        print(subset)
