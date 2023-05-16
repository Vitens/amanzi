from .model import Model
from .submodels.balance import Balance

class Ionexchange(Model, Balance):
    def __init__(self, config, pp):
        super().__init__(config, pp)
        # self.config = config
        self.configuration = config.get('configuration', {})
        # self.ion_exchange = self.configuration.get('ion_exchange', {'Na': 0.9, 'Cl': 0.9, 'Mg': 0.5, 'Ca': 0.5})
        self.iex_coefficients = self.configuration.get('iex_coefficients', {'Cl': 0.95, 'SO4': 0.9, 'NO3': 0.92, 'NO2':0.9})

        self.resin_capacity = self.configuration.get('resin_capacity', 10) #10kg default capacity
        self.resin_load = self.configuration.get('resin_load', 0)

        self.regenerations = 0
        
    def run_model(self, type, total_inflow, solution):
        return solution
        effluent = solution.copy()
        for el, ret in self.ion_exchange.items():
            pass
            effluent.change({el: solution.total(el, 'mmol') * ret}, 'mmol')
