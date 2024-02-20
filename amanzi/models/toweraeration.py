from .model import Model
from .submodels.balance import Balance
import math
import numpy as np

from .tower.onda import run_onda
from .tower.engelstichlmair import run_engelstichlmair
from .tower import run_mackoviak
from .tower.water_properties import Water
from .tower.air_properties import Air



class Toweraeration(Model, Balance):

    def __init__(self, config, pp: dict = {}) -> None:
        super().__init__(config, pp)

        self.configuration = config.get('configuration', {})

        self.rq = float(self.configuration.get('RQ', 50))
        self.diameter = self.configuration.get('diameter', 2)
        self.packing_type = self.configuration.get('packing_type', 'raflux50')
        self.packing_height = self.configuration.get('packing_height', 2.5)
        self.capacity = self.configuration.get('nominal_capacity', 100)

        print('RQ is', self.rq)

    def run_mackoviak2(self):
        T=self.influent.temperature
        p= 1.032e5
        liquid = Water(T)
        gas = Air(T,p)
        rho_l = liquid.density()        # kg/m³
        rho_g = gas.density()           # kg/m³
        sigma_l = liquid.tension()      # N/m
        nue_g = liquid.kin_viscosity()  # m²/s 
        g=9.81
        a_geo= 110                      # m²/m³
        d=float(self.diameter)          # m
        eta = 0.94                      #void fraction
        Area= math.pi*d**2/4            # m² d in m
        form_factor = 0.28              # packing dependent
        V_l = int(self.capacity)        # m³/h
        u_l = V_l/Area/3600             # m³/m²/s
        m_yx = 1.18646 # dimensionless Henry-volatility coeficcient CO2: 1.18646 :
        u_v = u_l*self.rq #gas loading
        D_l = 1.4618272585616647e-09    # not temp-dependent yet compound specific connection to C02 or CH4 necessary
        D_g= 0.14517791941097494e-4     # not temp-dependent yet compound specific connection to C02 or CH4 necessary

        d_h = 4*eta/a_geo               #m hydraulic equivilant diameter

        beta_l_a_e =15.1*(D_l*(rho_l-rho_g)*g/sigma_l)**0.5*(a_geo/g)**(1/6)*u_l**(5/6)/((1-form_factor)**(1/3)*d_h**0.25)

        h_l = 0.57*(a_geo*u_l**2/g)**(1/3)      # m³/m³ liquid holdup
        u_r = u_v/(eta-h_l)+u_l/h_l             # m/s relative vapour velocity
        d_t = (sigma_l/((rho_l-rho_g)*g))**0.5  # m droplet diameter
        Re_t = u_r * d_t/nue_g                  # dimensionless

        # Empirical parameters from Mackoviak
        C_v= 0.0285
        n=1
        m=6
        Sc_g= nue_g/D_g  # calculate Schmidt number
        Sh_g = 2+C_v*Re_t**n*Sc_g**(1/3)
        beta_g = Sh_g*D_g/d_t               #m/s
        beta_g_real = beta_g*(1-h_l/eta)**6 #m/s
        a_e=6*h_l/d_t                       #m²/m³

        HTU_og = u_v/beta_g_real/a_e+m_yx*u_l/self.rq/beta_l_a_e
        H= float(self.packing_height) # m user input
        l_g_ratio = (V_l*rho_l/0.018)/(V_l*self.rq*rho_g/0.029) # molar ratio of liquid to gas stream
        c_l_in = self.influent.total('CO2', units='mol')        # user input for choice of Compound
        c_g_in = 0.000001   # user input or fixed values
        A=l_g_ratio/m_yx    # stripping factor
        z= np.exp((H*(A-1))/HTU_og/A)
        c_g_out = c_g_in-((A*(z-1))/(A*z-1))*(c_g_in-(c_l_in*m_yx))
        c_l_out = c_l_in-(1/l_g_ratio)*(c_g_out-c_g_in)

        efficiency = ((c_l_in-c_l_out)/c_l_in)*100
        return efficiency  
      
    def calculate_efficiency(self, method='Engel', flow=150, packing_height=5, packing='RAFLUX50', RQ=50, component='CO2', c_in=10, c_gas=0 ):
        ## run onda model
        #k= self.influent.temperature
        #efficiency = run_onda(flow, packing_height, packing, RQ, component, c_in, c_gas)
        efficiency_mackoviak= self.run_mackoviak2()

        #efficiency_engel = run_engelstichlmair(flow, packing_height, packing, RQ, component, c_in, c_gas)
        return efficiency_mackoviak




    def run_model(self, type, total_inflow, solution):
        ## gets called by solver
        #co2_removal = self.calculate_efficiency(component='CO2', c_in=solution.total('CO2', 'mmol'), c_gas=0, flow=self.capacity, packing_height=self.packing_height, packing=self.packing_type, RQ=self.rq)
        #ch4_removal = self.calculate_efficiency(component='CH4', c_in=solution.total('Mtg', 'mmol'), c_gas=0, flow=self.capacity, packing_height=self.packing_height, packing=self.packing_type, RQ=self.rq)
        co2_removal=0.5
        ch4_removal=0.5
        solution.remove_fraction('CO2', co2_removal)
        solution.remove_fraction('Mtg', ch4_removal)

        return solution



    def design(self):
        ## gets called by design GUI
        
        test= self.calculate_efficiency()
        print(f"Efficiency is {test} %")
        ## Charts
        ph = []
        co2 = []

        ## flooding and operating charts
        xx = np.linspace(0, 0.1, 50)
        flooding = [{'x': x, 'y': 0.1-10*x**2} for x in xx]
        operating = [{'x': x, 'y': 0.08-11*x**2} for x in xx]

        ## Efficiency loading and height charts
        xx = np.linspace(10,100, 50)

        heights = [1, 2, 3, 4, 5]

        loading_charts = []
        height_charts = []

        for h in heights:
            pass



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

