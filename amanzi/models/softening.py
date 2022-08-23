from .model import Model
import pandas as pd
import sys

class Softening(Model):
    def __init__(self, config: dict, split=0.5) -> None:
        super().__init__(config)
        # self.name = type(self).__name__.lower()
        # self.n_units = configuration['n_units']         
        self.config = config
        self.split = split

    @property
    def equations(self):
        equations = []
        # output_1 is equal to split * input
        equations.append([[c.eq(self.split) for c in self.connections['left']]+[c.eq(-1) for c in self.connections['right']], 0])
        # output_2 is equal to split * (1-input)
        equations.append([[c.eq(1-self.split) for c in self.connections['left']]+[c.eq(-1) for c in self.connections['bottom']], 0])
        return equations       