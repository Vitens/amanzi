from .model import Model
class Groundwater(Model):
    def __init__(self, config):
        super().__init__(config)
        self.constant = config['configuration'].get("production", 0)
        self.emitter = True

    @property
    def equations(self):
        return [ [ [self.connections['right'][0].eq(1)], self.constant] ]

    @property
    def emitter_solution(self):
        composition = self.config['configuration'].get('solution', {'Na':1, 'Cl':1}) #tijdelijk omdat concentratie nog niet in front-end-config stond
        return self.pp.add_solution_simple(composition)

    @property
    def flow(self):
        """override model-flow with constant"""
        return self.constant