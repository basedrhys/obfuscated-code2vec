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
    return "none"

class AbstractPCA(AbstractReductionMethod):
  def __init__(self, df, k):
    self.k = k
    return super().__init__(df)

  def reduce(self):
    feat_cols = self.df.columns[:-1]  

    pca = PCA(self.k)
    pca_result = pca.fit_transform(self.df[feat_cols].values)

    print("{} components explain {} variance"
    .format(self.k, np.sum(pca.explained_variance_ratio_)))

    # Construct the new dataframe from the reduced dimensions
    new_cols = ['x{}'.format(i) for i in range(self.k)]
    new_df = pd.DataFrame(data=pca_result, columns=new_cols)
    new_df['class_val'] = self.df['class_val']

    return new_df

class PCAReduction50(AbstractPCA):
  def __init__(self, df):
    return super().__init__(df, 50)

  @staticmethod
  def name():
    return "PCA50"

class PCAReduction100(AbstractPCA):
  def __init__(self, df):
    return super().__init__(df, 100)

  @staticmethod
  def name():
    return "PCA100"


# n_cols = 500
# n_instances = 200

# cols = ['x{}'.format(x) for x in range(n_cols)]
# data = np.random.rand(n_instances, n_cols)

# labels = ['ok' for x in range(n_instances)]

# df = pd.DataFrame(data=data, columns=cols)
# df['class_val'] = labels


# pca_test = PCAReduction100(df)
# res = pca_test.reduce()

# print(res)

# new_arr = np.load('data.npy', allow_pickle=True)

# pca = PCAReduction(new_arr)
# pca.reduce()
