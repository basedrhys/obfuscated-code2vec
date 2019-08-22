import tensorflow as tf
import os
from common import Config, VocabType
from argparse import ArgumentParser
from file2vec import File2Vec
from model import Model

models = [
    {
        'location': 'models/pretrained/saved_model_iter8.release', 
        'name': 'pretr',
        'obfuscated': False
    }
    # {
    #     'location': 'models/obfuscated/saved_model_iter3.release', 
    #     'name': 'obfs',
    #     'obfuscated': True
    # },
    # {
    #     'location': 'models/obfuscated/saved_model_iter3.release', 
    #     'name': 'obfsn',
    #     'obfuscated': False
    # },
    ]
dataset_dir = 'java_files/test'

if __name__ == '__main__':
    # Loop through each model we have
    for modelDef in models:
        config = Config.get_default_config(modelDef['location'])

        modelObj = Model(config, modelDef['name'])
        modelObj.predict([])
        print('Created model')

        file2vec = File2Vec(config, modelObj, modelDef, dataset_dir)
        file2vec.run()

        modelObj.close_session()
        
        




# snippet_vectors = [[0.2152, 5215, 12], [1, 1, 1], [5211, 5.215, 5215]]

# for method in agg_methods:
#     vec = method(snippet_vectors)
#     print(vec.aggregate())
