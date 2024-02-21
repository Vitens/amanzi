import numpy as np
from .water_properties import Water
class Chemical:
    def __init__(self,T ,p):
        self.temperature = T
        self.temperature_in_K = float(T)+273.15

    def D_in_water(self,A,B):
        return 10**(A+B/(self.temperature_in_K))
    def D_in_air(self,A,B,C): #for 1 atm
        return A+B*(self.temperature_in_K)+C*(self.temperature_in_K)**2
    
    def henry_conversion(self,Hcp_s,H_dt):
            T_ref=298.15 # K
            R = 8.314 #Gas constant
            Henry_coefficient = Hcp_s*np.exp(H_dt*((1/self.temperature_in_K)-(1/T_ref)))
            return 1/(Henry_coefficient*R*self.temperature_in_K)

    def carbon_dioxide(self, pressure=1.023):
        A_water=-1.37281
        B_water=-997.66
        D_water=self.D_in_water(A_water,B_water)*1e-4 # m²/s
        
        A_air=-0.15731
        B_air=8.86E-04
        C_air=5.6831E-07
        D_air_atm=self.D_in_air(A_air,B_air,C_air)*1e-4 # m²/s
        #inclusion of pressure dependence
        D_air=D_air_atm*(1.023/pressure)  #ideal gas assumption
        
        # Values from Henrys-law.org
        Hcp_s= 3.4e-4 #mol/(m³*Pa) 
        H_dt = 2300
        Henry_dimensionless = self.henry_conversion(Hcp_s,H_dt)
        
        return D_water, D_air , Henry_dimensionless
    
    def methane(self, pressure=1.023):
        A_water=-1.64756
        B_water=-920.56
        D_water=self.D_in_water(A_water,B_water)*1e-4 # m²/s
        			
        A_air=-0.17171
        B_air=1.05E-03
        C_air=9.2532E-07
        D_air_atm=self.D_in_air(A_air,B_air,C_air)*1e-4 # m²/s
        #inclusion of pressure dependence
        D_air=D_air_atm*(1.023/pressure)  #ideal gas assumption
        
        # Values from Henrys-law.org
        Hcp_s= 1.4e-5 #mol/(m³*Pa) 
        H_dt = 1600
        Henry_dimensionless = self.henry_conversion(Hcp_s,H_dt)
        return D_water, D_air , Henry_dimensionless

    
    def properties(self):
        Dwater_CH4, Dair_CH4, H_CH4 =self.methane(pressure=1.023)
        Dwater_CO2, Dair_CO2, H_CO2 =self.carbon_dioxide(pressure=1.023)

        return {
                'CO2':{'Diff_water': Dwater_CO2, 'Diff_air': Dair_CO2,'Henry': H_CO2 ,'MW':44}, #CO2
                'CH4':{'Diff_water': Dwater_CH4, 'Diff_air': Dair_CH4,'Henry': H_CH4 ,'MW':16 }
                }
    
