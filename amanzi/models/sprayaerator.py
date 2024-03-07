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

    def __init__(self, config, pp):
        super().__init__(config, pp)

        self.configuration = config.get('configuration', {})
        self.rq = float(self.configuration.get('RQ', 50))
        self.fall_height = float(self.configuration.get('fall_height', 2))


    def calculate_efficiency(self,compound, RQ):
        g=9.81
        k2= 0.5 #random value: gas transfer koefficient
        k= 1-np.exp(-k2*np.sqrt(2*self.fall_height/g))
    
    def run_model(self, type, total_inflow, solution):
        

        return super().run_model(type, total_inflow, solution)