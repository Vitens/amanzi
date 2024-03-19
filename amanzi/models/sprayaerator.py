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
        self.sauter = float(self.configuration.get('sauter_diameter', 0.00002))
        self.fall_height = float(self.configuration.get('fall_height', 1))
        self.compound = self.configuration.get('model_component', 'CO2')


    def calculate_efficiency(self,compound, RQ, fall_height, d_sauter=0.00025):
        #d_sauter = 0.00025 # m sauter diameter function of presure/ nozzle/ volume flow.
        A = math.pi*(d_sauter**2)/4
        V = math.pi*(d_sauter**3)/6
        g=9.81
        # c_v= 0.95 # nozzle sprecific parameter
        # alpha = 45 # angle of the nozzle outflow
        # t = 2*c_v * math.sin(alpha)*np.sqrt(4*fall_height/g)

        t =np.sqrt(2*fall_height/g) ## exposure time, simple   
        
        comp=Chemical(self.influent.temperature,20)
        D_comp= comp.properties()[compound]['Diff_water']#diffusion coefficient
        k2=2*(A/V)*np.sqrt(D_comp*t/(math.pi)) #0.5 #gas transfer coefficient
        efficiency= 1-np.exp(-k2)
        return efficiency
    
    def run_model(self, type, total_inflow, solution):
        solution = self.influent.copy()
        h = self.fall_height
        RQ=1
        effciency_co2 = self.calculate_efficiency('CO2', RQ, self.fall_height, self.sauter)
        effciency_ch4 = self.calculate_efficiency('Mtg', RQ, self.fall_height,self.sauter)
        solution.remove_fraction('CO2', effciency_co2)
        solution.remove_fraction('Mtg', effciency_ch4)
        return solution


    def design(self):
        effluent = self.run_model(None, None, self.influent)
        height =np.linspace(0.01, 4, 50)
        d_sauter = np.linspace(0.000001, 0.001, 500)
        RQ=1
        height_charts = [{'x': h, 'y': self.calculate_efficiency(self.compound, RQ, h,self.sauter)} for h in height]
        
        sauter_charts ={}
        h = [0.5,1,1.5,2]
        for i in h:
            intermediary =[]
            for k in d_sauter:
                intermediary.append({'x': k, 'y':self.calculate_efficiency(self.compound,RQ,i,k)})
            sauter_charts[i] =intermediary 
        
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
                'Sauter': sauter_charts

            }
        }
    