
class AbstractReductionMethod:

  def __init__(self, dataset):
    self.dataset = dataset

  def reduce():
    raise NotImplementedError


class NoReduction(AbstractReductionMethod):
  def __init__(self, dataset):
    return super().__init__(dataset)

  def reduce(self):
    return self.dataset

  @staticmethod
  def name():
    return "noReduction"