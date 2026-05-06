import math
import numpy as np
from .packing_properties import packing
from .compounds import Chemical
from .water_properties import Water
from .air_properties import Air

def run_onda(T_liq,T_gas,flow,diameter, packing_height, packing_type, RQ, compound, c_in, c_gas):
  liquid = Water(T_liq)
  rho_l = liquid.density()        # kg/m³
  sigma_l = liquid.tension()      # N/m
  mue_l = liquid.dyn_viscosity()
  M_l = liquid.mol_mass() 
  p=1.023e5
  gas = Air(T_gas,p)
  rho_g = gas.density()           # kg/m³
  mue_g = gas.dyn_viscosity()     # 
  M_g = gas.mol_mass()            # kg/mol molar weight
  g = 9.81 # m/s²
  column_area= math.pi*diameter**2/4

  m_l_flux = (rho_l*flow/3600)/column_area
  m_g_flux = (rho_g*flow*RQ/3600)/column_area
  a_geo =packing()[packing_type]['ageo']
  size =packing()[packing_type]['size']
  comp=Chemical(T_liq,T_gas)
  D_l =comp.properties()[compound]['Diff_water']*1e4  # cm²/s
  D_g =comp.properties()[compound]['Diff_air'] *1e4   # cm²/s
  Hc= comp.properties()[compound]['Henry'] #dimensionless Henry

  k_g =5.23*(m_g_flux/(a_geo*mue_g))**0.7*(mue_g/(rho_g*(D_g/10000)))**(1/3)*(a_geo*size/1000)**(-2) * (a_geo*D_g/10000) 
  a_t = (1-np.exp(-1.45*(sigma_l/(sigma_l*1.25))**0.75 * (m_l_flux/(a_geo*(mue_l)))**0.1 * ((m_l_flux**2*a_geo)/(rho_l**2*9.81))**(-0.05) * ((m_l_flux**2)/(rho_l*sigma_l*a_geo))**0.2))
  a_w= a_geo*a_t
  k_l1=(rho_l/(mue_l*g))**(-1/3)
  k_l2=0.0051*(m_l_flux/(a_w*mue_l))**(2/3) * (mue_l/(rho_l*(D_l/10000)))**(-0.5)*(a_geo*size/1000)**0.4
  k_l = k_l1*k_l2

  kl= 1/((1/(k_g*Hc))+(1/k_l))
  Kla= kl * a_w
  HTU_ov= m_l_flux/rho_l/Kla
  return   HTU_ov

