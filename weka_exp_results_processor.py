import os
import pandas as pd

results_loc = '/Users/rhyscompton/Dropbox/Honours_staging/datasets/opencv_spring/arff_files'

df = pd.DataFrame(columns=['model', 'selection_method', 'agg_method', 'accuracy'])

for f in os.listdir(files_loc):
    print(f)
