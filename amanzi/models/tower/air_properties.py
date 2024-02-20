
class Air:
    def __init__(self, T, p):
        self.temperature = T
        self.temperature_in_K = float(T)+273.15
        self.pressure = p # in Pa
        
    #Ideal gas assumption
    def density(self):
        ## https://en.wikipedia.org/wiki/Density_of_air
        M = 0.0289652 # molar mass air in kg.mol-1
        R = 8.31446261815324 # gas constant J.k-1.mol-1
        return self.pressure*M/(R*self.temperature_in_K)
    
    def dyn_viscosity(self):
        #Power law for dynamic viscosity
        mue_273K = 17.15e-6 #
        mue_T = mue_273K*(self.temperature_in_K/273.15)**(2/3)
        return mue_T
    