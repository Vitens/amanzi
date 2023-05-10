from .model import Model
class Groundwater(Model):
    def __init__(self, config, pp):
        super().__init__(config, pp)
        self.constant = config['configuration'].get("production", 0)

        composition = self.config['configuration'].get('solution', {'Na':1, 'Cl':1, 'Mg': 10, 'Ca': 10}) 

        self.solution = self.pp.add_solution_simple(composition)
        self.emitter = True
    
    # @property
    # def mass(self):
    #     outflow = sum([c.flow for c in self.downstream_connections['product']])
    #     return self.solution.total('Na') * outflow

    @property
    def equations(self):
        return [ [ [self.downstream_connections['product'][0].eq(1)], self.constant] ]

    @property
    def emitter_solutions(self):
        return {'product': self.solution}

    @property
    def flow(self):
        """override model-flow with constant"""
        return self.constant