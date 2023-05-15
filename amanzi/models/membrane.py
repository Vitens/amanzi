from .model import Model
from .submodels.splitter import Splitter

class Membrane(Model, Splitter):
    def __init__(self, config, pp):
        super().__init__(config, pp)
        self.split = config['configuration'].get('recovery', 0.8)
        self.retention = config['configuration'].get('retention', {'Na': 0.9, 'Cl': 0.9, 'Mg': 0.5, 'Ca': 0.5})
        self.concentrate = None


    @property
    def emitter_solutions(self):
        return {'waste': self.concentrate}

    # def run_model(self, type, total_inflow, solution):
    #     return solution

    def run_model(self, type, total_inflow, solution):
        permeate = solution.copy()
        ion_removal = {}

        ion_removal = {}
        for ion, ret in self.retention.items():
            ion_removal[ion] = solution.total(ion, 'mmol') * ret  * -0.99999
        
        permeate.change(ion_removal, 'mmol')

        # Calculate Concentrate:
        ion_removal.update((x, y*-1) for x, y in ion_removal.items())
        concentrate_composition = ion_removal
        # concentrate_composition.update({'-units': 'mmol/l', 'temp': 10})

        # #Rewrite HCO3 and SO4 in terms that PhreeqPython understands
        # concentrate_composition['Alkalinity'] = str(concentrate_composition['HCO3']) + " as HCO3"
        # concentrate_composition['S(6)'] = str(concentrate_composition['SO4']) + " as SO4"

        # #Delete dormant keys
        # del concentrate_composition['HCO3']
        # del concentrate_composition['SO4']
        
        #Create new concentrate solution
        self.concentrate = self.pp.add_solution_simple(concentrate_composition)

        return permeate
