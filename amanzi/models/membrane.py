from .model import Model
from .submodels.splitter import Splitter


# Temporary database hardcoded untill implemented globally
MEMBRANES_DATABASE = { 
        "ESPA2-LD": {
          "name": "ESPA2-LD",
          "surface": 40,
          "size": "8x40 (inch * inch)",
          "retention": {
            "Na": 0.9, "Cl": 0.9, "Mg": 0.95, "Ca": 0.95}
        }
      }
class Membrane(Model, Splitter):
    def __init__(self, config, pp):
        super().__init__(config, pp)
        self.configuration = config.get('configuration', {})
        self.split = self.configuration.get('recovery', 80)/100
        self.membrane = self.configuration.get('membrane', 'ESPA2-LD')
        self.retention = MEMBRANES_DATABASE[self.membrane].get('retention', {'Na': 0.9, 'Cl': 0.9, 'Mg': 0.5, 'Ca': 0.5})
        
        self.concentrate = None

    @property
    def surface_area(self):
        stacks = self.configuration.get('stacks', 1)
        modules = self.configuration.get('modules', 1)
        stages = self.configuration.get('stages', 1)
        vessels = self.configuration.get('vessels', 1)
        module_surface_area = MEMBRANES_DATABASE[self.membrane]['surface']

        return modules * vessels * stages * module_surface_area * stacks

        


    @property
    def emitter_solutions(self):
        return {'waste': self.concentrate}

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

    def design(self):
        print('design!', self.influent.pH)
        # print('vacuum', self.pressure)
        print(self.configuration)

        effluent = self.run_model(None, None, self.influent)

        # pressures = np.linspace(0.03, 1.0, 200)

        # ph_data = []
        # si_data = []
        # ch4_data = []
        # n2_data = []
        # co2_data = []
        # h2s_data = []
        # volumes = []
        # normal_volumes = []

        # for p in pressures:
        #     eff, gas = self.degass(self.influent, p)

        #     si_data.append({'x': p, 'y': eff.si('Calcite')})
        #     ph_data.append({'x': p, 'y': eff.pH})
        #     ch4_data.append({'x': p, 'y': eff.total('Mtg') * 16})
        #     n2_data.append({'x': p, 'y': eff.total('Ntg') * 28})
        #     co2_data.append({'x': p, 'y': eff.total('CO2','mg')})
        #     h2s_data.append({'x': p, 'y': eff.total('H2S','mg')})
        #     normal_volumes.append({'x': p, 'y': gas.volume*self.pressure})
        #     volumes.append({'x': p, 'y': gas.volume})





        return {
            'surface_area': self.surface_area,
            'influent': {
                'pH': self.influent.pH,
                'na': self.influent.total('Na'),
                'cl': self.influent.total('Cl'),
                'ca': self.influent.total('Ca','mg'),
                'mg': self.influent.total('Mg','mg'),
            },
            'effluent': {
                'pH': effluent.pH,
                'na': effluent.total('Na'),
                'cl': effluent.total('Cl'),
                'ca': effluent.total('Ca','mg'),
                'mg': effluent.total('Mg','mg'),
            },
            'concentrate': {
                'pH': self.concentrate.pH,
                'na': self.concentrate.total('Na'),
                'cl': self.concentrate.total('Cl'),
                'ca': self.concentrate.total('Ca','mg'),
                'mg': self.concentrate.total('Mg','mg'),
            },
            # 'charts': {
            # 'pH': ph_data,
            # 'SI': si_data, 
            # 'ch4': ch4_data,
            # 'n2': n2_data,
            #     'co2': co2_data,
            #     'h2s': h2s_data,
            #     'normal_volume': normal_volumes,
            #     'volume': volumes,
            # }

        }