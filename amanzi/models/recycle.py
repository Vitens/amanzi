from .model import Model
from .submodels.splitter import Splitter

class Recycle(Model, Splitter):
    parent_loop_count = 0
    
    def __init__(self, config, pp):
        super().__init__(config, pp)
        self.split = config['configuration'].get('fraction', 0.8)
        self.product_solution = None
        self.product_tracker = {}
    

    def run_model(self, type, total_inflow, solution):
        ## remove 95% of NaCl
        total = solution.total('Na')*total_inflow

        in_waste = (total*0.95) / ((1-self.split) * total_inflow)
        in_product = (total*0.05) / (self.split * total_inflow)

        self.product_solution = solution.copy().remove('NaCl', solution.total('Na') - in_product)
        self.product_tracker[Recycle.parent_loop_count] = self.product_solution
        Recycle.parent_loop_count += 1

        return solution.add('NaCl', in_waste - solution.total('Na'))

    @property
    def emitter_solutions(self):
        return {'product': self.product_solution}
    
    @property
    def mass(self):
        # recycle mass is 0 otherwise the model will not converge
        return {}

