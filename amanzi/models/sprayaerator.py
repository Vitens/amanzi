from .model import Model
from .submodels.balance import Balance
import math
import numpy as np
from .tower.onda import run_onda
from .tower.engelstichlmair import run_engelstichlmair
from .tower.mackoviak import run_mackoviak
from .tower.water_properties import Water
from .tower.air_properties import Air
from .tower.packing_properties import packing
from .tower.compounds import Chemical

class Sprayaerator(Model, Balance):

    def __init__(self, config, pp: dict = {}) -> None:
        super().__init__(config, pp)

        self.configuration = config.get('configuration', {})
        self.rq = float(self.configuration.get('RQ', 50))
        self.fall_height = float(self.configuration.get('fall_height', 2))
        self.compound = self.configuration.get('model_component', 'CO2')


    def calculate_efficiency(self,compound, RQ, fall_height):
        g=9.81
        d_sauter = 0.00025 # m sauter diameter function of presure/ nozzle/ volume flow.
        A = math.pi*(d_sauter**2)/4
        V = math.pi*(d_sauter**3)/6
        g=9.81
        c_v= 0.95 # nozzle sprecific parameter
        alpha = 45 # angle of the nozzle outflow
        t =np.sqrt(2*fall_height/g) #2*c_v * math.sin(alpha)*np.sqrt(4*fall_height/g)# exposure time   
        
        comp=Chemical(self.influent.temperature,20)
        D_comp= comp.properties()[compound]['Diff_water']#diffusion coefficient
        k2=2*(A/V)*np.sqrt(D_comp*t/(math.pi)) #0.5 #gas transfer coefficient
        efficiency= 1-np.exp(-k2)
        return efficiency
    
    def run_model(self, type, total_inflow, solution):
        solution = self.influent.copy()
        h = self.fall_height
        RQ=1
        effciency = self.calculate_efficiency('CO2', RQ, self.fall_height)#-0.299*h**4 + 1.4589**h**3 - 2.6619*h**2 + 2.2924*h - 0.0127
        solution.remove_fraction('CO2', effciency)
        return solution


    def design(self):
        effluent = self.run_model(None, None, self.influent)
        height =np.linspace(0.01, 4, 50)
        def effciency(h):
            return -0.299*h**4 + 1.4589**h**3 - 2.6619*h**2 + 2.2924*h - 0.0127
        RQ=1
        height_charts = [{'x': h, 'y': self.calculate_efficiency(self.compound, RQ, h)} for h in height]
        print(height_charts)
        return {
            'influent': {
                'pH': self.influent.pH,
                'O2': self.influent.total('O2', 'mg'),
                'CO2': self.influent.total('CO2', 'mg'),
                'CH4': self.influent.total('Mtg') * 16,
            },
            'effluent': {
                'pH': self.solution.pH,
                'O2': self.solution.total('O2', 'mg'),
                'CO2': self.solution.total('CO2', 'mg'),
                'CH4': self.solution.total('Mtg') * 16 
            },
            'efficiency': {
                'Height': height_charts,
                'Height2': height_charts

            }
        }
    