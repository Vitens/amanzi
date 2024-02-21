from .model import Model
from .submodels.balance import Balance
import math
import numpy as np

from .tower.onda import run_onda
from .tower.engelstichlmair import run_engelstichlmair
from .tower import run_mackoviak
from .tower.water_properties import Water
from .tower.air_properties import Air
from .tower.packing_properties import packing
from .tower.compounds import Chemical


class Toweraeration(Model, Balance):

    def __init__(self, config, pp: dict = {}) -> None:
        super().__init__(config, pp)

        self.configuration = config.get('configuration', {})

        self.rq = float(self.configuration.get('RQ', 50))
        self.diameter = self.configuration.get('diameter', 2)
        self.packing_type = self.configuration.get('packing_type', 'Raflux50')
        self.packing_height = float(self.configuration.get('packing_height', 2.5))
        self.capacity = self.configuration.get('nominal_capacity', 100)
        self.compound = self.configuration.get('model_component', 'CO2')

        print('RQ is', self.rq)

    def run_mackoviak2(self,compound,RQ, H):
        T=self.influent.temperature
        p= 1.023e5
        liquid = Water(T)
        rho_l = liquid.density()        # kg/m³
        sigma_l = liquid.tension()      # N/m
        M_l = liquid.mol_mass()         # kg/mol

        gas = Air(T,p)
        rho_g = gas.density()           # kg/m³
        nue_g = gas.kin_viscosity()     # m²/s 
        M_g = gas.mol_mass()            # kg/mol molar weight
        g=9.81

        #Packing properties
        a_geo= packing()[self.packing_type]['ageo']   # m²/m³
        eta = packing()[self.packing_type]['void']    #void fraction
        form_factor = packing()[self.packing_type]['form']              # packing dependent
        # Column Properties
        d=float(self.diameter)          # m
        Area= math.pi*d**2/4            # m² d in m
        #H=  #float(self.packing_height)   # m 
        # Column operation
        V_l = int(self.capacity)        # m³/h
        u_l = V_l/Area/3600             # m³/m²/s liquid loading
        u_v = u_l*RQ               # m³/m²/s gas loading
        # solved compounds
        comp=Chemical(T,p)
        D_l = comp.properties()[compound]['Diff_water']    # compound specific connection to C02 or CH4 necessary
        D_g= comp.properties()[compound]['Diff_air']      #  compound specific connection to C02 or CH4 necessary
        m_yx = comp.properties()[compound]['Henry']      # dimensionless Henry-volatility coeficcient Hcc_v
        # Empirical parameters from Mackoviak
        C_v= 0.0285
        n=1
        m=6

        # calculating HTU based on Mackoviak 2015
        d_h = 4*eta/a_geo               #m hydraulic equivilant diameter
        beta_l_a_e =15.1*(D_l*(rho_l-rho_g)*g/sigma_l)**0.5*(a_geo/g)**(1/6)*u_l**(5/6)/((1-form_factor)**(1/3)*d_h**0.25)
        h_l = 0.57*(a_geo*u_l**2/g)**(1/3)      # m³/m³ liquid holdup
        u_r = u_v/(eta-h_l)+u_l/h_l             # m/s relative vapour velocity
        d_t = (sigma_l/((rho_l-rho_g)*g))**0.5  # m droplet diameter
        Re_t = u_r * d_t/nue_g                  # dimensionless    
        Sc_g= nue_g/D_g  # calculate Schmidt number
        Sh_g = 2+C_v*Re_t**n*Sc_g**(1/3)
        beta_g = Sh_g*D_g/d_t               #m/s
        beta_g_real = beta_g*(1-h_l/eta)**6 #m/s
        a_e=6*h_l/d_t                       #m²/m³
        l_g_ratio = (V_l*rho_l/M_l)/(V_l*RQ*rho_g/M_g) # molar ratio of liquid to gas stream

        HTU_og = u_v/beta_g_real/a_e+m_yx*u_l/l_g_ratio/beta_l_a_e
        
        # calculating liquid outflow concentration
        c_l_in = self.influent.total(self.compound, units='mmol')    # user input for choice of Compound
        c_g_in = 0.000001                                           # user input or fixed values
        A=l_g_ratio/m_yx                                            # stripping factor
        z= np.exp((H*(A-1))/HTU_og/A)
        c_g_out = c_g_in-((A*(z-1))/(A*z-1))*(c_g_in-(c_l_in*m_yx))
        c_l_out = c_l_in-(1/l_g_ratio)*(c_g_out-c_g_in)

        efficiency = ((c_l_in-c_l_out)/c_l_in)
        return efficiency  
      
    def calculate_efficiency(self,compound, RQ,H): 
        ## run onda model  method='Engel', flow=150, packing_height=5, packing='RAFLUX50', RQ=50, component='CO2', c_in=10, c_gas=0 
        #k= self.influent.temperature
        #efficiency = run_onda(flow, packing_height, packing, RQ, component, c_in, c_gas)
        efficiency_mackoviak= self.run_mackoviak2(compound,RQ,H)

        #efficiency_engel = run_engelstichlmair(flow, packing_height, packing, RQ, component, c_in, c_gas)
        return efficiency_mackoviak




    def run_model(self, type, total_inflow, solution):
        ## gets called by solver
        #co2_removal = self.calculate_efficiency(component='CO2', c_in=solution.total('CO2', 'mmol'), c_gas=0, flow=self.capacity, packing_height=self.packing_height, packing=self.packing_type, RQ=self.rq)
        #ch4_removal = self.calculate_efficiency(component='CH4', c_in=solution.total('Mtg', 'mmol'), c_gas=0, flow=self.capacity, packing_height=self.packing_height, packing=self.packing_type, RQ=self.rq)
        
        co2_removal= self.calculate_efficiency('CO2',self.rq, self.packing_height)
        ch4_removal= self.calculate_efficiency('CH4',self.rq, self.packing_height)
        solution.remove_fraction('CO2', co2_removal)
        solution.remove_fraction('Mtg', ch4_removal)

        return solution



    def design(self):
        ## gets called by design GUI
        
        test= self.calculate_efficiency(self.compound, self.rq, self.packing_height)
        print(f"Efficiency is {test*100} %")
        ## Charts
        ph = []
        co2 = []

        ## flooding and operating charts
        xx = np.linspace(0, 0.1, 50)
        flooding = [{'x': x, 'y': 0.1-10*x**2} for x in xx]
        operating = [{'x': x, 'y': 0.08-11*x**2} for x in xx]
        #print(flooding)
        ## Efficiency loading and height charts
        xx = np.linspace(10,2000, 50)

        heights = [1,2,3] #[1, 2, 3, 4, 5]

        loading_charts = []
        height_charts = []

        for h in heights:
            intermediary =[]
            for k in xx:
                intermediary.append({'x': k, 'y':self.calculate_efficiency('CO2',k,h)})
            height_charts.append(intermediary)

            
        print(height_charts)


        return {
            'influent': {
                'pH': self.influent.pH,
                'O2': 0,
                'CO2': self.influent.total('CO2', 'mg'),
                'CH4': self.influent.total('Mtg') * 16,
            },
            'effluent': {
                'pH': self.solution.pH,
                'O2': 0,
                'CO2': self.solution.total('CO2', 'mg'),
                'CH4': self.solution.total('Mtg') * 16 
            },
            'model': {
                'F': 1.4,
                'liquid_load': 88,
                'flooding_factor': 61,
                'liquid_holdup': 15,
                'pressure_drop': 1.5,
            },
            'charts': {
                'flooding': flooding,
                'operating': operating,
                'working_point': [{'x': 0.04, 'y': 0.05}],
                'efficiency_loading': loading_charts,
                'efficiency_height': height_charts
            }
        }

