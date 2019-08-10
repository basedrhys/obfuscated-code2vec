from agg_functions import all_func
from selection_methods import all_methods


vectors = []

vectors.append({'vector': [1, 2, 3, 7], 'length': 7})
vectors.append({'vector': [1, 2, 3, 4], 'length': 4})
vectors.append({'vector': [1, 2, 3], 'length': 3})
vectors.append({'vector': [1, 2, 3], 'length': 3})

for func in all_methods:
    agg = func(vectors)
    print(agg.name(), agg.select())