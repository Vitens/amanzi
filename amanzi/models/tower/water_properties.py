import math

def water(temperature): # Temperature in Celsius
    temperature_in_K = temperature+273.15
    # Viswanath, D.S.; Natarajan, G. (1989). Data Book on the Viscosity of Liquids.
    A= 0.02939 #mPa*s
    B= 507.88 #K
    C = 149.3 #K
    dynamic_viscosity= 1e-3*A*math.exp(B/(temperature_in_K-C)) #[Pa*s] 
    
    # Density from Density, thermal expansivity, and compressibility of liquid water from 0.deg. to 150.deg.. Correlations and tables for atmospheric pressure and saturation reviewed and expressed on 1968 temperature scale
    # George S. Kell: Journal of Chemical & Engineering Data 1975 20 (1), 97-105 
    density = (999.83952+16.945176*temperature-0.001*(temperature**2)*7.9870401-
               46.170461*0.000001*(temperature**3)+105.56302*0.000000001*(temperature**4)-
               280.54253*0.000000000001*(temperature**5))/(1+16.89785*0.001*temperature)    # kg/m³ // g/l
                             
    kinetic_viscosity = dynamic_viscosity*1e-3/density    # m²/s
    
    # NIST : Vergaftik 1983 Internation tables of the surface tension of water
    B2= 235.8e-3 #N/m
    b3= -0.625
    mue = 1.256
    T_c = 647.15 #K
    surface_tension =(1+b3*(T_c-temperature_in_K)/T_c)*B2*((T_c-temperature_in_K)/T_c)**mue #N/m
    
    molar_mass= 18 #kg/kmol  PubChemPy an option for implementing molar mass
                             
    
    return dynamic_viscosity, kinetic_viscosity, density, surface_tension
                             