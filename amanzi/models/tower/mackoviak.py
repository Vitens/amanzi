import numpy as np
import math
from .water_properties import Water
from .air_properties import Air
from .packing_properties import packing
from .compounds import Chemical

def run_mackoviak(Temp ,flow, diameter,packing_height, packing_type, RQ, compound, c_in, c_gas):
    T=Temp
    p= 1.023e5
    liquid = Water(T)
    rho_l = liquid.density()        # kg/m³
    sigma_l = liquid.tension()      # N/m
    M_l = liquid.mol_mass()         # kg/mol

    gas = Air(T,p)
    rho_g = gas.density()           # kg/m³
    nue_g = gas.kin_viscosity()     # m²/s 
    M_g = gas.mol_mass()            # kg/mol molar weight
    g = 9.81 # m/s²

    #Packing properties
    a_geo= packing()[packing_type]['ageo']   # m²/m³
    eta = packing()[packing_type]['void']    #void fraction
    form_factor = packing()[packing_type]['form']              # packing dependent
    # Column Properties
    d=float(diameter)          # m
    Area= math.pi*d**2/4            # m² d in m
    # Column operation
    V_l = int(flow)        # m³/h
    u_l = V_l/Area/3600             # m³/m²/s liquid loading
    u_g = u_l*RQ                    # m³/m²/s gas loading
    # solved compounds
    comp=Chemical(T)
    D_l = comp.properties()[compound]['Diff_water']    # compound specific 
    D_g= comp.properties()[compound]['Diff_air']      #  compound specific 
    m_yx = comp.properties()[compound]['Henry']      # dimensionless Henry-volatility coeficcient Hcc_v
    # Empirical parameters from Mackoviak
    C_v= 0.0285
    n=1
    m=6
    # calculating HTU based on Mackoviak 2015
    d_h = 4*eta/a_geo               #m hydraulic equivilant diameter
    beta_l_a_e =(15.1*(D_l*(rho_l-rho_g)*g/sigma_l)**0.5*(a_geo/g)**(1/6)*u_l**(5/6))/((1-form_factor)**(1/3)*d_h**0.25) # 1/s
    h_l = 0.57*(a_geo*u_l**2/g)**(1/3)      # m³/m³ liquid holdup
    if h_l>1:
        print("Column is flooding")
    u_r = (u_g/(eta-h_l))+(u_l/h_l)         # m/s relative vapour velocity
    d_t = (sigma_l/((rho_l-rho_g)*g))**0.5  # m droplet diameter
    Re_t = u_r * d_t/nue_g                  # dimensionless    
    Sc_g= nue_g/D_g                         # calculate Schmidt number
    Sh_g = 2+(C_v*Re_t*Sc_g**(1/3))
    beta_g = Sh_g*D_g/d_t                   # m/s
    beta_g_real = beta_g*(1-(h_l/eta))**6   # m/s
    a_e=6*h_l/d_t                           # m²/m³
    l_g_ratio = (V_l*rho_l/M_l)/(V_l*RQ*rho_g/M_g) # molar ratio of liquid to gas stream
    lambda_s=m_yx/l_g_ratio
    HTU_og = (u_g/(beta_g_real*a_e))+(lambda_s*u_l/beta_l_a_e)

    return HTU_og