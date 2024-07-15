from .model import Model
from .submodels.balance import Balance
import math
import numpy as np
from .tower.compounds import Chemical
#from .CADET.modelsetup import CADETMODEL



class Activatedcarbon(Model, Balance):

    def __init__(self, config, pp: dict = {}) -> None:
        super().__init__(config, pp)

        self.configuration = config.get('configuration', {})
        self.packing_height = float(self.configuration.get('packing_height', 2.5))
        self.dimension = float(self.configuration.get('diameter', 2))
        self.packing_type = self.configuration.get('packing_type', 'NORA Supra 0.8')
        self.volumeflow = float(self.configuration.get('volumeflow', 100))
        self.packing_volume = self.packing_height * math.pi * (self.dimension/2)**2
        self.capacity = float(self.configuration.get('capacity', 100))
        self.freundlich_k = float(self.configuration.get('K_freundlich', 0.5))
        self.freundlich_n = float(self.configuration.get('N_freundlich', 1))
 

    def calculate_efficiency(self, compound, solution): 
        #Freundlich Isotherm parameters
        #Diffusion koefficient for film diffusion from water to GAC from compound file'
        
        t_in_seconds = 134776000
        resolution = 100
        volume_flow_rate = self.volumeflow/3600 #m³/s
        height = self.packing_height            #m
        crosssection = math.pi * (self.dimension/2)**2  #m²
        filmdiffusion =  Chemical(20,20).properties()['CO2']['Diff_water']*1000#m²/s should be m/s thats why *1000
        freundlich_k = self.freundlich_k
        freundlich_n = self.freundlich_n
                
        cadet_model = CADETMODEL()
        model=cadet_model.create_and_run_model(t_in_seconds, [solution.total('CO2', 'mol')*1000],  resolution, volume_flow_rate, height, crosssection, filmdiffusion,freundlich_k, freundlich_n)

        efficiency= 1-(model.root.output.solution.unit_001.solution_outlet[3][0]/solution.total('CO2', 'mol'))

        return efficiency

    def calculate_concentration(self, compound, solution, time): 
        #Freundlich Isotherm parameters
        #Diffusion koefficient for film diffusion from water to GAC from compound file'
        
        
        resolution = 100
        volume_flow_rate = self.volumeflow/3600 #m³/s
        height = self.packing_height            #m
        crosssection = math.pi * (self.dimension/2)**2  #m²
        filmdiffusion =  Chemical(20,20).properties()['CO2']['Diff_water']*1000#m²/s should be m/s thats why *1000
        freundlich_k = self.freundlich_k
        freundlich_n = self.freundlich_n
                
        cadet_model = CADETMODEL()
        model=cadet_model.create_and_run_model(time, [solution.total('CO2', 'mol')*1000],  resolution, volume_flow_rate, height, crosssection, filmdiffusion,freundlich_k, freundlich_n)

        efficiency= 1-(model.root.output.solution.unit_001.solution_outlet[3][0]/solution.total('CO2', 'mol'))

        return efficiency



    def run_model(self, type, total_inflow,solution):
        effciency_co2 = self.calculate_efficiency('CO2',solution)
        solution.remove_fraction('CO2', effciency_co2)
        return solution
    
    def design(self):
        EBCT_chart = np.linspace(1, 30, 30)
        effciency_chart = [{'x': i , 'y': 1-(np.exp((30-i)/30)/np.exp(1))}for i in EBCT_chart]
        c_feed = [self.influent.total('CO2', 'mol')*1000] #mol/m³
        print(dir(self.influent))
        print("Mass is ",self.influent.mass)
        t_in_seconds = 134776000
        resolution = 100
        volume_flow_rate = self.volumeflow/3600 #m³/s
        height = self.packing_height            #m
        crosssection = math.pi * (self.dimension/2)**2  #m²
        filmdiffusion =  Chemical(20,20).properties()['CO2']['Diff_water']*1000 #m²/s should be m/s thats why *1000
        freundlich_k = self.freundlich_k
        freundlich_n = self.freundlich_n
                
        cadet_model = CADETMODEL()
        model=cadet_model.create_and_run_model(t_in_seconds, c_feed,  resolution, volume_flow_rate, height, crosssection, filmdiffusion,freundlich_k, freundlich_n)
        def c_quotient(i):
            return model.root.output.solution.unit_001.solution_outlet[i][0]/c_feed[0]
        model_timesteps=model.root.output.solution.solution_times
        
        timestep=0
        for i in range(len(model.root.output.solution.solution_times)):
            if c_quotient(i) > 0.5:
                t_50 = model.root.output.solution.solution_times[i]
                timestep = i
                break
      
        regeration =  model_timesteps[timestep]-((model_timesteps[timestep]-model_timesteps[timestep-1])/(c_quotient(timestep)-c_quotient(timestep-1)))*(c_quotient(timestep)-0.5)


        eff= [{'x': (model.root.output.solution.solution_times[i]/(3600*24)) , 'y': c_quotient(i) }for i in range(len(model.root.output.solution.solution_times))]

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
            'model': {
                'regeneration': regeration/(3600*24*365),
                'EBCT' : self.packing_volume/(self.volumeflow/60),
                'Efficiency':effciency_chart,
                'Volume': self.packing_volume,
                'breathrough': eff
            }
        }