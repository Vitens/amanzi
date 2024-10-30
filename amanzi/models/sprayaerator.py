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
    parametric_model = ['base','model', 'sprayaerator', 'aeration']

    def __init__(self, config, pp: dict = {}) -> None:
        super().__init__(config, pp)

        self.configuration = config.get('configuration', {})
        # self.sauter = float(self.parameters['sauter_diameter'])
        self.fall_height = float(self.parameters['fall_height'])
        self.compound = self.configuration.get('model_component', 'CO2')
        self.g_density = Air(self.parameters['ambient_temperature'], 1.023e5).density()
        self.RQ = float(self.parameters['rq'])
    @staticmethod
    def blower_power(Qair,Tair, delta_p, efficiency, air_density):
        Pin = 101325 # Pa
        R = 8.31446 # J/(mol*K)
        kappa = 1.4
        Mair = 28.97e-3 # kg/mol
        Tair = Tair + 273.15 # C to K
        Pavg = Qair * air_density* R * Tair *(kappa/(kappa-1)) * (((Pin+delta_p)/Pin)**((kappa-1)/kappa)-1)/(efficiency*Mair)
        # conversion J to kWh
        Pavg = Pavg / 3600000
        return Pavg
    
    @property
    def context(self):
        ctx = super().context
        ctx['blower_power'] = self.blower_power
        ctx['Air_density'] = self.g_density
        return ctx
    
    def calculate_efficiency(self,compound, RQ, fall_height, d_sauter=0.00025):
        #d_sauter = 0.00025 # m sauter diameter function of presure/ nozzle/ volume flow.
        A = math.pi*(d_sauter**2)/4
        V = math.pi*(d_sauter**3)/6
        g=9.81
        # c_v= 0.95 # nozzle sprecific parameter
        # alpha = 45 # angle of the nozzle outflow
        # t = 2*c_v * math.sin(alpha)*np.sqrt(4*fall_height/g)

        t =np.sqrt(2*fall_height/g) ## exposure time, simple   
        
        comp=Chemical(self.quality.influent.product.temperature,20)
        D_comp= comp.properties()[compound]['Diff_water']#diffusion coefficient
        k2=2*(A/V)*np.sqrt(D_comp*t/(math.pi)) #gas transfer coefficient
        efficiency= 1-np.exp(-k2)
        return efficiency
    
    def run_quality(self, type, total_inflow, solution):
        solution = self.quality.influent.product.copy()
        effciency_co2 = self.calculate_efficiency('CO2', self.RQ , self.fall_height, self.sauter)
        effciency_ch4 = self.calculate_efficiency('Mtg', self.RQ , self.fall_height,self.sauter)
        solution.remove_fraction('CO2', effciency_co2)
        solution.remove_fraction('Mtg', effciency_ch4)
        return solution


    def design(self):
        effluent = self.run_quality(None, None, self.quality.influent.product)
        height =np.linspace(0.01, 4, 50)
        d_sauter = np.linspace(0.000001, 0.001, 500)

        height_charts = [{'x': h, 'y': self.calculate_efficiency(self.compound, self.RQ , h,self.sauter)} for h in height]
        
        sauter_charts ={}
        h = [0.5,1,1.5,2]
        for i in h:
            intermediary =[]
            for k in d_sauter:
                intermediary.append({'x': k, 'y':self.calculate_efficiency(self.compound,self.RQ ,i,k)})
            sauter_charts[i] =intermediary 
        
        return {
            'influent': {
                'pH': self.quality.influent.product.pH,
                'O2': self.quality.influent.product.total('O2', 'mg'),
                'CO2': self.quality.influent.product.total('CO2', 'mg'),
                'CH4': self.quality.influent.product.total('Mtg') * 16,
            },
            'effluent': {
                'pH': self.quality.effluent.product.pH,
                'O2': self.quality.effluent.product.total('O2', 'mg'),
                'CO2': self.quality.effluent.product.total('CO2', 'mg'),
                'CH4': self.quality.effluent.product.total('Mtg') * 16 
            },
            'efficiency': {
                'Height': height_charts,
                'Sauter': sauter_charts

            }
        }
    