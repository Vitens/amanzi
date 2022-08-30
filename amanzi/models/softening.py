from .model import Model
from .submodels.balance import Balance

class Softening(Model, Balance):
    def __init__(self, config: dict) -> None:
        super().__init__(config)
        self.config = config

    # @property
    # def equations(self):
    #     equations = []
    #     # output_1 is equal to split * input
    #     equations.append([[c.eq(self.split) for c in self.connections['left']]+[c.eq(-1) for c in self.connections['right']], 0])
    #     # output_2 is equal to split * (1-input)
    #     equations.append([[c.eq(1-self.split) for c in self.connections['left']]+[c.eq(-1) for c in self.connections['bottom']], 0])
    #     return equations       