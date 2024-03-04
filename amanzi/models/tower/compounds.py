import numpy as np
from .water_properties import Water
class Chemical:
    def __init__(self,T_liq,T_gas):
        self.temperature_in_K_liq = float(T_liq)+273.15
        self.temperature_in_K_gas = float(T_gas)+273.15

    def D_in_water(self,para):
        return 10**(para[0]+para[1]/(self.temperature_in_K_liq))
    def D_in_air(self,para): #for 1 atm
        return para[0]+para[1]*(self.temperature_in_K_gas)+para[2]*(self.temperature_in_K_gas)**2
    
    def henry_conversion(self,Hcp_s,H_dt):
            T_ref=298.15 # K
            R = 8.314 #Gas constant
            Henry_coefficient = Hcp_s*np.exp(H_dt*((1/self.temperature_in_K_liq)-(1/T_ref)))
            return 1/(Henry_coefficient*R*self.temperature_in_K_liq)

    def carbon_dioxide(self):
        Para_water=[-1.37281,-997.66]
        D_water=self.D_in_water(Para_water)*1e-4 # m²/s
        
        Para_air=[-0.15731, 8.86E-04, 5.6831E-07]
        D_air=self.D_in_air(Para_air)*1e-4 # m²/s
        
        # Values from Henrys-law.org
        Hcp_s= 3.4e-4 #mol/(m³*Pa) 
        H_dt = 2300
        Henry_dimensionless = self.henry_conversion(Hcp_s,H_dt)
        return D_water, D_air , Henry_dimensionless
    
    def methane(self):
        Para_water = [-1.64756,-920.56]
        D_water=self.D_in_water(Para_water)*1e-4 # m²/s

        Para_air=[-0.17171,1.05E-03,9.2532E-07]		
        D_air=self.D_in_air(Para_air)*1e-4 # m²/s
        
        # Values from Henrys-law.org
        Hcp_s= 1.4e-5 #mol/(m³*Pa) 
        H_dt = 1600
        Henry_dimensionless = self.henry_conversion(Hcp_s,H_dt)
        return D_water, D_air , Henry_dimensionless
    
    def perchloroethylene(self):
        Para_water = [-1.4943,-1059]
        D_water=self.D_in_water(Para_water)*1e-4 # m²/s

        Para_air=[-0.06298, 3.60E-04, 3.9976E-07]		
        D_air=self.D_in_air(Para_air)*1e-4 # m²/s
        
        # Values from Henrys-law.org
        Hcp_s= 5.5e-4 #mol/(m³*Pa) 
        H_dt = 4500
        Henry_dimensionless = self.henry_conversion(Hcp_s,H_dt)
        return D_water, D_air , Henry_dimensionless
    
    def trichloroethylene(self):
        Para_water = [-1.44642, -1055.1]
        D_water=self.D_in_water(Para_water)*1e-4 # m²/s

        Para_air=[-0.06933, 3.97E-04, 4.3737E-07]		
        D_air=self.D_in_air(Para_air)*1e-4 # m²/s
        
        # Values from Henrys-law.org
        Hcp_s= 1.1e-3 #mol/(m³*Pa) 
        H_dt = 4100
        Henry_dimensionless = self.henry_conversion(Hcp_s,H_dt)
        return D_water, D_air , Henry_dimensionless
    
    def cis_1_2_Dichlooretheen(self):
        Para_water = [-1.4292,-1050.4]
        D_water=self.D_in_water(Para_water)*1e-4 # m²/s

        Para_air=[-0.0782, 4.50E-04, 4.8345E-07]		
        D_air=self.D_in_air(Para_air)*1e-4 # m²/s
        
        # Values from Henrys-law.org
        Hcp_s= 1.2e-2 #mol/(m³*Pa)  low confidence in the parameter 
        H_dt = 0                    # no value for temperature dependence available
        Henry_dimensionless = self.henry_conversion(Hcp_s,H_dt)
        return D_water, D_air , Henry_dimensionless
    
    # def vinylchloride(self): does not have values for henry coefficient
    #     Para_water = [-1.56323,-986.78]
    #     D_water=self.D_in_water(Para_water)*1e-4 # m²/s

    #     Para_air=[-9.16E-02, 5.41E-04, 5.6117E-07]		
    #     D_air=self.D_in_air(Para_air)*1e-4 # m²/s
        
    #     # Values from Henrys-law.org
    #     Hcp_s= 1.1e-3 #mol/(m³*Pa) 
    #     H_dt = 4100
    #     Henry_dimensionless = self.henry_conversion(Hcp_s,H_dt)
    #     return D_water, D_air , Henry_dimensionless



    
    def properties(self):
        Dwater_CH4, Dair_CH4, H_CH4 =self.methane()
        Dwater_CO2, Dair_CO2, H_CO2 =self.carbon_dioxide()
        Dwater_C2Cl4,Dair_C2Cl4, H_C2Cl4 = self.perchloroethylene()
        Dwater_C2HCl3,Dair_C2HCl3, H_C2HCl3 = self.perchloroethylene()
        Dwater_C2H2Cl2,Dair_C2H2Cl2, H_C2H2Cl2 = self.cis_1_2_Dichlooretheen()

        return {
                'CO2':{'Diff_water': Dwater_CO2, 'Diff_air': Dair_CO2,'Henry': H_CO2 ,'MW':44}, #CO2
                'Mtg':{'Diff_water': Dwater_CH4, 'Diff_air': Dair_CH4,'Henry': H_CH4 ,'MW':16 },
                'C2Cl4':{'Diff_water': Dwater_C2Cl4, 'Diff_air': Dair_C2Cl4,'Henry': H_C2Cl4 ,'MW':16 },
                'C2HCl3':{'Diff_water': Dwater_C2HCl3, 'Diff_air': Dair_C2HCl3,'Henry': H_C2HCl3 ,'MW':16 },
                'C2H2Cl2':{'Diff_water': Dwater_C2H2Cl2, 'Diff_air': Dair_C2H2Cl2,'Henry': H_C2H2Cl2 ,'MW':16 }               
                
                }
    
