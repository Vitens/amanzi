from .model import Model

class Reservoir(Model):
    parametric_model = ['base', 'aeration', 'reservoir']

    def __init__(self, config, pp):
        super().__init__(config, pp)
        self.reservoir_solution = None

    def run_quality(self, type, total_inflow, solution):

        if type == 'flush':
            return self.reservoir_solution.copy()

        if self.parameters.get('integrated_aeration', False):
            co2_removal = self.parameters.get('co2_removal', 0)
            o2_saturation = self.parameters.get('o2_saturation', 0)

            oxygen_type = 'Oxg' if solution.total('Oxg') > 0.001 else 'O2'

            # calculate oxygen saturation and CO2 removal
            air = self.pp.add_gas({f'{oxygen_type}(g)': 0.21, 'Ntg(g)': 0.79, 'CO2(g)': 0.043/100}, fixed_pressure=True, fixed_volume=False, volume=1000, pressure=1)

            saturated = solution.copy().interact(air)

            max_o2 = saturated.total(oxygen_type)
            min_co2 = saturated.total('CO2')

            # add oxygen as oxg if solution contains oxg, otherwise add as o2
            to_add = max(0, max_o2 * o2_saturation - solution.total(oxygen_type))
            to_remove = (solution.total('CO2')-min_co2) * co2_removal

            solution.change({oxygen_type: to_add, 'CO2': -to_remove, 'Mtg': -solution.total('Mtg')})

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

