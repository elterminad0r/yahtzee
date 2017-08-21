import collections

def mode(l):
    return collections.Counter(l).most_common[0]

def simple_alg():
    to_keep = []

    yield to_keep

    while True:
        rolls, sheet = yield
        best_type, freq = mode(rolls + to_keep)
