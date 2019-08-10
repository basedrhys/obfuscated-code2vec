import os
from shutil import copyfile

source_folder = '/Users/rhyscompton/Documents/java_datasets/java-xs'
target_folder = '/Users/rhyscompton/Documents/java_datasets/java-xs-new'
obfuscated_folder = '/Users/rhyscompton/Documents/java_datasets/java-xs-obfs'

files = []
# r=root, d=directories, f = files
for r, d, f in os.walk(source_folder):
    for file in f:
        # Is this file in the obfuscated folder?
        obfuscated_file = os.path.join(obfuscated_folder, r, file)

        print(obfuscated_folder, r, file)
        # print(source_folder, r)
        # If it is, then copy it to the target folder
        if os.path.exists(obfuscated_file) and f != ".DS_STORE":
            target_file = os.path.join(target_folder, r, file)

            print(target_file)
            # print(source_folder, d, file)

            # copyfile(source_file, target_file)
