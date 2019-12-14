import traceback
import os
import csv
import tempfile
import time
import random
import re
import json

from selection_methods import selection_methods
from agg_functions import all_func
from reduction_methods import reduction_methods
from common import common
from extractor import Extractor
from ClassPreprocessor import ClassPreprocessor
from aggregation_pipeline import AggregationPipeline
import pandas as pd
import numpy as np

dataset_dir = 'java_files'

SHOW_TOP_CONTEXTS = 10
MAX_PATH_LENGTH = 8
MAX_PATH_WIDTH = 2
EXTRACTOR_JAR_PATH = 'JavaExtractor/JPredict/target/JavaExtractor-0.0.1-SNAPSHOT.jar'
CLASS_PREPROCESS_JAR_PATH = 'java-tool.jar'
tmp_file_name = "tmpsnippet.java"

debug=True

class File2Vec:

    def __init__(self, config, model, model_info, data_dir, k=2000):
        self.model = model
        self.model_info = model_info
        self.config = config
        self.data_dir = data_dir
        self.path_extractor = Extractor(config,
                                        jar_path=EXTRACTOR_JAR_PATH,
                                        max_path_length=MAX_PATH_LENGTH,
                                        max_path_width=MAX_PATH_WIDTH)
        self.k = k

        self.class_preprocessor = ClassPreprocessor(CLASS_PREPROCESS_JAR_PATH, model_info['args'])

        self.duplicate = False
        # Set the flag to duplicate if our dataset is a duplicate
        if 'duplicate' in self.data_dir:
            self.duplicate = True

    def read_file(self, input_filename):
        with open(input_filename, 'r') as file:
            return file.readlines()

    def get_pair_num(self, file_name):
        res = re.match(r'(\d+)_\d', file_name)
        return res.group(1)

    def run(self):
        file_vectors = self.create_file_vectors()
        self.run_pipeline(file_vectors)

    def create_file_vectors(self):
        folder_dir = os.path.join(dataset_dir, self.data_dir)
        file_vectors = []
        fileNum = 0
        # Loop through each class value
        for class_val in os.listdir(folder_dir):
            # Get each file from each class
            class_folder = os.path.join(folder_dir, class_val)
            if os.path.isdir(class_folder):
                file_list = os.listdir(class_folder)

                # Limit the number of files per class
                if len(file_list) > self.k:
                    print("File list over the limit, randomly selecting {} files...".format(self.k))
                    random.seed(42)
                    file_list = random.sample(file_list, self.k)

                for file in file_list:
                    time0 = time.time()
                    method_vectors = []

                    # Split the file into its composing methods
                    methods = self.class_preprocessor.get_methods(os.path.join(class_folder, file))

                    # for each of it's composing methods
                    for method in methods:
                        # Get number of lines in the method
                        lines = method.count('\n')
                            
                        # Spit it into a temp file
                        try:
                            with open(tmp_file_name, mode='w') as tmp_file:
                                tmp_file.write(method)
                        except Exception as e:
                            if debug:
                                print("{}\n{}".format(e, method))
                        
                        # Make the predictions 
                        try:
                            predict_lines, hash_to_string_dict = self.path_extractor.extract_paths(tmp_file_name)
                        except ValueError as e:
                            print(e)
                            if debug:
                                print("Error for method {} in file {}".format(method, file))
                            continue

                        results, code_vectors = self.model.predict(predict_lines)
                        prediction_results = common.parse_results(results, hash_to_string_dict, topk=SHOW_TOP_CONTEXTS)

                        # Process the predictions
                        for i, method_prediction in enumerate(prediction_results):
                            method_vectors.append({"vector": code_vectors[i], "length": lines})
                        
                    file_vectors.append({'methods': method_vectors, 'class_val': class_val, 'filename': file,
                                        'processed': False})

                    print(fileNum, file, "Time:", time.time() - time0)
                    fileNum += 1
            
        os.remove(tmp_file_name)
        return file_vectors


    def get_num_columns(self, file_vectors):
        # Set up the dataframe values to hold the resulting dataset
        num_columns = 0
        for i in file_vectors:
            if 'attributes' in i:
                num_columns = len(i['attributes'])
                break

        return num_columns

    def get_by_filename(self, filename, file_vectors):
        for i in file_vectors:
            if i['filename'] == filename:
                return i

    def get_pair(self, file, file_vectors):
        if file['processed']:
            return None

        if not self.duplicate:
            file['processed'] = True
            return [file]

        # Now find this files duplicate pair
        pair_num = self.get_pair_num(file['filename'])
        pair_filename1 = '{}_1.java'.format(pair_num)
        pair_filename2 = '{}_2.java'.format(pair_num)

        file_obj_1 = self.get_by_filename(pair_filename1, file_vectors)
        file_obj_2 = self.get_by_filename(pair_filename2, file_vectors)

        file_obj_1['processed'] = True
        file_obj_2['processed'] = True

        return [file_obj_1, file_obj_2]

    def reset_file_vectors(self, file_vectors):
        for f in file_vectors:
            f['processed'] = False
            f.pop('attributes', None)

    def run_pipeline(self, file_vectors):
        for func in all_func:
            for selection_method in selection_methods:
                for reduction_method in reduction_methods:
                    print("Running {}, {}, {}".format(func.name(), selection_method.name(), reduction_method.name()))
                    pipeline = AggregationPipeline(
                        dataset_name=self.data_dir,
                        model_name=self.model_info['name'],
                        agg_function=func,
                        selection_method=selection_method,
                        reduction_method=reduction_method)

                    self.reset_file_vectors(file_vectors)

                    for file_ in file_vectors:
                        paired_files = self.get_pair(file_, file_vectors)
                        aggregated_vectors = []

                        # paired_files is None if we've already visited this file
                        if paired_files is not None:
                            for paired_file in paired_files:
                                # Apply the aggregation function now we have collected all the individual vectors from each method
                                aggregated = pipeline.aggregate_vectors(paired_file['methods'])
                                if len(aggregated) > 0:
                                    aggregated_vectors.append(aggregated)
                            
                            # Subtract the vectors for both files to give us our final vectors
                            # If we only have one file then just use that
                            # If we're in duplicate mode but we only get one of the two vectors then just ignore
                            if len(aggregated_vectors) > 0:                       
                                if self.duplicate and len(aggregated_vectors) == 2:
                                    file_['attributes'] = np.subtract(aggregated_vectors[0], aggregated_vectors[1])
                                elif not self.duplicate:
                                    file_['attributes'] = aggregated_vectors[0]
                                else:
                                    print(file_)

                    # Set up the dataframe values to hold the resulting dataset
                    columns = self.get_num_columns(file_vectors)
                            
                    col_names = ['x{}'.format(i) for i in range(columns)] + ['filename', 'class_val']

                    # Now we want to generate the dataframe from the aggregated results
                    rows_list = []
                    for file_ in file_vectors:
                        if 'attributes' in file_:
                            dict1 = {}

                            # Create the dict representing this file (row in the dataframe)
                            for i, val in enumerate(file_['attributes']):
                                this_col = col_names[i]
                                dict1[this_col] = val

                            dict1['filename'] = file_['filename']
                            dict1['class_val'] = file_['class_val']
                            rows_list.append(dict1)

                    df = pd.DataFrame(data=rows_list, columns=col_names)   

                    # Write the resulting vectors to an arff file
                    pipeline.process_dataset(df)
