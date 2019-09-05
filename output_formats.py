import os
import numpy as np
import pandas as pd

output_folder = 'weka_files'

class ARFFFile:

    def __init__(self, dataset_name, model_name, selection_name, agg_name, reduce_name, df):
        self.dataset_name = dataset_name
        self.model_name = model_name
        self.selection_name = selection_name
        self.agg_name = agg_name
        self.reduce_name = reduce_name
        self.df = df

    def write_line(self, file, text):
        file.write("{}\n".format(text))

    def write_attributes(self, file):
        # Ignore file name and class value
        num_features = len(self.df.columns[:-2])

        for i in range(num_features):
            self.write_line(file, "@ATTRIBUTE x{} NUMERIC".format(i))

    def write_filename(self, file):
        self.write_line(file, "@ATTRIBUTE filename STRING")

    def write_class_attribute(self, file):
        class_vals = set()
        for i, row in self.df.iterrows():
            class_vals.add(row['class_val'])

        self.write_line(file, "@ATTRIBUTE class { " + ",".join(class_vals) + " }")

    def write_data(self, file):
        self.write_line(file, "\n\n@DATA")
        self.df['concat'] = pd.Series(self.df.values.tolist()).map(lambda x: ','.join(map(str,x)))
        for i, row in self.df.iterrows():
            self.write_line(file, row['concat'].replace(' ', '').replace(',', ''))

    def write_to_file(self):
        full_output_path = os.path.join(output_folder, self.dataset_name)
        if not os.path.exists(full_output_path):
            os.makedirs(full_output_path)

        filename = '{}_{}_{}_{}'.format(
            self.model_name, 
            self.selection_name, 
            self.agg_name,
            self.reduce_name)

        with open(os.path.join(output_folder, self.dataset_name, filename + ".arff"), mode='w') as open_file:
            # Write the relation header
            self.write_line(open_file, "@RELATION {}\n\n".format(filename))

            # Write each attribute
            self.write_attributes(open_file)

            # Write the filename
            self.write_filename(open_file)

            # Write the class attribute
            self.write_class_attribute(open_file)

            # Write the actual data
            self.write_data(open_file)
