import traceback
import os
import csv
import tempfile

from selection_methods import all_methods
from agg_functions import all_func
from common import common
from extractor import Extractor
from ClassPreprocessor import ClassPreprocessor
from arff_file import ARFFFile
from aggregation_pipeline import AggregationPipeline

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
        file_vectors = []
        fileNum = 0
        # Loop through each class value
        for class_val in os.listdir(folder_dir):
            # Get each file from each class
            class_folder = os.path.join(folder_dir, class_val)
            if os.path.isdir(class_folder):
                for file in os.listdir(class_folder):
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
                        
                    file_vectors.append({'methods': method_vectors, 'class_val': class_val})

                    print(fileNum)
                    fileNum += 1
            
        os.remove(tmp_file_name)
        return file_vectors


    def run_pipeline(self, file_vectors):
        for func in all_func:
            for method in all_methods:
                print("Running {}, {}".format(func, method))
                pipeline = AggregationPipeline(
                    self.model_info['name'],
                    agg_function=func,
                    selection_method=method)
                
                dataset = []

                for file_vec in file_vectors:
                    # Apply the aggregation function now we have collected all the individual vectors from each method
                    aggregated = pipeline.aggregate_vectors(file_vec['methods'])
                    if len(aggregated) > 0:
                        dataset.append({'attributes': aggregated, 'class_val': file_vec['class_val']})
        
                # Write the resulting vectors to an arff file
                pipeline.process_dataset(dataset)