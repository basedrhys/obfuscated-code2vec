import os
import pandas as pd

dataset_dir = 'java_files/'

output_dir = 'text_arff'

for dataset in os.listdir(dataset_dir):
    this_dataset_dir = os.path.join(dataset_dir, dataset)
    class_vals = os.listdir(this_dataset_dir)
    
    with open('{}/{}.arff'.format(output_dir, dataset), mode='w') as open_file:
        open_file.write("@RELATION {}\n\n".format(dataset))

        open_file.write("@ATTRIBUTE filetext STRING\n")
        open_file.write("@ATTRIBUTE class { " + ",".join(class_vals) + " }\n\n")

        open_file.write("@DATA\n")

        for class_val in os.listdir(this_dataset_dir):
            file_list = os.listdir(os.path.join(this_dataset_dir,class_val))

            for file_ in file_list:
                path = os.path.join(this_dataset_dir, class_val, file_)
                
                try:
                    with open(path) as file_string:
                        file_repr = repr(file_string.read())
                except:
                    pass

                open_file.write("{},{}\n".format(file_repr, class_val))