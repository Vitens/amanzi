from .model import Model
from .submodels.splitter import Splitter

class Recycle(Model, Splitter):
    parametric_model = ['recycle']

    def __init__(self, config, pp: dict = {}) -> None:
        super().__init__(config, pp)

        if pp:
            self.product_solution = pp.add_solution({})
            self.waste_solution = pp.add_solution({})
        
        print(self.parameters)

        self.split = self.parameters.get('recycle_efficiency', 0.8)

    

    def run_quality(self, type, total_inflow, solution):
        ## remove 95% of NaCl

        self.product_solution = solution.deepcopy()
        self.waste_solution = solution.deepcopy()
        return solution

    # Problem is that run_trace only happens for product, not waste
    @property
    def emitter_solutions(self):
        return {'product': self.product_solution,
                'waste': self.waste_solution}
    
    @property
    def mass(self):
        # recycle mass is 0 otherwise the model will not converge
        return {}