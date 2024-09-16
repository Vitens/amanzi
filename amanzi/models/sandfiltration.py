from pprint import pprint as pprint
from .model import Model
from .submodels.loss import Loss

class Sandfiltration(Model, Loss):
    parametric_model = ['base', 'model', 'filtration']

    def __init__(self, config, pp):
        super().__init__(config, pp)
        #self.loss = config['configuration'].get('loss', 0.5)
        config = config.get('configuration', {})
        config = config.get('parameters', {})

        self.loss = self.get_output('backwash_loss')
        self.load = 0
        self.waste_solution = None

    def oxidize(self, solution, from_element, to_element, oxygen_consumption, efficiency=1):
        solution = solution.copy()
        to_exchange = solution.total(from_element) * 0.999999 # prevent negative concentrations
        oxygen_available = solution.total("O2") # free oxygen

        to_exchange = min(to_exchange, oxygen_available / oxygen_consumption)
        to_exchange = to_exchange * efficiency

        solution.change({from_element: -to_exchange, to_element: to_exchange})

        return solution
    
    @property
    def backwash_programme(self):
        config = self.config.get('configuration', {})
        programme = config.get('backwash_programme', [])
        return programme
    
    @property
    def _backwash_duration(self):
        return sum([p['time'] for p in self.backwash_programme]) / 60

    @property
    def _backwash_volume(self):
        surface = self.output_parameters['surface_area'].calculate(super().context)
        return sum([p['water'] * surface * p['time']/3600 for p in self.backwash_programme])

    @property
    def _backwash_max_rate(self):
        return max([p['water'] for p in self.backwash_programme] + [0])
        
    @staticmethod
    def kozeny_carman(p, v, d):
        d /= 1e3 # convert to mm
        v /= 3600 # convert to m/s
        return 180 * 1.3e-6 / 9.81 * (1-p)**2 / p**3 * v/d**2


    @property
    def context(self):
        ctx = super().context
        ctx['_backwash_duration'] = self._backwash_duration
        ctx['_backwash_volume'] = self._backwash_volume
        ctx['_backwash_max_rate'] = self._backwash_max_rate
        ctx['kozeny_carman'] = self.kozeny_carman
        return ctx

    def filtrate(self, solution):
        # suppress removal of elements if set to True
        fe_removal_efficiency = 1
        if self.parameters['suppress_iron_removal']:
            fe_removal_efficiency = self.parameters['iron_removal_efficiency']
        nh4_removal_efficiency = 1
        if self.parameters['suppress_ammonium_removal']:
            nh4_removal_efficiency = self.parameters['ammonium_removal_efficiency']
        mn_removal_efficiency = 1
        if self.parameters['suppress_manganese_removal']:
            mn_removal_efficiency = self.parameters['manganese_removal_efficiency']

        # influent
        influent = solution.copy()

        # replace inert oxygen with free oxygen
        influent.change({"O2": influent.total("Oxg"), "Oxg": -influent.total("Oxg")*0.99999})

        # oxidize methane
        after_ch4 = self.oxidize(influent, "Mtg", "C-4", 2)
            
        after_fe = self.oxidize(after_ch4, "[Fe+2]", "Fe+2", 0.25, fe_removal_efficiency).desaturate("Fe(OH)3(a)", 0)
        
        # oxidize h2
        after_h2s = self.oxidize(after_fe, "[S-2]", "S-2", 2)



        after_nh4 = self.oxidize(after_h2s, "[N-3]", "N-3", 2, nh4_removal_efficiency)
        after_no2 = self.oxidize(after_nh4, "[N+3]", "N+3", 2)
        after_mn = self.oxidize(after_no2, "[Mn+2]", "Mn+2", 0.5, mn_removal_efficiency).desaturate("Manganite", to_si=0)

        effluent = after_mn.copy()

        return effluent, [influent, after_ch4, after_fe, after_h2s, after_nh4, after_no2, after_mn]


    def run_quality(self, type, total_inflow, solution):

        if(type == 'flush'):
            # add load to waste solution
            self.waste_solution = solution.copy()
            return
        
        if(type == 'product'):
            effluent, _ = self.filtrate(solution)
            return effluent

        return solution


    def design(self):
        labels = ["Influent", "Methaan oxidatie", "IJzerverwijdering", "H2S oxidatie", "Nitrificatie", "Denitrificatie", "Ontmanganing"]

        values = {
            'pH': lambda s: s.pH,
            'O2': lambda s: s.total("O2", 'mg'),
            'CO2': lambda s: s.total("CO2", 'mg'),
            'CH4': lambda s: s.total("Mtg") * 16e3,
            'Fe': lambda s: s.total("Fe", 'mg'),
            'NH4': lambda s: s.total("[N-3]") * 18,
            'NO2': lambda s: s.total("[N+3]") * 46,
            'NO3': lambda s: s.total("NO3", 'mg'),
            'Mn': lambda s: s.total("Mn", 'mg'),
        }


        effluent, steps = self.filtrate(self.quality.influent.product)

        results = {}

        for i, step in enumerate(steps):

            print(step.pH)
            step_results = {}

            for n, v in values.items():
                step_results[n] = v(step)
            
            results[labels[i]] = step_results
                
        return {
            'steps': labels,
            'values': results,
            'names': list(values.keys())
        }

    @property
    def emitter_solutions(self):
        return {'waste': self.waste_solution}