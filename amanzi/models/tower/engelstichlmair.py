from .water_properties import Water
from .air_properties import Air
import math
import numpy as np


def run_engelstichlmair(flow, packing_height, packing, RQ, component, c_in, c_gas):
  def loading(T,u_l):
    water_surf_tension=water(T)[3]
    water_density= water(T)[2]
    water_dyn_viscosity= water(T)[0]
    p=1.023
    air_density=air(T, p)[0]
    air_dynamic_viscosity= air(T,p)[1]
    
    #static holdup  Engel/Stichlmair Eq.2
    h_stat=0.033*math.exp(-0.22*water_density*g/water_surf_tension/(a_geo**2)) #has to be value between 0-1
    
    #dynamic holdup  Engel/Stichlmair Eq.4 
    A1 = ((u_l/(3600))*a_geo**0.5)/(g**0.5)     #u_l in m³/m²/h need to be converted to seconds
    A2 = water_dyn_viscosity*(a_geo**1.5)/(water_density*g**0.5)
    A3 = water_surf_tension*(a_geo**2)/water_density/g
    h_dyn_0 = 3.6*(A1**0.66)*(A2**0.25)*(A3**0.1)  #has to be value between 0-1
    return h_dyn_0, h_stat


  def operating_point(u_l):
      water_surf_tension=water(T)[3]
      water_density= water(T)[2]
      water_dyn_viscosity= water(T)[0]
      p=1.023
      air_density=air(T, p)[0]
      air_dynamic_viscosity= air(T,p)[1]

      u_g=u_l*RQ/3600   #m/s
      eta=void_fraction
      F=u_g*math.sqrt(air_density)
      d_l=0.4*np.sqrt(6*water_surf_tension/g/(water_density-air_density))
      #alternative for dp_dry
      #dp_dry = 10**b*F**a
      d_p=6*(1-void_fraction)/a_geo
      Re = d_p*u_g*air_density/(air_dynamic_viscosity*(1-void_fraction))
      #Friction factor
      f=150/Re+1.75
      dp_dry=(f*a_geo*air_density*u_g**2)/(8*void_fraction**4.65)
      h_dyn_0,h_stat=loading(T,u_l)
      h_dyn = h_dyn_0
      dp_tot=0
      for i in range(10):
          dp_tot = (((6*h_dyn)/d_l + a_geo) / (a_geo) * (eta/(eta-h_dyn))**4.65) * dp_dry
          h_dyn = h_dyn_0 * (1+36*((dp_tot)/(water_density*g))**2)
      h_tot=h_dyn+h_stat    
      print(f"Dry Pressure Drop: \t\t {dp_dry/100:.5f} mbar/m")
      print(f"Operationg Pressure Drop: \t {dp_tot/100:.5f} mbar/m")
      print(f"F-factor: \t\t\t {F:.2f} ")
      print(f"Liquid Holdup: \t\t\t {h_tot*100:.2f}%")
      return dp_dry, dp_tot, h_dyn
  ## Packing
  a_geo = 110 #m²/m³  specific area of packing
  void_fraction=0.93 #[-] Void fraction of packing
  a = 2.0177 # A-factor
  b = 1.533 # B-factor

  ## Column dimensions
  d=120 #mm column diameter
  Area=0.25*1e-6*np.pi*d**2 #m² Crosssection area
  V_liq=1 #m³/h Volumeflowrate of water
  u_l=V_liq/Area #m³/m²/h liquid load

  ## Operating conditions
  T=5 #C Temperature
  RQ=50 # Gas to liquid ratio
  g = 9.81 #m/s²  Earth acceleration
  operating_point(u_l)
  
  return T