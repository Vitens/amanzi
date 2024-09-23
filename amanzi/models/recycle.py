from .model import Model
from .submodels.splitter import Splitter

class Recycle(Model, Splitter):
    parametric_model = ['recycle']

    def __init__(self, config, pp):
        super().__init__(config, pp)
        self.split = config.get('configuration', {}).get('fraction', 0.8)

        if pp:
            self.product_solution = pp.add_solution({})
    

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

