from .model import Model
from .submodels.loss import Loss

class Sandfiltration(Model, Loss):
    def __init__(self, config):
        super().__init__(config)
        self.loss = config['configuration'].get('loss', 0.1)
    
    # @property
    # def equations(self):
    #     equations = []
        
    #     eq1 = [c.eq(1) for c in self.connections['left']]
    #     eq2 = [c.eq(-1) for c in self.connections['right']]
    #     equations.append([ eq1 + eq2, 0])
        
    #     # backwash in equals loss times sum of inputs
    #     eq3 = [c.eq(self.loss) for c in self.connections['left']]
    #     eq4 = [c.eq(-1) for c in self.connections.get("top",[])]        
    #     equations.append([eq3 + eq4, 0])
        
    #     # backwash out equals loss times sum of inputs
    #     eq5 = [c.eq(self.loss) for c in self.connections['left']]
    #     eq6 = [c.eq(-1) for c in self.connections.get("bottom",[])]
    #     equations.append([ eq5 + eq6, 0])
        
    #     return equations            
            
    @property
    def cost(self):
        return 250_000 # €

    @property
    def emission(self):
        return 500_000 # CO2eq

    @property    
    def energy(self):
        return 350_000 # kWh        