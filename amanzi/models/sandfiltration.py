from .model import Model
from .submodels.loss import Loss

class Sandfiltration(Model, Loss):
    def __init__(self, config, pp):
        super().__init__(config, pp)
        # self.loss = config['configuration'].get('loss', 0.5)
        self.loss = 0.5
        self.load = 0
        self.waste_solution = None
    
    def run_model(self, type, total_inflow, solution):

        if(type == 'flush'):
            # add load to waste solution
            self.waste_solution = solution.copy().add('NaCl', self.load/total_inflow)
            return

        # total filter load
        self.load = total_inflow * solution.total('Na')*0.9

        # remove 90% 
        effluent = solution.remove('NaCl', 0.9*solution.total('Na'))
        # total load
        effluent.add('CaSO4', 10)

        # effluent.add('NaCl', 1)
        
        return effluent

    @property
    def emitter_solutions(self):
        return {'waste': self.waste_solution}


    @property
    def cost(self):
        return 250_000 # €

    @property
    def emission(self):
        return 500_000 # CO2eq

    @property    
    def energy(self):
        return 350_000 # kWh        