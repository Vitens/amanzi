from .water_properties import Water
from .air_properties import Air
import math
from .packing_properties import packing


class run_engelstichlmair:
  def __init__(self, T_liq,T_gas, packing_type):
    self.temperature = T_liq
    self.packing_type = packing_type
    self.pressure = 1.013e5
    self.temperature_gas = T_gas

  def loading(self,u_l):
    liquid = Water(self.temperature)
    rho_l = liquid.density()        # kg/m³
    sigma_l = liquid.tension()      # N/m
    mue_l = liquid.dyn_viscosity()  
    g = 9.81
    a_geo =packing()[self.packing_type]['ageo']
    
    #static holdup  Engel/Stichlmair Eq.2
    h_stat=0.033*math.exp(-0.22*rho_l*g/sigma_l/(a_geo**2)) #has to be value between 0-1
    
    #dynamic holdup  Engel/Stichlmair Eq.4 
    A1 = (u_l*a_geo**0.5)/(g**0.5)     #u_l in m³/m²/h need to be converted to seconds
    A2 = mue_l*(a_geo**1.5)/(rho_l*g**0.5)
    A3 = sigma_l*(a_geo**2)/rho_l/g
    h_dyn_0 = 3.6*(A1**0.66)*(A2**0.25)*(A3**0.1)  #has to be value between 0-1

    return h_dyn_0, h_stat
  def flooding_factor(self, dp_dry,u_l,rho_l,rho_g):
      cap_liq = u_l*math.sqrt(rho_l/(rho_l-rho_g))
      _, dp_dry_fl = self.flooding_line(cap_liq,1)

      flooding_factor= math.sqrt(dp_dry/dp_dry_fl)

      return flooding_factor
                        

  def operating_point(self,liq_in,RQ,d):
      liquid = Water(self.temperature)
      rho_l = liquid.density()        # kg/m³
      sigma_l = liquid.tension()      # N/m
      g = 9.81
      gas = Air(self.temperature_gas,self.pressure)
      rho_g = gas.density()           # kg/m³
      a_geo =packing()[self.packing_type]['ageo']
      eta=packing()[self.packing_type]['void']
      u_l =liq_in/(math.pi*0.25*d**2)/3600  #m/s
      u_g=u_l*RQ                            #m/s

      F=u_g*math.sqrt(rho_g)
      d_l=0.4*math.sqrt(6*sigma_l/g/(rho_l-rho_g))

      a=packing()[self.packing_type]['a'] 
      b=packing()[self.packing_type]['b']
      F=u_g*math.sqrt(rho_g) 
      dp_dry = 10**b*F**a
     
      h_dyn_0,h_stat=self.loading(u_l)
      h_dyn = h_dyn_0
      dp_tot = 0

      for i in range(10):
          dp_tot = (((6*h_dyn)/d_l + a_geo) / (a_geo) * (eta/(eta-h_dyn))**4.65) * dp_dry
          h_dyn = h_dyn_0 * (1+36*((dp_tot)/(rho_l*g))**2)
      h_tot=h_dyn+h_stat 
      flooding_factor = self.flooding_factor(dp_dry,u_l,rho_l,rho_g)

      return dp_dry, dp_tot, h_tot, F ,flooding_factor
  
  def flooding_line(self, cap_liq, flooding_factor):
      def Capacity_gas(u_g):
        return u_g*math.sqrt(rho_g/(rho_l-rho_g))
  
      def convert_cap_to_u_l(cap_liq):
        return cap_liq/math.sqrt(rho_l/(rho_l-rho_g))
      
      liquid = Water(self.temperature)
      rho_l = liquid.density()        # kg/m³
      sigma_l = liquid.tension()      # N/m
      gas = Air(self.temperature_gas,self.pressure)
      rho_g = gas.density()           # kg/m³
      g= 9.81

      u_l = convert_cap_to_u_l(cap_liq)               # m³/m²/s gas loading
      #Packing properties
      a_geo= packing()[self.packing_type]['ageo']   # m²/m³
      eta = packing()[self.packing_type]['void']    #void fraction
      a=packing()[self.packing_type]['a']  # Raflux 50
      b=packing()[self.packing_type]['b']

      d_l=0.4*math.sqrt(6*sigma_l/g/(rho_l-rho_g))      
      h_dyn_0,h_stat=self.loading(u_l)
      
      ## Operating Point
      X=3600*eta+186480*h_dyn_0*eta+32280*d_l*a_geo*eta+191844*h_dyn_0**2+95028*d_l*a_geo*h_dyn_0+10609*d_l**2*a_geo**2
      dp_tot_fl =(rho_l*g*(249*h_dyn_0*((X**0.5)-60*eta-558*h_dyn_0-103*d_l*a_geo))**0.5)/(2988*h_dyn_0) #Pa/m             
      
      #dynamic liquid holdup at flooding, Engel/Stichlmair Eq.15                   
      h_dyn_flooding=h_dyn_0*(1+(6*dp_tot_fl/rho_l/g)**2)   
      #fictive dry pressure drop at flooding, Engel/Stichlmair Eq.15 
      dp_dry_fl = dp_tot_fl *a_geo *(1-(h_dyn_flooding/eta))**4.65/((6*h_dyn_flooding/d_l)+a_geo) #Pa/m
      
      dp_dry= dp_dry_fl*(flooding_factor**2)

      F=(dp_dry/10**b)**(1/a)
      u_g=F/math.sqrt(rho_g) 

      cap_g=Capacity_gas(u_g)
      return cap_g, dp_dry_fl


  
  
