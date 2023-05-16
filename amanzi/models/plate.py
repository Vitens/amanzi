from .model import Model
from .submodels.balance import Balance
from math import log

class Plate(Model, Balance):
    def __init__(self, config, pp: dict = {}) -> None:
        super().__init__(config, pp)
        self.configuration = config.get('configuration', {})

        # self.RQ = self.configuration.get('RQ', 0.4)
        self.steps = self.configuration.get('steps', 10)
        self.height = self.configuration.get('height', 0.6)     

        self.gasses = ['Oxg', 'CO2', 'Mtg']
        # self.air_composition = {'Ntg(g)':0.79, 'O2(g)': 0.208,'CO2(g)':0.002}
        
        self.change_per_step = {}

    def run_model(self, type, total_inflow, solution):
        # air_volume = total_inflow * self.RQ
        # gas_phase = self.pp.add_gas(self.air_composition, volume = air_volume)
        gas_change = {}

        for gas in self.gasses:
            mw = self.gas_properties[gas]['MW']                 
            c_in = solution.total(gas, 'mmol') * mw
            self.change_per_step[gas] = self.gas_areation(gas, c_in) # Save gas concentration in liquid-phase at each step for plotting in UI-Design-fuction
            gas_change[gas] = -1/mw*(c_in - self.change_per_step[gas][-1])
        
        effluent = solution.copy()
        print("gas_change")
        print(gas_change)
        effluent.change(gas_change, 'mmol')        
        return effluent

    def gas_areation(self, gas, c_in):
        """Returns gas concentration in liquid-phase at each step"""
        steps = range(1, self.steps+1)
        k_X = self.gas_properties[gas]['k_eff']/100
        c_s = self.gas_properties[gas]['c_sat']
        
        
        # Calculate new concentration
        concentrations = []        
        for step in steps:
            product = (c_s-c_in)*(1-(1-k_X) ** step)
            effluent_per_step = c_in + product
            concentrations.append(effluent_per_step)

        return concentrations

    @property
    def gas_properties(self):
        """Efficiency and saturation values per gas as function of fall height. Assumes T=10 degrees Celcius."""
        return {
            'Oxg':{
                'k_eff': (28.85*log(self.height)+50.066),
                'c_sat': 11.3,
                'MW': 32
                },
            'CO2':{
                'k_eff': (0.6832*log(self.height)+15.017),
                'c_sat': 0.79,
                'MW':44
                },
            'Mtg':{
                'k_eff': (-19.196*self.height**2+75.161*self.height-0.3),
                'c_sat': 0.023,
                'MW': 16
                } #CH4, interpolated at 10 degrees Celcius from solubility data in (Table 4, Duan and Mao, 2006)
            }


