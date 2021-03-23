import itertools


def combinations(cols):
    stuff = []

    for L in range(0, len(cols)+1):
        for subset in itertools.combinations(cols, L):

            if len(list(subset)) > 0:
                stuff.append(list(subset))

    return stuff
