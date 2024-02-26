import itertools


a = [1, 2, 3, 4]

combinations = list(itertools.combinations(a, 2))
print(combinations)

combinations = list(itertools.dropwhile(lambda x: x[0] == 1, combinations))
print(combinations)