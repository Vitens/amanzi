import numpy as np
import math
from .water_properties import Water
from .air_properties import Air

def run_mackoviak(Temp ,flow, packing_height, packing, RQ, component, c_in, c_gas):
    print(type(Temp))
    T=20
    p= 1.032e6
    liquid = Water(T)
    gas = Air(T,p)
    rho_l = liquid.density()
    rho_g = gas.density()
    sigma_l = liquid.tension()
    nue_g = liquid.dyn_viscosity() #check units
    g=9.81
    a_geo= 110
    d=1000# mm
    eta = 0.94 #void fraction
    Area= 1e-6*math.pi*d**2/4 #m² d in mm
    form_factor = 0.28 # packing dependent
    V_l = flow # m³/h
    u_l = V_l/Area/3600 # m³/m²/s
    m_yx = 0.6 # need values for Ch4 and Co2
    RQ= 40 # gas to liquid ratio
    u_v = u_l*RQ
    D_l = 10 # compound specific connection to C02 or CH4 necessary
    D_g= 0.5 # compound specific connection to C02 or CH4 necessary

    d_h = 4*eta/a_geo # hydraulic equivilant diameter

    beta_l_a_e =15.1*(D_l*(rho_l-rho_g)*g/sigma_l)**0.5*(a_geo/g)**(1/6)*u_l**(5/6)/((1-form_factor)**(1/3)*d_h**0.25)

    h_l = 0.57*(a_geo*u_l**2/g)**(1/3)  #liquid holdup
    u_r = u_v/(eta-h_l)+u_l/h_l #relative vapour velocity
    d_t = (sigma_l/((rho_l-rho_g)*g))**0.5 #droplet diameter

    Re_t = u_r * d_t/nue_g

    # Empirical parameters from Mackoviak
    C_v= 0.0285
    n=1
    m=6
    Sc_g= nue_g/D_g# calculate Schmidt number
    Sh_g = 2+C_v*Re_t**n*Sc_g**(1/3)
    beta_g = Sh_g*D_g/d_t 
    beta_g_real = beta_g*(1-h_l/eta)**6
    a_e=6*h_l/d_t

    HTU_og = u_v/beta_g_real/a_e+m_yx*u_l/RQ/beta_l_a_e

    H= packing_height # m user input
    c_l_in = c_in# user input
    c_g_in = c_gas  # user input or fixed values
    A=1/(m_yx*RQ) # stripping factor

    z= np.exp(H*(A-1)/HTU_og/A)
    c_g_out = c_g_in-((A-z)/(-A+1))*(c_g_in-(c_l_in*m_yx))
    c_l_out = c_l_in-RQ*(c_g_out-c_g_in)

    efficiency = (c_l_in-c_l_out)/c_l_in
    return 5