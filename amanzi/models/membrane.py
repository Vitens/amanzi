from .model import Model
from .submodels.splitter import Splitter
from .membranestack import MembraneStack
from pprint import pprint as pprint
import pandas as pd

class Membrane(Model, Splitter):
  parametric_model = ['base','model', 'membrane']

  def __init__(self, config, pp):
    super().__init__(config, pp)
    if not pp:
      return

    # set split fraction to recovery
    self.split = self.parameters.get('recovery', 0.8)

    dp_stage = self.parameters.get('pressure_loss_between_stages', 2)/9.81 # convert from mH2O to bar

    self.concentrate = pp.add_solution({})

    self.feed_pressure = 10

    # store the results of the calculation during run_quality to use during design
    self.calculation_results = {
      'element_results': []
    } 

    self.stack = MembraneStack(self.parameters['membrane_type'], self.staging, self.number_of_modules, dp_stage)

  @property
  def staging(self):
    """
    Returns the number of vessels per stage as a list
    if optiflux is enabled, the number of vessels is doubled

    Returns:
        list: number of vessels per stage
    """
    number_of_stages = self.parameters.get('number_of_stages', 3)
    modifier = 2 if self.parameters.get('optiflux', False) else 1

    return [self.parameters[f'stage{n+1}_vessels'] * modifier for n in range(number_of_stages)]

  @property
  def number_of_modules(self):
    """
    Returns the number of modules per stage
    if optiflux is enabled, the number of modules is halved

    Returns:
        int: number of modules per stage
    """
    return int(self.parameters['modules_per_vessel'] * (0.5 if self.parameters.get('optiflux', False) else 1))

  @property
  def context(self):
      ctx = super().context
      ctx['calculated_feed_pressure'] = self.feed_pressure
      ctx['membrane'] = self.stack.membrane
      ctx['element_results'] = pd.DataFrame(self.calculation_results['element_results'])
      return ctx

  @property
  def emitter_solutions(self):
      return {'waste': self.concentrate}
  

  def run_quality(self, type, total_inflow, solution):
    """
    Run Membrane Stack model and return solution
    """
    # capacity
    capacity = self.parameters['nominal_capacity']
    recovery = self.parameters['recovery']

    # solve pressure
    required_pressure = self.stack.solve_pressure(Q_f=capacity, C_f=solution.tds, T=solution.temperature, R=recovery)
    # solve hydraulics
    Q_p, results = self.stack.run_hydraulics(Q_f=capacity, C_f=solution.tds, P_f=required_pressure, T=solution.temperature)
    # solve quality
    permeate, concentrate, stage_permeate, stage_concentrate, element_permeate, element_concentrate = self.stack.run_quality(solution, results)


    self.calculation_results = {
       'Q_p': Q_p,
       'P_f': required_pressure,
       'element_results': results,
       'stage_permeate': stage_permeate,
       'stage_concentrate': stage_concentrate,
       'element_permeate': element_permeate,
       'element_concentrate': element_concentrate,
    }

    self.feed_pressure = required_pressure
    self.concentrate = concentrate

    return permeate
  
  @property
  def stage_results(self):
    """
    Calculate results per stage
    """
    num_stages = self.parameters.get('number_of_stages', 3)

    results_df = pd.DataFrame(self.calculation_results['element_results'])

    stage_results = []

    for stage in range(1, num_stages+1):

      vessels = self.staging[stage-1]

      Q_f = results_df.loc[results_df['stage'] == stage, 'Q_f'].iloc[0] * vessels  # feed flow rate (m3/h) of first element, multiplied by number of vessels
      Q_c = results_df.loc[results_df['stage'] == stage, 'Q_c'].iloc[-1] * vessels  # concentrate flow rate (m3/h) of last element, multiplied by number of vessels
      Q_p = Q_f - Q_c
      P_f = results_df.loc[results_df['stage'] == stage, 'P_f'].iloc[0] # feed pressure (bar) of first element
      P_c = results_df.loc[results_df['stage'] == stage, 'P_c'].iloc[-1] # concentrate pressure (bar) of last element
      D_p = P_f - P_c

      P_p = self.hydraulics.head_out / 9.81
      P_f += P_p # add permeate pressure to feed pressure
      P_c += P_p # add permeate pressure to concentrate pressure

      feed = self.calculation_results['stage_concentrate'][stage-2] if stage > 1 else self.quality.influent.product

      stage_results.append({
        'Q_f': Q_f,         # feed flow rate (m3/h)
        'Q_c': Q_c,         # concentrate flow rate (m3/h)
        'Q_p': Q_p,         # permeate flow rate (m3/h)
        'R': Q_p / Q_f,     # recovery
        'P_f': P_f,         # feed pressure (bar)
        'P_c': P_c,         # concentrate pressure (bar)
        'P_p': P_p, # permeate pressure (bar)
        'D_p': D_p,          # pressure drop (bar
        'J_max': results_df.loc[results_df['stage'] == stage, 'J'].max(), # max flux (L/m2/h)
        'J_avg': results_df.loc[results_df['stage'] == stage, 'J'].mean(), # average flux (L/m2/h)
        'J_min': results_df.loc[results_df['stage'] == stage, 'J'].min(), # min flux (L/m2/h
        'C_f': results_df.loc[results_df['stage'] == stage, 'C_f'].iloc[0], # feed TDS (ppm)
        'C_c': results_df.loc[results_df['stage'] == stage, 'C_c'].iloc[-1], # concentrate TDS (ppm)
        'C_p': self.calculation_results['stage_permeate'][stage-1].tds, # permeate TDS (ppm)
        'permeate_quality': self.calculation_results['stage_permeate'][stage-1].summary, # permeate quality
        'feed_quality': feed.summary, # permeate quality
        'concentrate_quality': self.calculation_results['stage_concentrate'][stage-1].summary, # permeate quality
        'feed_saturation': self.supersaturation(feed),
        'concentrate_saturation': self.supersaturation(self.calculation_results['stage_concentrate'][stage-1]),
      })

    return stage_results
  
  @staticmethod
  def supersaturation(sol):
      """ Calculate supersaturation of scaling components in a solution 

      args:
        sol (Solution): Solution object

      returns:
        dict: supersaturation index of each scaling component
      """

      return {
        'Calcite (CaCO3)': sol.si('Calcite'),
        'Gypsum (CaSO4)': sol.si('Gypsum'),
        'Hydroxyapatite': sol.si('Hydroxyapatite'),
        'Barite (BaSO4)': sol.si('Barite'),
        'Celestite (SrSO4)': sol.si('Celestite'),
        'Fluorite (CaF2)': sol.si('Fluorite'),
        'Silica (SiO2)': sol.si('Silica'),
      }
  
  def design(self):

     influent = self.quality.influent.product

     stage_results = self.stage_results
     element_results = self.calculation_results['element_results']
     element_concentrate = self.calculation_results['element_concentrate']
     # calculate super saturations
     

     si = [self.supersaturation(s) for s in element_concentrate]

     def stream_results(stream):
      return [
        {'name': 'pH', 'value': stream.pH, 'units': '-'},
        {'name': 'EGV', 'value': stream.sc20/100, 'units': 'mS/m'},
        {'name': 'TDS', 'value': stream.tds, 'units': 'mg'},
        {'name': 'Na', 'value': stream.total('Na', 'mg'), 'units': 'mg'},
        {'name': 'Cl', 'value': stream.total('Cl', 'mg'), 'units': 'mg'},
      ]

     return {
       'stage_results': stage_results,
       'element_results': element_results,
       'streams': {
         'influent': stream_results(influent),
         'effluent': stream_results(self.quality.effluent.product),
         'concentrate': stream_results(self.concentrate)
       },
       'supersaturation': si
       }
    


