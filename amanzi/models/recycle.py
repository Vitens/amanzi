from .model import Model
from .submodels.splitter import Splitter

class Recycle(Model, Splitter):
    def __init__(self, config):
        super().__init__(config)
        self.split = config['configuration'].get('fraction', 0.5)
    
    # @property
    # def equations(self):
    #     equations = []
    #     # output_1 is equal to split * input
    #     equations.append([[c.eq(self.split) for c in self.connections['left']]+[c.eq(-1) for c in self.connections['right']], 0])
    #     # output_2 is equal to split * (1-input)
    #     equations.append([[c.eq(1-self.split) for c in self.connections['left']]+[c.eq(-1) for c in self.connections['bottom']], 0])
    #     return equations
