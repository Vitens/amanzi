from .model import Model
from .submodels.balance import Balance

class Plateaeration(Model, Balance):
    def __init__(self, config: dict = {}) -> None:
        super().__init__(config)
        self.config = config
        # self.settings = config['settings']
        # self.RQ = config['settings']['RQ']

    # def solve(self, influent = None) -> None:
    #     self.effluent = influent.copy().interact(self.gas_phase)
    
    # @property
    # def gas_phase(self):
    #     self.RQ = 0.6
    #     # air_composition = Database.get("air_composition", {})
    #     air_composition = {'Ntg(g)':0.79, 'O2(g)': 0.208,'CO2(g)':0.002}
    #     air_volume = self.inflow * self.RQ
    #     return self.pp.add_gas(air_composition, volume = air_volume)