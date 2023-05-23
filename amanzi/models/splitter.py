from .model import Model
from .submodels.splitter import Splitter
 
class Splitter(Model, Splitter):
    def __init__(self, config, pp):
        super().__init__(config, pp)
        self.split = config['configuration'].get('fraction', 0.5)
        # self.split = 0.5
    #     self.product_solution = None

    # def run_model(self, type, total_inflow, solution):
    #     self.product_solution = solution.copy()
    #     return solution

    # @property
    # def emitter_solutions(self):
    #     return {'product': self.product_solution}
    
    # @property
    # def mass(self):
    #     # recycle mass is 0 otherwise the model will not converge
    #     return {}
