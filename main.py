import tensorflow as tf
import os
from common import Config, VocabType
from argparse import ArgumentParser
from file2vec import File2Vec
from model import Model
from sys import argv
from model_defs import models

dataset_dir = 'java_files/'

if __name__ == '__main__':
    # Get the model for this session
    modelDef = models[int(argv[1])]
    print("\n\nRunning model:", modelDef['name'],'\n\n')
    config = Config.get_default_config(modelDef['location'])

    modelObj = Model(config, modelDef['name'])
    modelObj.predict([])
    print('Created model')

    # For each dataset in our collection of them, run the model on it
    for dataset in os.listdir(dataset_dir):
        print("Processing dataset:", dataset)
        file2vec = File2Vec(config, modelObj, modelDef, dataset)
        file2vec.run()

    modelObj.close_session()