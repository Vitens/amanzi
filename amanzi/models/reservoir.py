from .model import Model

class Reservoir(Model):

    def __init__(self, config, pp):
        super().__init__(config, pp)
        self.reservoir_solution = None

    def run_model(self, type, total_inflow, solution):
        self.reservoir_solution = solution.copy()
        return solution

    @property
    def equations(self):
        # all ingoing streams must match all outgoing streams
        return [[[c.eq(self.minorloss_percentage) for c in self.upstream_connections['product']]+ 
                 [c.eq(-1) for c in self.downstream_connections['product']] + 
                 [c.eq(-1) for c in self.downstream_connections.get('flush',[])] 
                 , self.minorloss]]
    
    @property
    def emitter_solutions(self):
        return {'flush': self.reservoir_solution}

