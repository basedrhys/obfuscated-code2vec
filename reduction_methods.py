import time
import numpy as np
import pandas as pd
from sklearn.datasets import fetch_mldata
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns

# import the main drawing library
from matplotlib.widgets import Button
from matplotlib.text import Annotation


class AbstractReductionMethod:

  def __init__(self, df):
    self.df = df

  def reduce():
    raise NotImplementedError


class NoReduction(AbstractReductionMethod):
  def __init__(self, df):
    return super().__init__(df)

  def reduce(self):
    return self.df

  @staticmethod
  def name():
    return "noReduction"

class PCAReduction(AbstractReductionMethod):
  def __init__(self, dataset):
    return super().__init__(dataset)

  def reduce(self):
    # Create a dataframe from the dataset
    return self.df

# new_arr = np.load('data.npy', allow_pickle=True)

# pca = PCAReduction(new_arr)
# pca.reduce()
