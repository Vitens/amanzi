from .model import Model
from .submodels.balance import Balance
import math
import numpy as np
from scipy.optimize import fsolve

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
        self.temp_g = float(self.configuration.get('air_temp', 50))

    
      
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
        # Af=RQ*Hc 
        # z2= np.exp((packing_height*(Af-1))/(HTU_ov*Af))
        # c_h20= rho_l/M_l       # mol H20/ m³ H20
        # c_air = rho_g/M_g*RQ   # mol Air / m³ H20
        # gas_loading_in= 0       #mol CO2 / mol Air
        # liquid_loading_in=(c_in)/c_h20  #mol Co2 / mol H20

        # cg_eq_out = Hc*liquid_loading_in*(c_h20/c_air) # gas loading at equilibrium of outflow

        # gas_loading_out =(Af*cg_eq_out*z2-Af*cg_eq_out+Af*gas_loading_in-gas_loading_in)/(Af*z2-1)
        # liquid_loading_out = liquid_loading_in-(c_air/c_h20)*(gas_loading_out-gas_loading_in)
        
        # efficiency2= ((liquid_loading_in-liquid_loading_out)/liquid_loading_in)
        # print(f"c_g out for Onda is {c_g_o} ")
        # print(f"c_g out for Mackoviak is {gas_loading_out*c_air} ")
        
        return efficiency

    def calculate_efficiency(self,compound, RQ, packing_height): 
        #run onda model  method='Engel', flow=150, packing_height=5, packing='RAFLUX50', RQ=50, component='CO2', c_in=10, c_gas=0 
        T_liq= self.influent.temperature
        T_gas= self.temp_g
        flow = self.capacity
        packing = self.packing_type
        c_in = self.influent.total(self.compound, units='mmol')
        c_in=0.0002
        if self.compound != 'CO2' and self.compound != 'Mtg':
            c_in=0.0002
        
        
        c_gas=0
        diameter=self.diameter
        HTU_ov = run_onda(T_liq,T_gas,flow,diameter, packing_height, packing, RQ, compound, c_in, c_gas)
        efficiency= self.get_NTU(T_liq,T_gas,flow,diameter, packing_height, packing, RQ, compound, c_in, c_gas,HTU_ov)
        
        return efficiency





    def run_model(self, type, total_inflow, solution):
        ## gets called by solver
        co2_removal= self.calculate_efficiency('CO2',self.rq, self.packing_height)
        ch4_removal= self.calculate_efficiency('Mtg',self.rq, self.packing_height)
        #dict1 =solution.species
        #print(solution.species)
        #print(co2_removal)
        print(self.temp_g)
        solution.remove_fraction('CO2', co2_removal)
        #dict2 =solution.species 
        #print(solution.species)
        #print({key: dict1[key] - dict2.get(key, 0) for key in dict1.keys()})
        solution.remove_fraction('Mtg', ch4_removal)

        solution.add('O2', 11-solution.total('O2', 'mg'), 'mg')

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


        Liquid_capacity= np.linspace(0.01, 0.1, 50)#capacity liquid m/s
        eng_stickl = run_engelstichlmair(self.influent.temperature,self.temp_g, self.packing_type)
        Gas_capacity_flooding, _=eng_stickl.flooding_line(Liquid_capacity,1)
        Gas_capacity_loading, _=eng_stickl.flooding_line(Liquid_capacity,0.65)

        flooding = [{'x':Liquid_capacity[x] , 'y': Gas_capacity_flooding[x]} for x in range(len(Liquid_capacity))]
        operating = [{'x': Liquid_capacity[x] , 'y': Gas_capacity_loading[x]} for x in range(len(Liquid_capacity))]

        ## Efficiency loading and height charts
        Rq = np.linspace(0.1,100, 500)

        heights = [1,2,3,4, self.packing_height]

        loading_charts = []
        height_charts = {}

        for h in heights:
            intermediary =[]
            for k in Rq:
                intermediary.append({'x': k, 'y':self.calculate_efficiency(self.compound,k,h)})
            height_charts[h] = intermediary
       

        liq_load = self.capacity/(math.pi*0.25*self.diameter**2)
        dp_dry, dp_tot, h_tot ,F, flooding_factor= eng_stickl.operating_point(self.capacity, self.rq, self.diameter)
        werkpunt_quality =[{'x': self.rq, 'y': self.calculate_efficiency(self.compound,self.rq,self.packing_height)}]
        
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
                'liquid_load': liq_load,
                'flooding_factor': flooding_factor*100,
                'liquid_holdup': h_tot*100,
                'pressure_drop': dp_tot/100,
            },
            'charts': {
                'flooding': flooding,
                'operating': operating,
                'working_point': werkpunt_hydro,
                'efficiency_loading': loading_charts,
                'efficiency_height': height_charts,
                'efficiency_workpoint': werkpunt_quality
            }
        }

