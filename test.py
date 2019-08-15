from agg_functions import all_func
from selection_methods import all_methods
import numpy as np
import pandas as pd

# new_arr = np.load('data.npy', allow_pickle=True)

# print(new_arr)
num_columns = 20

row = [x for x in range(num_columns)] + ['opencv']
row2 = [x + 1 for x in range(num_columns)] + ['spring']

input_rows = [row, row2]
col_names = ['x_{}'.format(i) for i in range(num_columns)]
col_names.append('label')

rows_list = []
for row in input_rows:
        dict1 = {}
        # get input row in dictionary format
        # key = col_name
        for i, col in enumerate(col_names):
          dict1[col] = row[i]

        rows_list.append(dict1)

df = pd.DataFrame(data=rows_list, columns=col_names, index=range(len(input_rows))) 

print(df)
print(df.columns[-1])