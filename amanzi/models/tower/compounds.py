


def D_in_water(A,B, temperature):
    return 10**(A+B/(273.15+temperature))
def D_in_air(A,B,C, temperature): #for 1 atm
    return A+B*(273.15+temperature)+C*(273.15+temperature)**2

def carbon_dioxide(temperature, pressure=1.023):
    A_water=-1.37281
    B_water=-997.66
    D_water=D_in_water(A_water,B_water,temperature)*1e-4 # m²/s
    
    A_air=-0.15731
    B_air=8.86E-04
    C_air=5.6831E-07
    D_air_atm=D_in_air(A_air,B_air,C_air,temperature)*1e-4 # m²/s
    #inclusion of pressure dependence
    D_air=D_air_atm*(1.023/pressure)  #ideal gas assumption
    
    Henry_coefficient = 1210 #bar 
    R = 8.314
    Henry_dimensionless = Henry_coefficient * R*temperature
    Molar_weight = 44 #kg/kmol
    return D_water, D_air , Henry_coefficient , Molar_weight