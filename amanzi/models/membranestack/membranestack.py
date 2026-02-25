import math
from dataclasses import dataclass
import numpy as np
import pandas as pd
import os
from amanzi.utils.optimize import fmin
import pprint

class MembraneStack():

  def __init__(self, membrane_type, staging, elements_per_stage, dp_stage=0.2):

    db = pd.read_csv(os.path.dirname(__file__)+'/membrane_database.csv', sep=';')
    self.membrane = db.loc[db['name'] == membrane_type].iloc[0]
    self.staging = staging
    self.elements_per_stage = elements_per_stage
    self.dp_stage = dp_stage

    # cache to store k_w values
    self.k_w_cache = {}
  
  def k_w(self, temperature: float =10.0) -> float:
    """
    Estimate the water permeability coefficient Kw for a given temperature
    based on the feed concentration, salt rejection and recovery of the membrane
    during test conditions.

    Procedure used as described in https://www.researchgate.net/publication/351606477

    Parameters:
      temperature (int): temperature in degrees Celsius
    
    Returns:
      float: water permeability coefficient in m3/m2*bar*h
    """
    # relevant constants
    DP_E = 0.2 # pressure drop across element in bar
    OSM_RATIO = 0.8 / 1000 # Osmotic pressure coefficient for NaCl in bar/ppm
    KW_TEMP_CORRECTION = 0.0300 # Kw temperature correction factor per degree C

    # check if k_w value is already in cache
    if temperature in self.k_w_cache:
      return self.k_w_cache[temperature]
    
    # load test conditions into variables
    C_fs = self.membrane.test_concentration # feed concentration in ppm NaCl
    SR = self.membrane.rejection # salt rejection in fraction
    R_e = self.membrane.test_recovery # recovery in fraction
    P_f = self.membrane.test_pressure # feed pressure in bar

    # calculate concentration in concentrate stream
    C_cs = C_fs * (1-R_e*(1-SR)) / (1-R_e) # ppm NaCl

    # calculate osmotic pressure
    P_osm_f = (C_fs * OSM_RATIO + C_cs * OSM_RATIO) / 2  # average osmotic pressure of feed in bar
    P_osm_p = 0.01 * P_osm_f # estimated osmotic pressure of permeate in bar
    P_osm = P_osm_f - P_osm_p # net osmotic pressure in bar

    # calculate net driving pressure
    NDP = P_f - DP_E/2 - P_osm # net driving pressure in bar
    # calculate flux
    J = self.membrane.test_production / self.membrane.area
    # calculate Kw at 25 degrees C
    Kw_25 = J / NDP # m3/m2*bar*h

    # correct for temperature, assume 3% change in Kw per degree C
    kw = Kw_25 * (1+KW_TEMP_CORRECTION * (temperature - 25)) # m3/m2*bar*h

    # store k_w value in cache
    self.k_w_cache[temperature] = kw

    return kw
  
  @staticmethod
  def kinematic_viscosity(T : float = 25.0) -> float:
    """
    Calculate the kinematic viscosity of water at a given temperature
    2-degree polynomial fit based on data from:
    https://www.engineeringtoolbox.com/water-dynamic-kinematic-viscosity-d_596.html

    Parameters:
      T (float): temperature in degrees Celsius
    
    Returns:
      float: kinematic viscosity in m2/s
    """
    return (-9E-06 * T**3 + 0.0011 * T**2 - 0.0583 * T + 1.7913)*1E-6 # m2/s

  def headloss(self, Qf: float, T: float = 25.0) -> float:
    """
    Calculate the headloss across a single membrane element
    based on the velocity of the feedwater, kinematic viscosity and spacer height

    Calculation based on Water Treatment - Nanofiltration and Reverse Osmosis - P195 (TU Delft)

    Parameters:
      Qf (float): feedwater flow rate in m3/s
      T (float): temperature in degrees Celsius

    Returns:
      tuple: headloss in bar, velocity in m/s
    """

    # constants
    CORRECTION_FACTOR = 1.2 # correction factor for spacer height to fit to experimental data
    ELEMENT_LENGTH = 1.016 # length of a single membrane element in meters
    POROSITY = 0.85 # porosity of the membrane spacer (estimate)
    RHO = 1000 # density of water in kg/m3

    total_spacer_width = (self.membrane.area/ELEMENT_LENGTH)/2 # total spacer width in m
    spacer_height = self.membrane.spacer_height * 2.54e-5 * CORRECTION_FACTOR # convert mil to meters, apply correction factor

    # calculate effective area and velocity
    A_effective = POROSITY * spacer_height * total_spacer_width # effective area in m2
    velocity = (Qf / A_effective) / 3600 # convert m/h to m/s

    # calculate Reynolds number and friction_factor
    reynolds = velocity * spacer_height / self.kinematic_viscosity(T)
    friction_factor = 6.23 * reynolds**-0.3 # p.195 of Water Treatment - Nanofiltration and reverse osmosis
    friction_factor = friction_factor if friction_factor > 0 else 0

    # calculate headloss in Pascal
    dP = friction_factor * ELEMENT_LENGTH * RHO * velocity**2 / (2 * spacer_height) # Pressure loss in Pascal

    return dP*1e-5, velocity # convert Pa to bar
  
  def element_recovery(self, R_init, C_f, Q_f, P_f, T, minimize=True):
    """
    Calculate the recovery of a single membrane element based on the feed concentration,
    feed flow rate, feed pressure, temperature and initial estimated recovery.

    Parameters:
      R_init (float): initial estimate of the recovery
      C_f (float): feed TDS in ppm
      Q_f (float): feed flow rate in m3/h
      P_f (float): feed pressure in bar
      T (float): temperature in degrees Celsius
      minimize (bool): if True, return the absolute difference between the initial and calculated recovery
                       else, return a tuple with the calculated values
    
    Returns:
      float or tuple: absolute error between initial and calculated recovery if minimize=True
                      or a tuple with the calculated values:
                        P_c (float): pressure at concentrate in bar
                        DP_e (float): pressure drop across element in bar
                        V_e (float): crossflow velocity in m/s
                        C_c (float): concentrate TDS in ppm
                        C_p (float): permeate TDS in ppm
                        Q_p (float): permeate flow rate in m3/h
                        NDP (float): net driving pressure in bar
                        J (float): flux in L/m2/h
                        R_calc (float): calculated recovery in fraction
                        P_osm (float): average osmosis pressure in
    """
    # constants
    OSM_RATIO = 0.6 / 1000 # Osmotic pressure coefficient for TDS in bar/ppm

    R_init = R_init[0]

    # calculate pressure drop across element
    DP_e, V_e = self.headloss(Q_f - 0.5*Q_f*R_init, T) # pressure drop across element in bar
    # calculate pressure at concentrate
    P_c = P_f - DP_e # pressure at concentrate is the feed pressure minus the pressure drop across the element in bar

    # calculate concentrate and permeate TDS
    C_c = (C_f * (1 - R_init * (1 - self.membrane.rejection)) / (1 - R_init)) # concentrate TDS in ppm
    # C_p is 
    C_p = (C_f + C_c)/2 * (1 - self.membrane.rejection) # permeate TDS in ppm, assume average of feed and concentrate

    # calculate osmotic pressures
    P_osm = (C_f * OSM_RATIO + C_c * OSM_RATIO) / 2  # average osmosis pressure of feed in bar
    P_osm_p = C_p * OSM_RATIO # osmotic pressure of permeate in bar

    # calculate net driving pressure
    # NDP = P_f - DP_e/2 - P_osm + P_osm_p # net driving pressure in bar 
    NDP = P_f - DP_e/2 - P_osm # net driving pressure in bar 

    # calculate flux and permeate flow rate
    J = NDP * self.k_w(T) # flux in m3/m2/h
    Q_p = J * self.membrane.area # permeate flow rate in m3/h
    J *= 1000 # convert to L/m2/h

    # calculate recovery
    R_calc = Q_p / Q_f # recovery in fraction

    if minimize:
      return abs(R_init - R_calc) # return absolute error between initial and calculated recovery
    else:
      return P_c, DP_e, V_e, C_c, C_p, Q_p, NDP, J, R_calc, P_osm
  
  def _to_scalar(self, x):
    """Convert numpy array/scalar to Python float to prevent array propagation from scipy."""
    return float(np.asarray(x).ravel()[0])

  def run_hydraulics(self, Q_f: float, C_f: float, P_f: float, T: float = 25.0):
    """
    Run the hydraulic calculations for a membrane stack based on the feed flow rate,
    feed pressure and temperature.

    Parameters:
      Q_f (float): feed flow rate in m3/h
      P_f (float): feed pressure in bar
      C_f (float): feed TDS in ppm
      T (float): temperature in degrees Celsius
    
    Returns:
      float, list: total permeate flow rate in m3/h and a list of dictionaries with the results per element
    """
    # Scipy minimize passes P_f as array; convert at boundary to prevent propagation
    P_f = self._to_scalar(P_f)

    # constants
    DP_PIPES = self.dp_stage # pressure drop in piping between stages in bar
    KP = 0.99 # beta factor constant (Hydranautics)

    # initialize variables
    Q_p_tot = 0.0 # total permeate flow rate in m3/h
    results = [] # list to store calculation results per element

    stage_inflow = Q_f # 1st stage inflow is the feed flow rate of the stack

    # iterate over each stage
    for stage_num, vessels in enumerate(self.staging):

      Q_f = stage_inflow / vessels # Get feed flow per vessel in m3/h

      for elem in range(self.elements_per_stage):
        # calculate recovery for each element using fmin to minimize the error, starting at 0.1
        R_e_initial = 0.1 + elem * 0.01 # initial recovery estimate, estimate increase by 0.01 per element
        R_e = self._to_scalar(fmin(self.element_recovery, [R_e_initial], args=(C_f, Q_f, P_f, T, True), xtol=0.001, ftol=0.001)['x'][0])

        # calculate results for membrane element using the final recovery estimate
        P_c, DP_e, V_e, C_c, C_p, Q_p, NDP, J, R_e, P_osm = self.element_recovery([R_e], C_f, Q_f, P_f, T, False)

        # calculate beta factor (average of feed and concentrate flow)
        Q_avg = (Q_f + (Q_f - Q_p)) / 2
        beta = KP * math.exp(Q_p / Q_avg)

        # store results in a dictionary and append
        results.append({
          'stage': stage_num+1,     # stage number (-)
          'element': elem+1,        # element number (-)
          'P_f': P_f,               # feed pressure (bar)
          'DP_e': DP_e,             # pressure drop across element (bar)
          'V_e': V_e,               # crossflow velocity (m/s)
          'P_c': P_c,               # pressure at concentrate (bar)
          'P_osm': P_osm,           # average osmotic pressure (bar)
          'J': J,                   # flux (L/m2/h)
          'NDP': NDP,               # net driving pressure (bar)
          'C_f': C_f,               # feed TDS (ppm)
          'C_c': C_c,               # concentrate TDS (ppm)
          'C_p': C_p,               # permeate TDS (ppm)
          'Q_f': Q_f,               # feed flow rate (m3/h)
          'Q_c': Q_f - Q_p,         # concentrate flow rate (m3/h)
          'Q_p': Q_p,               # permeate flow rate (m3/h)
          'R_e': R_e,               # recovery (-)
          'beta': beta              # beta factor (-)
        })

        # set Q_f to Q_f - Q_p for next element calculation
        Q_f = Q_f - Q_p
        C_f = C_c
        P_f = P_c
        # update total permeate flow rate
        Q_p_tot += Q_p * vessels

      P_f -= DP_PIPES
      # set stage_inflow for next stage to total permeate flow rate for next stage
      stage_inflow = Q_f * vessels

    return Q_p_tot, results

  def solve_pressure(self, Q_f: float, C_f: float, T: float = 25.0, R: float = 0.8):
    """
    Calculate required feed pressure to achieve a given recovery for a given feed flow rate,
    feed TDS and temperature.

    Parameters:
      Q_f (float): feed flow rate in m3/h
      C_f (float): feed TDS in ppm
      T (float): temperature in degrees Celsius
      R (float): target recovery in fraction
    """

    Q_perm_target = Q_f * R # target permeate flow rate in m3/h

    def optfun(P_f, target):
      Q_p, _ = self.run_hydraulics(Q_f, C_f, P_f[0], T)
      return abs(Q_p - target)
    
    # res = minimize(optfun, x0=10, method='COBYLA', tol=0.01, options={'disp': False}, args=(Q_perm_target))
    res = fmin(optfun, [10], args=(Q_perm_target, ))

    return self._to_scalar(res['x'][0])
  
  @staticmethod
  def balance_solution(composition):
    """
    Balance the composition of a solution based on the charge of the species
    adding a new species 'Nmod' or 'Pmod' to balance the charge.
    This prevents the charge error of the solution leading to incorrect values for pH
    """

    # calculate charge balance
    cbalance = 0
    
    # iterate over each species in the composition, calculate charge and add to balance
    for species, quantity in composition.items():
        if species[-1] == "-":
            charge = -1
        elif species[-1] == "+":
            charge = 1
        elif species[-2] == "-":
            charge = -int(species[-1])
        elif species[-2] == "+":
            charge = int(species[-1])
        else:
            charge = 0
        cbalance += quantity * charge

    # add Nmod or Pmod species to balance the charge
    if cbalance > 0:
        composition['Nmod'] = cbalance
    else:
        composition['Pmod'] = -cbalance
    return composition
  
  def calculate_element_solution(self, feed, R_e):
    """ 
    Calculate the concentrate and permeate solutions for a single element based on the recovery and a feed solution 

    parameters:
      feed (Solution): PhreeqPython solution object
      R_el (float): recovery of the element
    
    returns:
      tuple: concentrate and permeate solutions (Solution)
    """
    # constants
    IGNORED_ELEMENTS = ["H2", "H+", "OH-", "H2O", "CO2", "Mtg", "Ntg", "Oxg", "O2", "CH4"] # elements to ignore because they either are gasses or are not relevant for the calculation

    # changes in composition of the permeate and concentrate solution
    permeate_changes = {}
    concentrate_changes = {}

    # iterate over each element in the feed solution
    for el, conc in feed.species.items():
      # dont remove gasses
      if el not in IGNORED_ELEMENTS:
        permeate_changes[el] = conc * -self.membrane.rejection # remove the fraction of the element based on the rejection of the membrane
        concentrate_changes[el] = (conc * (1 - R_e * (1 - self.membrane.rejection)) / (1 - R_e)) - conc # add the difference between the concentrate and feed to the concentrate solution
    
    # balance the solutions to prevent charge errors
    permeate_changes = self.balance_solution(permeate_changes)
    concentrate_changes = self.balance_solution(concentrate_changes)

    print('wtf mate', R_e)

    # create the concentrate and permeate solutions and apply the changes
    permeate = feed.copy().change(permeate_changes, units='mol')
    concentrate = feed.copy().change(concentrate_changes, units='mol')


    return concentrate, permeate
      
  def run_quality(self, solution, results):
    """
    Calculate all solutions based on the results of a membrane stack calculation

    parameters:
      solution (Solution): PhreeqPython solution object
      results (list): list of dictionaries with the results per element
    
    returns:
      tuple: stack permeate and concentrate solutions, list of stage permeate and concentrate solutions, list of element permeate and concentrate
    """

    feed_solution = solution.copy() # copy the solution object
    # get phreeqpython instance
    pp = solution.pp

    # store results for each element and each stage
    element_permeate = []
    element_concentrate = []

    stage_permeate_flows = []
    stage_permeate = []
    stage_concentrate = []

    result_index = 0

    for stage_num, vessels in enumerate(self.staging):

      stage_flows = []

      for elem in range(self.elements_per_stage):
        Q_p = results[result_index]['Q_p'] # get the permeate flow rate
        R_e = results[result_index]['R_e'] # get the recovery of the element
        conc, perm = self.calculate_element_solution(feed_solution, R_e)
        element_permeate.append(perm)
        element_concentrate.append(conc)
        # set feed solution to concentrate solution for next element
        feed_solution = conc.copy()

        stage_flows.append(Q_p)

        result_index += 1
      
      # calculate stage permeate
      stage_flow = sum(stage_flows) # sum of all element permeate flows
      # store stage permeate flow
      stage_permeate_flows.append(stage_flow)

      # calculate stage permeate mixture
      permeate_mixture = {element_permeate[stage_num * self.elements_per_stage + idx]: stage_flows[idx]/stage_flow for idx in range(self.elements_per_stage)}

      # calculate stage permeate and concentrate composition
      stage_permeate.append(pp.mix_solutions(permeate_mixture))
      stage_concentrate.append(feed_solution.copy())
  
    # calculate total stack permeate quality
    total_permeate = sum(stage_permeate_flows)
    stack_permeate_mixture = {stage_permeate[idx]: stage_permeate_flows[idx]/total_permeate for idx in range(len(self.staging))}
    stack_permeate = pp.mix_solutions(stack_permeate_mixture)
    stack_concentrate = feed_solution.copy()

    return stack_permeate, stack_concentrate, stage_permeate, stage_concentrate, element_permeate, element_concentrate