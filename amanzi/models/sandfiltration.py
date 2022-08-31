from .model import Model
from .submodels.loss import Loss

class Sandfiltration(Model, Loss):
    def __init__(self, config):
        super().__init__(config)
        self.loss = config['configuration'].get('loss', 0.1)
    
    @property
    def cost(self):
        return 250_000 # €

    @property
    def emission(self):
        return 500_000 # CO2eq

    @property    
    def energy(self):
        return 350_000 # kWh        