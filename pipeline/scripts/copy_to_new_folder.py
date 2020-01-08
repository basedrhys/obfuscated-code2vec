'''
Create the reduced dataset - if a file exists in the obfuscated folder, 
copy the original file (not obfuscated) to the target folder
'''


import os
from shutil import copyfile

source_folder = '' # original folder of java files
target_folder = '' # where do we want them to be copied to
obfuscated_folder = '' # the folder of obfuscated files

file_count = 0

def walk_dir(dir_name):
  src_dir = os.path.join(source_folder, dir_name)
  for item in os.listdir(src_dir):
    full_src_item = os.path.join(src_dir, item)

    if os.path.isdir(full_src_item):
      target_item = os.path.join(target_folder, dir_name, item)
      if not os.path.exists(target_item):
        os.mkdir(target_item)

      new_dir = os.path.join(dir_name, item)
      walk_dir(new_dir)

    # else copy the file into the new folder
    else:
      obfs_file = os.path.join(obfuscated_folder, dir_name, item)
      if os.path.exists(obfs_file):
        file_path = os.path.join(dir_name, item)
        copy_to_target(file_path)

def copy_to_target(path):
  global file_count
  print("Copying file {}".format(file_count))
  src_file = os.path.join(source_folder, path)
  target_file = os.path.join(target_folder, path)
  copyfile(src_file, target_file)
  file_count += 1

walk_dir('')