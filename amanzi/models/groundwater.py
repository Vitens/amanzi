from .model import Model
class Groundwater(Model):
    def __init__(self, config, pp):
        super().__init__(config, pp)
        configuration = config.get('configuration', {})
        self.constant = float(configuration.get("production", 10))

        # modify production for minorloss
        if self.minorloss_percentage < 1:
            self.constant *= self.minorloss_percentage
        else:
            self.constant -= self.minorloss


        self.composition = configuration.get('solution', {'Na':1, 'Cl':1, 'Mg': 10, 'Ca': 10}) 
        # self.composition = {'Mtg': 0.5, 'Oxg': 0.1, 'CO2': 0.3, 'Toc':50}

        self.solution = self.pp.add_solution_simple(self.composition)
        self.emitter = True

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