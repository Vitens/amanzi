from .model import Model
from .submodels.splitter import Splitter

class Recycle(Model, Splitter):
    parametric_model = ['recycle']

    def __init__(self, config, pp: dict = {}) -> None:
        super().__init__(config, pp)
        self.configurations = config.get('configuration', {})
        self.split = self.configurations.get('fraction', 0.8)
        try:
            self.product_solution = pp.add_solution({})
        except:
            self.product_solution = None
    

    def run_quality(self, type, total_inflow, solution):
        ## remove 95% of NaCl
        self.product_solution = solution.copy()
        return solution

    @property
    def emitter_solutions(self):
        return {'product': self.product_solution}
    
    @property
    def mass(self):
        # recycle mass is 0 otherwise the model will not converge
        return {}

