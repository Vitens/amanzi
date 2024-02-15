def air(temperature, pressure):
    temperature_in_K = temperature+273.15
    #Ideal gas assumption
    def density_air(temperature=20):
        ## https://en.wikipedia.org/wiki/Density_of_air
        p = 101325 # air pressure Pa
        T = 273.15 + temperature # temperature in K
        M = 0.0289652 # molar mass air in kg.mol-1
        R = 8.31446261815324 # gas constant J.k-1.mol-1
        return p*M/(R*T)
    density = density_air(temperature)
    #Power law for dynamic viscosity
    mue_273K = 17.15e-6
    mue_T = mue_273K*(temperature_in_K/273.15)**(2/3)
    
    return density, mue_T