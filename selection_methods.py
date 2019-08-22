import random
import numpy as np

class AbstractSelectionMethod:

  def __init__(self, vectors, max_num):
    self.vectors = vectors

    if len(self.vectors) < max_num:
      max_num = len(self.vectors)
    self.max_num = max_num

  def select(self, vectors):
    raise NotImplementedError


class SelectAll(AbstractSelectionMethod):

  def __init__(self, vectors):
    super().__init__(vectors, 999)

  def select(self):
    return [x['vector'] for x in self.vectors]

  @staticmethod
  def name():
    return "all"

class SelectRandomK(AbstractSelectionMethod):
  def __init__(self, vectors, k):
    super().__init__(vectors, k)

  def select(self):
    return [x['vector'] for x in random.sample(self.vectors, self.max_num)]

  @staticmethod
  def name():
    raise NotImplementedError

class SelectRandom1(SelectRandomK):

  def __init__(self, vectors):
    super().__init__(vectors, 1)

  @staticmethod
  def name():
    return "rand1"

class SelectRandom2(SelectRandomK):

  def __init__(self, vectors):
    super().__init__(vectors, 2)

  @staticmethod
  def name():
    return "rand2"

class SelectRandom3(SelectRandomK):

  def __init__(self, vectors):
    super().__init__(vectors, 3)

  @staticmethod
  def name():
    return "rand3"

class SelectRandom5(SelectRandomK):

  def __init__(self, vectors):
    super().__init__(vectors, 5)

  @staticmethod
  def name():
    return "rand5"

class SelectTopK(AbstractSelectionMethod):
  
  def __init__(self, vectors, k):
    super().__init__(vectors, k)

  def select(self):
    self.vectors.sort(key=lambda x: x['length'], reverse=True)
    return [x['vector'] for x in self.vectors[:self.max_num]]

  @staticmethod
  def name():
    raise NotImplementedError
  
class SelectTop1(SelectTopK):

  def __init__(self, vectors):
    super().__init__(vectors, 1)

  @staticmethod
  def name():
    return "top1"

class SelectTop2(SelectTopK):

  def __init__(self, vectors):
    super().__init__(vectors, 2)

  @staticmethod
  def name():
    return "top2"

class SelectTop3(SelectTopK):

  def __init__(self, vectors):
    super().__init__(vectors, 3)

  @staticmethod
  def name():
    return "top3"

class SelectTop5(SelectTopK):

  def __init__(self, vectors):
    super().__init__(vectors, 5)

  @staticmethod
  def name():
    return "top5"

selection_methods = [
  SelectAll
  # SelectRandom1,
  # SelectRandom2,
  # SelectRandom3,
  # SelectRandom5,
  # SelectTop1,
  # SelectTop2,
  # SelectTop3,
  # SelectTop5
]