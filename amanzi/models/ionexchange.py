from .model import Model
from .submodels.balance import Balance

class Ionexchange(Model, Balance):
    parametric_model = ['model', 'ionexchange']
    def __init__(self, config, pp):
        super().__init__(config, pp)
        self.configuration = config.get('configuration', {})
        config = config.get('configuration', {})
        config = config.get('parameters', {})

        ## Future database parameters
        # self.resin = self.configuration.get('resin', 'Purolite-A860S')
        # self.iex_coefficients = self.configuration.get('iex_coefficients', [('Toc','Cl', 1, 0.95)]) #[water_ion, resin_ion, molratio, efficieny]
        # self.resin_capacity = self.configuration.get('resin_capacity', 5000) #5000kg Cl- capacity
        # ## Future database parameters

        
        # self.resin_load = self.configuration.get('resin_load', 0)
        self.regenerations = 0
    
    def simpleExtraneousRemoval(self, solution):  
        for i in self.scenario['metaData']['customMicroComponents']['PFAS']:
            name= i['name']
            removal_efficiency = i['removalIEX']
            if name in solution.extraneous['PFAS']:
                solution.extraneous['PFAS'][name]=solution.extraneous['PFAS'][name]*(1-float(removal_efficiency))
        for i in self.scenario['metaData']['customMicroComponents']['Other']  :
            name= i['name']
            removal_efficiency = i['removalIEX']
            if name in solution.extraneous['Other']:
                solution.extraneous['Other'][name]=solution.extraneous['Other'][name]*(1-float(removal_efficiency))    
        return solution
    
    def run_quality(self, type, total_inflow, solution):
        effluent = self.simpleExtraneousRemoval(solution.copy())




        # solution_change = {}
        # for (water_ion, resin_ion, molratio, eff) in self.iex_coefficients:
        #     # Ion change in water
        #     ion_removed = solution.total(water_ion) * molratio * eff #in abs(mmol)
        #     solution_change[water_ion] = -ion_removed
        #     solution_change[resin_ion] = ion_removed

        #     # Ion change in resin (for regeneration tracking)
        #     mw = 180.16 #MW of Toc (assuming glucose)
        #     self.resin_load += ion_removed * total_inflow * mw * 1e-6 #in kg
        
        # self.regenerations = self.resin_load // self.resin_capacity 
    
        # effluent = solution.copy()
        # effluent.change(solution_change)
            
        return effluent
    
    def design(self):

        ## Filter for all Mircoorganics that have an assigned removal efficiency
        relevantInfluent = self.quality.influent.product.extraneous['PFAS'].copy()
        relevantInfluent.update(self.quality.influent.product.extraneous['Other'])
        relevantEffluent = self.quality.effluent.product.extraneous['PFAS'].copy()
        relevantEffluent.update(self.quality.effluent.product.extraneous['Other'])

        IEXcompounds = {}
        for i in self.scenario['metaData']['customMicroComponents']['PFAS']:
            name = i['name']
            removal_efficiency = i['removalIEX']
            if name in relevantInfluent and removal_efficiency != 0:
                IEXcompounds[name] = removal_efficiency
        for i in self.scenario['metaData']['customMicroComponents']['Other']:
            name = i['name']
            removal_efficiency = i['removalIEX']
            if name in relevantInfluent and removal_efficiency != 0:
                IEXcompounds[name] = removal_efficiency
        relevantInfluent = {k: v for k, v in relevantInfluent.items() if k in IEXcompounds}
        relevantEffluent = {k: v for k, v in relevantEffluent.items() if k in IEXcompounds}
        print(relevantInfluent)
        print(relevantEffluent)
        return {
            'influent' : relevantInfluent,
            'effluent' : relevantEffluent

        }
