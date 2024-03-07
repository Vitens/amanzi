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
    def oxygen(self):
        Para_water=[0.02581,-1.384e3]
        D_water=self.D_in_water(Para_water)*1e-4 # m²/s
        
        Para_air=[-0.0875, 7.5478E-04, 9.9523E-07]
        D_air=self.D_in_air(Para_air)*1e-4 # m²/s
        
        # Values from Henrys-law.org
        Hcp_s= 1.3e-5 #mol/(m³*Pa) 
        H_dt = 1500
        Henry_dimensionless = self.henry_conversion(Hcp_s,H_dt)
        return D_water, D_air , Henry_dimensionless

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
        Hcp_s= 2.3e-3 #mol/(m³*Pa)  low confidence in the parameter 
        H_dt = 3400                    # no value for temperature dependence available
        Henry_dimensionless = self.henry_conversion(Hcp_s,H_dt)
        return D_water, D_air , Henry_dimensionless
    
    def vinylchloride(self): #does not have values for henry coefficient
        Para_water = [-1.56323,-986.78]
        D_water=self.D_in_water(Para_water)*1e-4 # m²/s

        Para_air=[-9.16E-02, 5.41E-04, 5.6117E-07]		
        D_air=self.D_in_air(Para_air)*1e-4 # m²/s
        
        # Values from Henrys-law.org
        Hcp_s= 4.1e-4 #mol/(m³*Pa) 
        H_dt = 2500
        Henry_dimensionless = self.henry_conversion(Hcp_s,H_dt)
        return D_water, D_air , Henry_dimensionless
    
    def trichloroethane(self):
        Para_water = [-1.4055,-1047.3]
        D_water=self.D_in_water(Para_water)*1e-4 # m²/s

        Para_air=[-0.07064, 3.77E-04, 4.26E-07]		
        D_air=self.D_in_air(Para_air)*1e-4 # m²/s
        
        # Values from Henrys-law.org
        Hcp_s= 6e-4 #mol/(m³*Pa)  
        H_dt = 3800                   
        Henry_dimensionless = self.henry_conversion(Hcp_s,H_dt)
        return D_water, D_air , Henry_dimensionless

    def dichloroethane1_1(self):
        Para_water = [-1.4471,-1052.8]
        D_water=self.D_in_water(Para_water)*1e-4 # m²/s

        Para_air=[-0.07714, 4.28E-04, 4.69E-07]		
        D_air=self.D_in_air(Para_air)*1e-4 # m²/s
        
        # Values from Henrys-law.org
        Hcp_s= 1.7e-3 #mol/(m³*Pa)   
        H_dt = 3900                   
        Henry_dimensionless = self.henry_conversion(Hcp_s,H_dt)
        return D_water, D_air , Henry_dimensionless

    def dichloroethane1_2(self):
        Para_water = [-1.4471,-1052.8]
        D_water=self.D_in_water(Para_water)*1e-4 # m²/s

        Para_air=[-0.07945, 4.31E-04, 4.73E-07]		
        D_air=self.D_in_air(Para_air)*1e-4 # m²/s
        
        # Values from Henrys-law.org
        Hcp_s= 7.5e-3 #mol/(m³*Pa)  
        H_dt = 4400                   
        Henry_dimensionless = self.henry_conversion(Hcp_s,H_dt)
        return D_water, D_air , Henry_dimensionless 

    def tetrachlormethane(self):
        Para_water = [-1.4762,-1056.6]
        D_water=self.D_in_water(Para_water)*1e-4 # m²/s

        Para_air=[-0.06813, 3.81E-04, 4.2294E-07]		
        D_air=self.D_in_air(Para_air)*1e-4 # m²/s
        
        # Values from Henrys-law.org
        Hcp_s= 3.4e-4 #mol/(m³*Pa)  
        H_dt = 4200                   
        Henry_dimensionless = self.henry_conversion(Hcp_s,H_dt)
        return D_water, D_air , Henry_dimensionless  

    def trichloromethane(self):
        Para_water = [-1.4389,-1051.7]
        D_water=self.D_in_water(Para_water)*1e-4 # m²/s

        Para_air=[-0.07838, 4.21E-04, 4.73E-07]		
        D_air=self.D_in_air(Para_air)*1e-4 # m²/s
        
        # Values from Henrys-law.org
        Hcp_s= 2.7e-3 #mol/(m³*Pa)  
        H_dt = 4200                    
        Henry_dimensionless = self.henry_conversion(Hcp_s,H_dt)
        return D_water, D_air , Henry_dimensionless
    
    def dichloromethane(self):
        Para_water = [-1.3916,-1045.5]
        D_water=self.D_in_water(Para_water)*1e-4 # m²/s

        Para_air=[-0.0904, 4.92E-04, 5.39E-07]		
        D_air=self.D_in_air(Para_air)*1e-4 # m²/s
        
        # Values from Henrys-law.org
        Hcp_s= 3.9e-3 #mol/(m³*Pa) 
        H_dt = 3500                    
        Henry_dimensionless = self.henry_conversion(Hcp_s,H_dt)
        return D_water, D_air , Henry_dimensionless  

    def dichloropropane1_2(self):
        Para_water = [-1.4831,-1057.6]
        D_water=self.D_in_water(Para_water)*1e-4 # m²/s

        Para_air=[-0.0671, 4.38E-04, 5.09E-07]		
        D_air=self.D_in_air(Para_air)*1e-4 # m²/s
        
        # Values from Henrys-law.org
        Hcp_s= 3.7e-3 #mol/(m³*Pa) 
        H_dt = 4100                   
        Henry_dimensionless = self.henry_conversion(Hcp_s,H_dt)
        return D_water, D_air , Henry_dimensionless  


    def properties(self):
        Dwater_O2, Dair_O2, H_O2 =self.oxygen()
        Dwater_CH4, Dair_CH4, H_CH4 =self.methane()
        Dwater_CO2, Dair_CO2, H_CO2 =self.carbon_dioxide()
        Dwater_C2Cl4,Dair_C2Cl4, H_C2Cl4 = self.perchloroethylene()
        Dwater_C2HCl3,Dair_C2HCl3, H_C2HCl3 = self.perchloroethylene()
        Dwater_C2H2Cl2,Dair_C2H2Cl2, H_C2H2Cl2 = self.cis_1_2_Dichlooretheen()
        Dwater_C2H3Cl,Dair_C2H3Cl, H_C2H3Cl = self.vinylchloride()
        Dwater_C2H3Cl3,Dair_C2H3Cl3, H_C2H3Cl3 = self.trichloroethane()
        Dwater_C2H4Cl2_1_1,Dair_C2H4Cl2_1_1, H_C2H4Cl2_1_1 = self.dichloroethane1_1()
        Dwater_C2H4Cl2_1_2,Dair_C2H4Cl2_1_2, H_C2H4Cl2_1_2 = self.dichloroethane1_2()       
        Dwater_CCl4,Dair_CCl4, H_CCl4 = self.tetrachlormethane()
        Dwater_CHCl3,Dair_CHCl3, H_CHCl3 = self.trichloromethane()
        Dwater_CH2Cl2,Dair_CH2Cl2, H_CH2Cl2 = self.dichloromethane()
        Dwater_C3H6Cl2,Dair_C3H6Cl2, H_C3H6Cl2 = self.dichloropropane1_2()

        return {
                'Oxg':{'Diff_water': Dwater_O2, 'Diff_air': Dair_O2,'Henry': H_O2 ,'MW':44}, #o2
                'CO2':{'Diff_water': Dwater_CO2, 'Diff_air': Dair_CO2,'Henry': H_CO2 ,'MW':44}, #CO2
                'Mtg':{'Diff_water': Dwater_CH4, 'Diff_air': Dair_CH4,'Henry': H_CH4 ,'MW':16 },
                'C2Cl4':{'Diff_water': Dwater_C2Cl4, 'Diff_air': Dair_C2Cl4,'Henry': H_C2Cl4 ,'MW':16 },
                'C2HCl3':{'Diff_water': Dwater_C2HCl3, 'Diff_air': Dair_C2HCl3,'Henry': H_C2HCl3 ,'MW':16 },
                'C2H2Cl2':{'Diff_water': Dwater_C2H2Cl2, 'Diff_air': Dair_C2H2Cl2,'Henry': H_C2H2Cl2 ,'MW':16 },              
                'C2H3Cl':{'Diff_water': Dwater_C2H3Cl, 'Diff_air': Dair_C2H3Cl,'Henry': H_C2H3Cl ,'MW':16 },               
                'C2H3Cl3':{'Diff_water': Dwater_C2H3Cl3, 'Diff_air': Dair_C2H3Cl3,'Henry': H_C2H3Cl3,'MW':16 },
                'C2H4Cl2_1_1':{'Diff_water': Dwater_C2H4Cl2_1_1, 'Diff_air': Dair_C2H4Cl2_1_1,'Henry': H_C2H4Cl2_1_1 ,'MW':16 },
                'C2H4Cl2_1_2':{'Diff_water': Dwater_C2H4Cl2_1_2, 'Diff_air': Dair_C2H4Cl2_1_2,'Henry': H_C2H4Cl2_1_2 ,'MW':16 },
                'CCl4':{'Diff_water': Dwater_CCl4, 'Diff_air': Dair_CCl4,'Henry': H_CCl4 ,'MW':16 },
                'CHCl3':{'Diff_water': Dwater_CHCl3, 'Diff_air': Dair_CHCl3,'Henry': H_CHCl3 ,'MW':16 },
                'CH2Cl2':{'Diff_water': Dwater_CH2Cl2, 'Diff_air': Dair_CH2Cl2,'Henry': H_CH2Cl2 ,'MW':16 },
                'C3H6Cl2':{'Diff_water': Dwater_C3H6Cl2, 'Diff_air': Dair_C3H6Cl2,'Henry': H_C3H6Cl2 ,'MW':16 }

                
                }
    
