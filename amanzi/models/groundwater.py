from .model import Model
class Groundwater(Model):
    def __init__(self, config):
        super().__init__(config)
        self.constant = config['configuration'].get("production", 0)
        self.emitter = True
    
    # def run(self):
    #     for conn in self.downstream_connections:
    #         conn.solution = self.emitter_solution
    #     return

    @property
    def equations(self):
        return [ [ [self.connections['right'][0].eq(1)], self.constant] ]

    @property
    def emitter_solution(self):
        composition = self.config['configuration'].get('solution', {'Na':1, 'Cl':1})
        return self.pp.add_solution_simple(composition)

    @property
    def flow(self):
        return self.constant