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




class Toweraeration(Model, Balance):

    def __init__(self, config, pp: dict = {}) -> None:
        super().__init__(config, pp)

        self.configuration = config.get('configuration', {})

        self.rq = float(self.configuration.get('RQ', 50))
        self.diameter = float(self.configuration.get('diameter', 2))
        self.packing_type = self.configuration.get('packing_type', 'Raflux50')
        self.packing_height = float(self.configuration.get('packing_height', 2.5))
        self.capacity = float(self.configuration.get('nominal_capacity', 100))
        self.compound = self.configuration.get('model_component', 'CO2')
        self.temp_g = float(self.configuration.get('air_temp', 15))

    
      
    def get_NTU(self,T_liq,T_gas,flow,diameter, packing_height, packing, RQ, compound, c_in, c_gas,HTU_ov) :
        comp=Chemical(T_liq,T_gas)
        Hc= comp.properties()[compound]['Henry'] #dimensionless Henry
        Sf=Hc*RQ
        #Calculate efficiency
        z = np.exp((packing_height*(Sf-1))/(HTU_ov*Sf))
        c_out_eq=c_gas/Hc # ist l, c+in ist p
        c_out = (Sf*c_out_eq*z-Sf*c_out_eq+Sf*c_in-c_in)/(Sf*z-1)
        efficiency= ((c_in-c_out)/c_in)
        c_g_o=c_gas+(c_in-c_out)/RQ
        NTU_ov=(Sf/(Sf-1)) * np.log((c_in-c_gas/Hc)*(Sf-1)/((c_out-c_gas/Hc)*Sf)+(1/Sf))
       
        return efficiency

    def calculate_efficiency(self,compound, RQ, packing_height,solution=0): 
        T_liq= self.influent.temperature
        T_gas= self.temp_g
        flow = self.capacity
        packing = self.packing_type
        c_gas = 0
        if self.compound != 'CO2' and self.compound != 'Mtg' and self.compound != 'Oxg':
            c_in=0.0002
        else:
            c_in = self.influent.total(self.compound, units='mmol') 
        if compound == 'Oxg':
            solution = self.influent.copy()
            oxg_in = self.influent.total("Oxg", "mmol")
            o2_in = self.influent.total("O2", "mmol")
 
            delta = o2_in - oxg_in        
            solution.add('Oxg', delta, 'mmol')
            c_in =solution.total("Oxg", "mmol")
            c_gas =0.208*101325/(8.31446*(273.15+T_gas)) #9.4
        if c_gas > 0:
            print(c_gas)
        diameter=self.diameter
        HTU_ov = run_onda(T_liq,T_gas,flow,diameter, packing_height, packing, RQ, compound, c_in, c_gas)
        efficiency= self.get_NTU(T_liq,T_gas,flow,diameter, packing_height, packing, RQ, compound, c_in, c_gas,HTU_ov)
        
        return efficiency


    def oxygen_transfer(self, solution):
        o2_in_gas = 9.4 # mol/m³
        o2_in = self.influent.total("O2", "mmol")
        o2_efficiency = self.calculate_efficiency('Oxg', self.rq,self.packing_height)      
        c_O2_out =-(o2_efficiency*o2_in-o2_in)
        c_o2_change = abs(o2_in-c_O2_out)
        #print(o2_efficiency)
        return c_o2_change
       


    def run_model(self, type, total_inflow, solution):
        ## gets called by solver
        co2_removal= self.calculate_efficiency('CO2',self.rq, self.packing_height)
        ch4_removal= self.calculate_efficiency('Mtg',self.rq, self.packing_height)
        o2_change = self.oxygen_transfer(self.influent)
        solution.remove_fraction('CO2', co2_removal)
        solution.remove_fraction('Mtg', ch4_removal)
        solution.add('O2',o2_change , 'mmol')

        return solution



    def design(self):
        ## gets called by design GUI
        liquid = Water(self.influent.temperature)
        rho_l = liquid.density()        # kg/m³
        p=1.023e5
        gas = Air(self.temp_g,p)
        rho_g = gas.density()           # kg/m³
        d=float(self.diameter)          # m
        Area= math.pi*d**2/4            # m² d in m
        # Column operation
        u_l = self.capacity/Area/3600             # m³/m²/s liquid loading
        ## flooding and operating charts
        def Capacity_gas(u_g):
            return u_g*math.sqrt(rho_g/(rho_l-rho_g))
        def Capacity_liq(u_l):
            return u_l*math.sqrt(rho_l/(rho_l-rho_g))

        werkpunt_hydro = [{'x': Capacity_liq(u_l), 'y': Capacity_gas(u_l*self.rq)}]

        werkpunt_quality =[{'x': self.rq, 'y': self.calculate_efficiency(self.compound,self.rq,self.packing_height)}]



        Liquid_capacity= np.linspace(0.01, 0.1, 30)#capacity liquid m/s
        eng_stickl = run_engelstichlmair(self.influent.temperature,self.temp_g, self.packing_type)

        Gas_capacity_flooding, _=eng_stickl.flooding_line(Liquid_capacity,1)
        Gas_capacity_loading, _=eng_stickl.flooding_line(Liquid_capacity,0.65)

        flooding = [{'x':Liquid_capacity[x] , 'y': Gas_capacity_flooding[x]} for x in range(len(Liquid_capacity))]
        operating = [{'x': Liquid_capacity[x] , 'y': Gas_capacity_loading[x]} for x in range(len(Liquid_capacity))]

        ## Efficiency loading and height charts
        Rq = np.linspace(0.1,100,100)

        heights = [1,2,3,4, self.packing_height]
        height_charts = {}

        for h in range(len(heights)):
            intermediary =[]
            for k in Rq:
                intermediary.append({'x': k, 'y':self.calculate_efficiency(self.compound,k,heights[h])})
            if h == len(heights)-1:
                height_charts['Werkpunt: '+ str(heights[h])]=intermediary
            else:
                height_charts[heights[h]] =intermediary  
            
        column_is_flooding = False
        try:
            dp_dry,dp_tot, h_tot ,F, flooding_factor= eng_stickl.operating_point(self.capacity, self.rq, self.diameter)
            if isinstance(dp_tot, complex):
                raise ValueError("dp_tot is a complex number.")
            if isinstance(h_tot, complex):
                raise ValueError("h_tot is a complex number.")
        except Exception as e:
            print(f"An error occurred : {e}")
            dp_dry,dp_tot, h_tot ,F, flooding_factor = 0, 0, 0, 0,0
            column_is_flooding = True
        
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
                'F': F,
                'liquid_load': u_l*3600,
                'flooding_factor': flooding_factor*100,
                'liquid_holdup': h_tot*100,
                'pressure_drop': dp_tot/100,
            },
            'charts': {
                'flooding': flooding,
                'operating': operating,
                'working_point': werkpunt_hydro,
                'efficiency_height': height_charts,
                'efficiency_workpoint': werkpunt_quality,
                'column_is_flooding': column_is_flooding
            }
        }

