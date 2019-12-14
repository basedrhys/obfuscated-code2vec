# Obsucated code2vec: Reducing Model Bias by Hiding Information

![Overall project view](img/overall.png)

Code for the paper: *Obsucated code2vec: Improving Generalisation by Hiding Information*

This repository contains code for the dataset pipeline, as well as the obfuscation tool used for obfuscating the datasets.

All of the model-related code (`common.py`, `model.py`, `PathContextReader.py`) as well as the `JavaExtractor` folder is code from the original [code2vec repository](https://github.com/tech-srl/code2vec). This was used for invoking the trained code2vec models to create method embeddings.

All models/datasets are on the paper google drive folder
https://drive.google.com/drive/u/1/folders/1CXgSXKf292BTlryASui2kBvYvJSvFnWN

## Requirements
- Java 8+
- Python 3

## Usage - Obfuscator
These steps should all be run from within the `java-obfuscator/` directory.
1. Locate a folder of `.java` files (e.g., from the [code2seq](https://github.com/tech-srl/code2seq) repository)
2. Alter the input and output directories in `obfs-script.sh`, as well as the number of threads of your machine. If you're running this on a particularly large folder (e.g., millions of files) then you may need to increase the `NUM_PARTITIONS` to 3 or 4, otherwise memory issues can occur, grinding the obfuscator to a near halt.
3. Run `obfs-script.sh` i.e. `$ source obfs-script.sh`

This will result in a new obfuscated folder of `.java` files, that can be used to train a new obfuscated code2vec model (or any model that performs learning from source code for that matter).

## Usage - Dataset Pipeline

![Dataset Pipeline View](img/pipeline.png)

These steps will convert a dataset of `.java` files into a numerical form (`.arff` by default), that can then be used with any standard WEKA classifier.

These steps should all be run from within the `pipeline/` directory of this repository.
To run the dataset pipeline and create class-level embeddings for a dataset of Java files:
1. `cd pipeline`
2. `pip install -r requirements.txt`
1. Download a `.java` dataset (from the datasets supplied or your own) and put in the `java_files/` directory
2. Download a code2vec model checkpoint and put the checkpoint folder in the `models/` directory
3. Change the paths and definitions in `model_defs.py` and number of models in `scripts/create_datasets.sh` to match your setup
4. Run `create_datasets.sh` (`source scripts/create_datasets.sh`). This will loop through each model and create class-level embeddings for the supplied datasets. The resulting datasets will be in `.arff` format in the `weka_files/` folder. 

You can now perform class-level classification on the dataset using any off-the-shelf classifier.

### Config
By default the pipeline will use the full range of values for each parameter, which creates a huge number of resulting `.arff` datasets (>1000). To reduce the number of these, remove (or comment out) some of the items in the arrays in `reduction_methods.py` and `selection_methods.py` (at the end of the file). Our experiments showed that the `SelectAll` selection method and `NoReduction` reduction method performed best in most cases so you may want to just keep these.

## Datasets

For embedding visualisations, the UMAP option (in the projector) usually shows the most interesting results.
The `.java` files are all [available for download](https://drive.google.com/drive/u/1/folders/1HALdnw8GO62HmYoGWxa4aX3XToEXAoGk). 
### OpenCV/Spring

2 categories, 305 instances

[Google Drive Link](https://drive.google.com/open?id=1WenQenDHMNOfQl_h0OaC25MHMNQF4xmS)

[Embedding Visualisation](http://projector.tensorflow.org/?config=https://gist.githubusercontent.com/basedrhys/fbb71520686db5e748e8681de112407c/raw/3900fd07bdc4441cf66f69c4e710611dd7fcecd9/opencv_config.json)

![OpenCV/Spring Visualisation](img/vis_opencv.png)

### Algorithm Classification

7 categories, 182 instances

[Google Drive Link](https://drive.google.com/open?id=16NPxqFEwkPFezSiZ1Ln6a_NoQWqaV6hy)

[Embedding Visualisation](http://projector.tensorflow.org/?config=https://gist.githubusercontent.com/basedrhys/5660cf47252411bdf83e4ff4f877f02a/raw/8e53136f79251fdce82524d9fc6539c039f9be63/algorithm_config.json)

![Algorithm Classification Visualisation](img/vis_algorithm.png)

### Code Author Attribution

13 categories, 1062 instances

This dataset was collected using the [github-scraper](https://github.com/basedrhys/github-scraper) python tool, which makes it easy to download specific types of files from github repos (`.java` files in this case).

[Google Drive Link](https://drive.google.com/open?id=1IC0Nxeew73p9yvfhKcKH-6mxW8nHGyfn)

[Embedding Visualisation](http://projector.tensorflow.org/?config=https://gist.githubusercontent.com/basedrhys/36fcd8653f2d759a8f1b03e56502a58e/raw/7d2ddef1c219d4fad7a49cc2c978d1ff4e25e5f1/author_config.json)

![Algorithm Classification Visualisation](img/vis_authors.png)

### Bug Detection

2 categories, 3344 instances

[Google Drive Link](https://drive.google.com/open?id=1KXGIDg9fJf334D967Md22bUai_41IZl1)

### Duplicate File Detection

2 categories, 1669 instances

[Google Drive Link](https://drive.google.com/open?id=1xkHyN-Jet8y8cNEQvX3Uf0s5ZdUWmcV5)

### Duplicate Function Detection

2 categories, 1277 instances

[Google Drive Link](https://drive.google.com/open?id=1_0Ai-DzotMtehcYkIRmNLq66-ZfAckuS)

### Malware Classification 

3 categories, 4891 instances

Can't share dataset for security reasons, you can request it from the original authors: http://amd.arguslab.org/