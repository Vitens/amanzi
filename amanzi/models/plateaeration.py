from .model import Model

class Plateaeration(Model):
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



    @property
    def equations(self):
        # all ingoing streams must match all outgoing streams
        return [[[c.eq(1) for c in self.connections['left']]+[c.eq(-1) for c in self.connections['right']], 0]]

    