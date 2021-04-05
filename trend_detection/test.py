mydictionary = {'a': 'apple', 'b': 'bear', 'c': 'castle'}
keys = ['b', 'c']

values = list(map(mydictionary.get, keys))

print(values)
