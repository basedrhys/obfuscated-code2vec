import numpy as np

class AbstractVectorAggregator:

  def __init__(self, vectors):
    self.vectors = np.array(vectors)
    self.check_row_length()

  def aggregate(self):
    raise NotImplementedError

  def check_row_length(self):
    rows = self.vectors.shape[0]
    last_row_length = -1
    for x in range(0, rows):
      length = len(self.vectors[x])

      if last_row_length != -1 and length != last_row_length:
        raise Exception("Length of vectors are not all equal, vector: " + str(x))

      last_row_length = length

class VectorSum(AbstractVectorAggregator):

  def __init__(self, vectors):
    super().__init__(vectors)

  def aggregate(self):
    return np.sum(self.vectors, 0)

  @staticmethod
  def name():
    return "sum"

class VectorMean(AbstractVectorAggregator):

  def __init__(self, vectors):
    super().__init__(vectors)

  def aggregate(self):
    return np.mean(self.vectors, 0)

  @staticmethod
  def name():
    return "mean"

class VectorMax(AbstractVectorAggregator):

  def __init__(self, vectors):
    super().__init__(vectors)

  def aggregate(self):
    return np.max(self.vectors, 0)

  @staticmethod
  def name():
    return "max"

class VectorMin(AbstractVectorAggregator):

  def __init__(self, vectors):
    super().__init__(vectors)

  def aggregate(self):
    return np.min(self.vectors, 0)

  @staticmethod
  def name():
    return "min"

class VectorMed(AbstractVectorAggregator):

  def __init__(self, vectors):
    super().__init__(vectors)

  def aggregate(self):
    return np.median(self.vectors, 0)

  @staticmethod
  def name():
    return "med"

class VectorStdDev(AbstractVectorAggregator):

  def __init__(self, vectors):
    super().__init__(vectors)

  def aggregate(self):
    return np.std(self.vectors, 0)

  @staticmethod
  def name():
    return "std"

class VectorMaxMean(AbstractVectorAggregator):

  def __init__(self, vectors):
    super().__init__(vectors)

  def aggregate(self):
    return np.concatenate((
      np.max(self.vectors, 0), 
      np.mean(self.vectors, 0)), 
      axis=0)

  @staticmethod
  def name():
    return "maxMean"

class VectorMaxMed(AbstractVectorAggregator):

  def __init__(self, vectors):
    super().__init__(vectors)

  def aggregate(self):
    return np.concatenate((
      np.max(self.vectors, 0), 
      np.median(self.vectors, 0)), 
      axis=0)

  @staticmethod
  def name():
    return "maxMed"

class VectorMaxMin(AbstractVectorAggregator):

  def __init__(self, vectors):
    super().__init__(vectors)

  def aggregate(self):
    return np.concatenate((
      np.max(self.vectors, 0), 
      np.min(self.vectors, 0)), 
      axis=0)

  @staticmethod
  def name():
    return "maxMin"

class VectorMaxStdDev(AbstractVectorAggregator):

  def __init__(self, vectors):
    super().__init__(vectors)

  def aggregate(self):
    return np.concatenate((
      np.max(self.vectors, 0), 
      np.std(self.vectors, 0)), 
      axis=0)

  @staticmethod
  def name():
    return "maxstd"

class VectorMaxSum(AbstractVectorAggregator):

  def __init__(self, vectors):
    super().__init__(vectors)

  def aggregate(self):
    return np.concatenate((
      np.max(self.vectors, 0), 
      np.sum(self.vectors, 0)), 
      axis=0)

  @staticmethod
  def name():
    return "maxSum"

class VectorMeanMed(AbstractVectorAggregator):

  def __init__(self, vectors):
    super().__init__(vectors)

  def aggregate(self):
    return np.concatenate((
      np.mean(self.vectors, 0), 
      np.median(self.vectors, 0)), 
      axis=0)

  @staticmethod
  def name():
    return "meanMed"

class VectorMeanMin(AbstractVectorAggregator):

  def __init__(self, vectors):
    super().__init__(vectors)

  def aggregate(self):
    return np.concatenate((
      np.mean(self.vectors, 0), 
      np.min(self.vectors, 0)), 
      axis=0)

  @staticmethod
  def name():
    return "meanMin"

class VectorMeanStdDev(AbstractVectorAggregator):

  def __init__(self, vectors):
    super().__init__(vectors)

  def aggregate(self):
    return np.concatenate((
      np.mean(self.vectors, 0), 
      np.std(self.vectors, 0)), 
      axis=0)

  @staticmethod
  def name():
    return "meanstd"

class VectorMeanSum(AbstractVectorAggregator):

  def __init__(self, vectors):
    super().__init__(vectors)

  def aggregate(self):
    return np.concatenate((
      np.mean(self.vectors, 0), 
      np.sum(self.vectors, 0)), 
      axis=0)

  @staticmethod
  def name():
    return "meanSum"

class VectorMedMin(AbstractVectorAggregator):

  def __init__(self, vectors):
    super().__init__(vectors)

  def aggregate(self):
    return np.concatenate((
      np.median(self.vectors, 0), 
      np.min(self.vectors, 0)), 
      axis=0)

  @staticmethod
  def name():
    return "medMin"

class VectorMedStdDev(AbstractVectorAggregator):

  def __init__(self, vectors):
    super().__init__(vectors)

  def aggregate(self):
    return np.concatenate((
      np.median(self.vectors, 0), 
      np.std(self.vectors, 0)), 
      axis=0)

  @staticmethod
  def name():
    return "medstd"

class VectorMedSum(AbstractVectorAggregator):

  def __init__(self, vectors):
    super().__init__(vectors)

  def aggregate(self):
    return np.concatenate((
      np.median(self.vectors, 0), 
      np.sum(self.vectors, 0)), 
      axis=0)

  @staticmethod
  def name():
    return "medSum"

class VectorMinStdDev(AbstractVectorAggregator):

  def __init__(self, vectors):
    super().__init__(vectors)

  def aggregate(self):
    return np.concatenate((
      np.min(self.vectors, 0), 
      np.std(self.vectors, 0)), 
      axis=0)

  @staticmethod
  def name():
    return "minstd"

class VectorMinSum(AbstractVectorAggregator):

  def __init__(self, vectors):
    super().__init__(vectors)

  def aggregate(self):
    return np.concatenate((
      np.min(self.vectors, 0), 
      np.sum(self.vectors, 0)), 
      axis=0)

  @staticmethod
  def name():
    return "minSum"

class VectorStdDevSum(AbstractVectorAggregator):

  def __init__(self, vectors):
    super().__init__(vectors)

  def aggregate(self):
    return np.concatenate((
      np.std(self.vectors, 0), 
      np.sum(self.vectors, 0)), 
      axis=0)

  @staticmethod
  def name():
    return "stdSum"

class VectorMinMeanMax(AbstractVectorAggregator):

    def __init__(self, vectors):
        super().__init__(vectors)

    def aggregate(self):
        return np.concatenate((
            np.min(self.vectors, 0),
            np.mean(self.vectors, 0),
            np.max(self.vectors, 0)),
            axis=0)

    @staticmethod
    def name():
        return "minMeanMax"

# agg_functions2 = [fx.VectorMax, fx.VectorMean, fx.VectorMed, fx.VectorMin, fx.VectorStdDev, fx.VectorSum]

all_func = [
  VectorMinMeanMax,
  #VectorMax,
  #VectorMean,
  #VectorMed,
  #VectorMin,
  #VectorStdDev,
  #VectorSum,
  #VectorMaxMean,
  #VectorMaxMed,
  #VectorMaxMin,
  #VectorMaxStdDev,
  #VectorMaxSum,
  #VectorMeanMed,
  #VectorMeanMin,
  #VectorMeanStdDev,
  #VectorMeanSum,
  #VectorMedMin,
  #VectorMedStdDev,
  #VectorMedSum,
  #VectorMinStdDev,
  #VectorMinSum,
  #VectorStdDevSum,
]
