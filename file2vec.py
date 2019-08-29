import traceback
import os
import csv
import tempfile
import time

from selection_methods import selection_methods
from agg_functions import all_func
from reduction_methods import reduction_methods
from common import common
from extractor import Extractor
from ClassPreprocessor import ClassPreprocessor
from aggregation_pipeline import AggregationPipeline
import pandas as pd
# from main import dataset_dir
dataset_dir = 'java_files'

SHOW_TOP_CONTEXTS = 10
MAX_PATH_LENGTH = 8
MAX_PATH_WIDTH = 2
EXTRACTOR_JAR_PATH = 'JavaExtractor/JPredict/target/JavaExtractor-0.0.1-SNAPSHOT.jar'
CLASS_PREPROCESS_JAR_PATH = 'ClassPreprocess.jar'
tmp_file_name = "tmpsnippet.java"

class File2Vec:

    def __init__(self, config, model, model_info, data_dir):
        self.model = model
        self.model_info = model_info
        self.config = config
        self.data_dir = data_dir
        self.path_extractor = Extractor(config,
                                        jar_path=EXTRACTOR_JAR_PATH,
                                        max_path_length=MAX_PATH_LENGTH,
                                        max_path_width=MAX_PATH_WIDTH)

        self.class_preprocessor = ClassPreprocessor(CLASS_PREPROCESS_JAR_PATH, model_info['obfuscated'])

    def read_file(self, input_filename):
        with open(input_filename, 'r') as file:
            return file.readlines()

    def run(self):
        file_vectors = self.create_file_vectors(self.data_dir)
        self.run_pipeline(file_vectors)

    def create_file_vectors(self, folder_dir):
        folder_dir = os.path.join(dataset_dir, folder_dir)
        file_vectors = []
        fileNum = 0
        # Loop through each class value
        for class_val in os.listdir(folder_dir):
            # Get each file from each class
            class_folder = os.path.join(folder_dir, class_val)
            if os.path.isdir(class_folder):
                for file in os.listdir(class_folder):
                    time0 = time.time()
                    method_vectors = []
                    # Split the file into its composing methods
                    methods = self.class_preprocessor.get_methods(os.path.join(folder_dir, class_val, file))

                    # for each of it's composing methods
                    for method in methods:
                        lines = method.count('\n')
                        # Spit it into a temp file
                        try:
                            with open(tmp_file_name, mode='w') as tmp_file:
                                tmp_file.write(method)
                        except Exception as e:
                            print("{}\n{}".format(e, method))
                        
                        # Make the predictions 
                        try:
                            predict_lines, hash_to_string_dict = self.path_extractor.extract_paths(tmp_file_name)
                        except ValueError as e:
                            print("Error for method {} in file {}".format(method, file))
                            continue

                        results, code_vectors = self.model.predict(predict_lines)
                        prediction_results = common.parse_results(results, hash_to_string_dict, topk=SHOW_TOP_CONTEXTS)

                        # Process the predictions
                        for i, method_prediction in enumerate(prediction_results):
                            method_vectors.append({"vector": code_vectors[i], "length": lines})
                        
                    file_vectors.append({'methods': method_vectors, 'class_val': class_val, 'filename': file})

                    print(fileNum, "Time:", time.time() - time0)
                    fileNum += 1
            
        os.remove(tmp_file_name)
        return file_vectors


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


                    # dataset = []

                    for file_ in file_vectors:
                        # Apply the aggregation function now we have collected all the individual vectors from each method
                        aggregated = pipeline.aggregate_vectors(file_['methods'])
                        if len(aggregated) > 0:
                            file_['attributes'] = aggregated
                            # dataset.append({'attributes': aggregated, 'class_val': file_vec['class_val'], 
                                # 'filename': file_vec['filename']})

                    # Set up the dataframe values to hold the resulting dataset
                    num_rows = len(file_vectors)
                    num_columns = len(file_vectors[0]['attributes'])
                    col_names = ['x{}'.format(i) for i in range(num_columns)] + ['filename', 'class_val']

                    # Now we want to generate the dataframe from the aggregated results
                    rows_list = []
                    for file_ in file_vectors:
                        dict1 = {}

                        # Create the dict representing this file (row in the dataframe)
                        for i, val in enumerate(file_['attributes']):
                            this_col = col_names[i]
                            dict1[this_col] = val

                        dict1['filename'] = file_['filename']
                        dict1['class_val'] = file_['class_val']
                        rows_list.append(dict1)

                    df = pd.DataFrame(data=rows_list, columns=col_names, index=range(num_rows))   

                    # with open('dataset.csv', newline='', mode='w') as out_file:
                    #     df.to_csv(out_file, index=False)

                    # Write the resulting vectors to an arff file
                    pipeline.process_dataset(df)