from .model import Model
from .submodels.balance import Balance
from math import log
import numpy as np
import logging

class Cascade(Model, Balance):
    parametric_model = ['base', 'model', 'cascade', 'aeration']
    def __init__(self, config, pp: dict = {}) -> None:
        super().__init__(config, pp)

        self.steps = self.parameters['number_of_steps']
        self.step_height = self.parameters['step_height']

    
    @property
    def gas_properties(self):
        """Efficiency and saturation values per gas as function of fall height. Assumes T=10 degrees Celcius."""
        return   {
                  'Oxg':{'k_eff': (28.85*log(self.step_height)+50.066), 'c_sat': 11.3, 'MW': 32}, #O2
                  'CO2':{'k_eff': (0.6832*log(self.step_height)+15.017), 'c_sat': 0.79, 'MW':44}, #CO2
                  'Mtg':{'k_eff': (-19.196*self.step_height**2+75.161*self.step_height-0.3), 'c_sat': 0.023,'MW': 16} #CH4, interpolated at 10 degrees Celcius from solubility data in (Table 4, Duan and Mao, 2006)
                 }
    
    def aerate(self, solution, steps):
        """Returns gas concentration changes in mmol"""
        changes = {}
        for gas in ['Oxg','CO2','Mtg']:     
            c_in = solution.total(gas, 'mmol') * self.gas_properties[gas]['MW'] # convert mmol to mg manually because of Mtg and Oxg
            k_X = self.gas_properties[gas]['k_eff']/100
            c_s = self.gas_properties[gas]['c_sat']

            delta_conc = (c_s-c_in)*(1-(1-k_X) ** steps)
            changes[gas] = delta_conc / self.gas_properties[gas]['MW'] #convert back to mg after mutations
        
        effluent = solution.change(changes, 'mmol')
        return effluent

    def oxygen_cheat(self, solution):
        """Little cheat to make sure Oxg is equal to O2. This function exists because the O2-Oxg-relationship might change in the future. Needs discussion"""
        o2_in = solution.total("O2", "mmol")
        oxg_in = solution.total("Oxg", "mmol")        
        delta = o2_in - oxg_in        
        solution.add('Oxg', delta, 'mmol') # As soon as ANYTHING is adjusted to the solution, a lot of O2 dissapears/oxidates? Needs review.
        return solution
    
    def run_quality(self, type, total_inflow, solution):
        sol = self.oxygen_cheat(solution.copy()) #temporary?
        effluent = self.aerate(sol, self.steps)
        return effluent
    
    def design(self):
        influent = self.quality.influent.product
        effluent = self.run_quality(None, None, influent)
        
        ph = []
        co2 = []
        o2 = []
        ch4 = []

        co2_eff = []
        ch4_eff = []
        o2_eff = []

        ## calculate o2 saturation
        air_comp = {
            'Oxg(g)': 0.208,
            'Ntg(g)': 0.7916,
            'CO2(g)': 0.0004,
            'Mtg(g)': 0,
            'H2Sg(g)': 0,
            'H2O(g)': 0,
        }
        air = self.pp.add_gas(air_comp, volume=1000, pressure=1, fixed_pressure=True, fixed_volume=False)
        oxg_saturation = influent.copy().interact(air).total('Oxg', 'mmol') # solution saturated with air


        # gas-transfer at constant height & different stepsizes
        for steps in range(1,9): # 8 is the maximum number of steps
            inf = influent.copy()
            design_effluents = self.aerate(inf, steps)
            ph.append({'x': steps, 'y': design_effluents.pH})
            co2.append({'x': steps, 'y': design_effluents.total("CO2", "mg")})
            o2.append({'x': steps, 'y': design_effluents.total("Oxg", "mmol") * 32})            
            ch4.append({'x': steps, 'y': design_effluents.total("Mtg", "mmol") * 16})
            ## calculate removal/transfer efficiency
            ## removal percentage = (1 - (effluent conc / influent conc)) * 100
            co2_eff.append({'x': steps, 'y': (1 - (design_effluents.total("CO2", "mg") / influent.total("CO2", "mg"))) * 100})
            ch4_eff.append({'x': steps, 'y': max(0,(1 - (design_effluents.total("Mtg", "mmol") / (influent.total("Mtg", "mmol")+1e-6))) * 100)})

            ## oxygen saturation efficiency
            o2_eff.append({'x': steps, 'y': ((design_effluents.total("Oxg", "mmol") / oxg_saturation)) * 100})
        
        return {
            'influent': {
                'pH': influent.pH,
                'CH4': influent.total('Mtg') * 16,
                'N2': influent.total('Ntg') * 28.0134,
                'CO2': influent.total('CO2', 'mg'),
                'O2': influent.total('Oxg') * 32,
            },
            'effluent': {
                'pH': effluent.pH,
                'CH4': effluent.total('Mtg') * 16,
                'CO2': effluent.total('CO2','mg'),
                'O2': effluent.total('Oxg') * 32,
            },
            'charts': {
                'pH': ph,
                'CH4': ch4,
                'CO2': co2,
                'O2': o2,
                'CO2_eff': co2_eff,
                'CH4_eff': ch4_eff,
                'O2_eff': o2_eff,
            }

        }    