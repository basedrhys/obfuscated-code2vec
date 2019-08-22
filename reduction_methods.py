import time
import numpy as np
import pandas as pd
from sklearn.datasets import fetch_mldata
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns
import umap

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
    return "none"

class AbstractUMap(AbstractReductionMethod):
  def __init__(self, df, k):
    # We can't have K be more than the # of instances
    if k > df.shape[0]:
      k = df.shape[0] - 2

    self.k = k
    return super().__init__(df)

  def reduce(self):
    reducer = umap.UMAP(n_components=self.k)

    embedding = reducer.fit_transform(self.df.iloc[:,:-1])

    # Convert the embedding (numpy array) back into a dataframe
    feat_cols = ["x{}".format(i) for i in range(embedding.shape[1])]

    return_df = pd.DataFrame(data=embedding, columns = feat_cols)
    return_df['class_val'] = self.df['class_val']
    
    return return_df

class UMapReduction25(AbstractUMap):
  def __init__(self, df):
    return super().__init__(df, 25)

  @staticmethod
  def name():
    return "UMap25"

class UMapReduction50(AbstractUMap):
  def __init__(self, df):
    return super().__init__(df, 50)

  @staticmethod
  def name():
    return "UMap50"

class UMapReduction100(AbstractUMap):
  def __init__(self, df):
    return super().__init__(df, 100)

  @staticmethod
  def name():
    return "UMap100"

class UMapReduction250(AbstractUMap):
  def __init__(self, df):
    return super().__init__(df, 250)

  @staticmethod
  def name():
    return "UMap250"

reduction_methods = [
  NoReduction,
  UMapReduction25,
  UMapReduction50,
  UMapReduction100,
  UMapReduction250
]


# n_cols = 362
# n_instances = 150

# cols = ['x{}'.format(x) for x in range(n_cols)]
# data = np.random.rand(n_instances, n_cols)

# labels = ['ok' if x < 100 else "not ok" for x in range(n_instances)]

# df = pd.DataFrame(data=data, columns=cols)
# df['class_val'] = labels

# umapTest = UMapReduction50(df)
# res = umapTest.reduce()
# umapTest = UMapReduction100(df)
# res = umapTest.reduce()
# print(res)
# umapTest = UMapReduction250(df)
# res = umapTest.reduce()
# print(res)
# pca_test = PCAReduction100(df)
# res = pca_test.reduce()

# print(res)

# new_arr = np.load('data.npy', allow_pickle=True)

# pca = PCAReduction(new_arr)
# pca.reduce()
