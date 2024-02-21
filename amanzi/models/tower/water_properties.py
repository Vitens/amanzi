import math
class Water:
    def __init__(self, T):
        
        self.temperature = T
        self.temperature_in_K = float(T)+273.15
        
    def density(self):
        # Density from Density, thermal expansivity, and compressibility of liquid water from 0.deg. to 150.deg.. Correlations and tables for atmospheric pressure and saturation reviewed and expressed on 1968 temperature scale
        # George S. Kell: Journal of Chemical & Engineering Data 1975 20 (1), 97-105 
        rho = (999.83952+16.945176*self.temperature-0.001*(self.temperature**2)*7.9870401-
               46.170461*0.000001*(self.temperature**3)+105.56302*0.000000001*(self.temperature**4)-
               280.54253*0.000000000001*(self.temperature**5))/(1+16.89785*0.001*self.temperature)    # kg/m³ // g/l
        return rho
    
    def dyn_viscosity(self):
        # Viswanath, D.S.; Natarajan, G. (1989). Data Book on the Viscosity of Liquids.
        A= 0.02939 #mPa*s
        B= 507.88 #K
        C = 149.3 #K
        dynamic_viscosity= 1e-3*A*math.exp(B/(self.temperature_in_K-C)) #[Pa*s] 
        return dynamic_viscosity
        
    def kin_viscosity(self):
        kinetic_viscosity = self.dyn_viscosity()/self.density()    # m²/s
        return kinetic_viscosity
    
    def tension(self):
        # NIST : Vergaftik 1983 Internation tables of the surface tension of water
        B2= 235.8e-3 #N/m
        b3= -0.625
        mue = 1.256
        T_c = 647.15 #K
        surface_tension =(1+b3*(T_c-self.temperature_in_K)/T_c)*B2*((T_c-self.temperature_in_K)/T_c)**mue #N/m
        return surface_tension

    def mol_mass(self):
        return 0.018 # kg/mol                  