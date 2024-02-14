from pprint import pprint as pprint
from .model import Model
from .submodels.loss import Loss

class Sandfiltration(Model, Loss):
    def __init__(self, config, pp):
        super().__init__(config, pp)
        self.loss = config['configuration'].get('loss', 0.5)
        # self.loss = 0.5
        self.load = 0
        self.waste_solution = None

    def oxidize(self, solution, from_element, to_element, oxygen_consumption):
        solution = solution.copy()
        to_exchange = solution.total(from_element) * 0.999999 # prevent negative concentrations
        oxygen_available = solution.total("O2") # free oxygen

        to_exchange = min(to_exchange, oxygen_available / oxygen_consumption)

        solution.change({from_element: -to_exchange, to_element: to_exchange})

        return solution

    def filtrate(self, solution):
        # influent
        influent = solution.copy()

        # replace inert oxygen with free oxygen
        influent.change({"O2": influent.total("Oxg"), "Oxg": -influent.total("Oxg")*0.99999})

        # oxidize methane
        after_ch4 = self.oxidize(influent, "Mtg", "C-4", 2)
        # oxidize iron
        after_fe = self.oxidize(after_ch4, "[Fe+2]", "Fe+2", 0.25).desaturate("Fe(OH)3(a)", 0)
        # oxidize h2
        after_h2s = self.oxidize(after_fe, "[S-2]", "S-2", 2)
        after_nh4 = self.oxidize(after_h2s, "[N-3]", "N-3", 2)
        after_no2 = self.oxidize(after_nh4, "[N+3]", "N+3", 2)
        after_mn = self.oxidize(after_no2, "[Mn+2]", "Mn+2", 0.5).desaturate("Manganite", to_si=0)

        effluent = after_mn.copy()

        return effluent, [influent, after_ch4, after_fe, after_h2s, after_nh4, after_no2, after_mn]


    def run_model(self, type, total_inflow, solution):

        if(type == 'flush'):
            # add load to waste solution
            self.waste_solution = solution.copy()
            return

        effluent, _ = self.filtrate(solution)

        return effluent


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


        effluent, steps = self.filtrate(self.influent)

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







        return {}
    
    @property
    def emitter_solutions(self):
        return {'waste': self.waste_solution}


    @property
    def cost(self):
        return 250_000 # €

    @property
    def emission(self):
        return 500_000 # CO2eq

    @property    
    def energy(self):
        return 350_000 # kWh        