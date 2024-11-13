from .model import Model
from .submodels.balance import Balance

class Membranedegassing(Model, Balance):
  parametric_model = ['base', 'model', 'membranedegassing', 'gasprocessing']

  def __init__(self, config, pp: dict = {}) -> None:
    super().__init__(config, pp)

    self.RQstage1 = [self.parameters['n2_rq_stage_1'], self.parameters['co2_rq_stage_1']]
    self.RQstage2 = [self.parameters['n2_rq_stage_2'], self.parameters['co2_rq_stage_2']]

    self.vacuum1 = self.parameters['vacuum_stage_1']
    self.vacuum2 = self.parameters['vacuum_stage_2']

    self.gas1 = None
    self.gas2 = None

  def degass(self, solution, rq1=[0,0], vacuum1=0.1, rq2=[0,0], vacuum2=0.1):

    total1 = rq1[0] + rq1[1]

    gas1 = self.pp.add_gas({
      'Ntg(g)': (rq1[0]/total1 * vacuum1 if total1 > 0 else 0), 
      'CO2(g)': (rq1[1]/total1 * vacuum1 if total1 > 0 else 0),
      'Mtg(g)': 0, 
      'H2O(g)': 0, 
    }, pressure = vacuum1, fixed_pressure = True, fixed_volume = False, volume = ((rq1[0] + rq1[1]) / vacuum1))

    total2 = rq2[0] + rq2[1]

    gas2 = self.pp.add_gas({
      'Ntg(g)': (rq2[0]/total2 * vacuum2 if total2 > 0 else 0),
      'CO2(g)': (rq2[1]/total2 * vacuum2 if total2 > 0 else 0),
      'Mtg(g)': 0, 
      'H2O(g)': 0, 
    }, pressure = vacuum2, fixed_pressure = True, fixed_volume = False, volume = ((rq2[0] + rq2[1]) / vacuum2))
    

    effluent1 = solution.copy().interact(gas1)
    effluent2 = effluent1.copy().interact(gas2)

    return effluent1, effluent2, gas1, gas2

  def run_quality(self, type, total_inflow, solution):

    effluent1, effluent2, gas1, gas2 = self.degass(solution,self.RQstage1, self.vacuum1, self.RQstage2, self.vacuum2)

    self.gas1 = gas1
    self.gas2 = gas2

    if(self.parameters['num_stages'] == 1):
      return effluent1
    return effluent2

  @property
  def context(self):
    ctx = super().context
    ctx['_gas'] = self.gas1
    ctx['_gas2'] = self.gas2
    ctx['pressure_loss'] = self.pressure_loss
    return ctx
  
  @staticmethod
  def pressure_loss(membrane_load, membrane_type):
    if membrane_type == "EXF14x40":
      return 0.0003 * membrane_load**2 + 0.0379*membrane_load - 0.0601
    else:
      return 0.0006 * membrane_load**2 + 0.0527*membrane_load + 0.2351
      


  def design(self):

    effluent1, effluent2, gas1, gas2 = self.degass(self.quality.influent.product ,self.RQstage1, self.vacuum1, self.RQstage2, self.vacuum2)

    values = {
      'pH': lambda s: s.pH,
      'CO2': lambda s: s.total('CO2', 'mg'),
      'CH4': lambda s: s.total('Mtg') * 16.04e3,
      'N2': lambda s: s.total('Ntg') * 28.0134,
      'SI': lambda s: s.si('Calcite')
    }

    gas_values = {
      'volume': lambda g: g.volume,
      'normal_volume': lambda g: g.volume * g.pressure,
      'CH4': lambda g: g.dry_fractions['Mtg(g)'] * 100,
      'CO2': lambda g: g.dry_fractions['CO2(g)'] * 100,
      'N2': lambda g: g.dry_fractions['Ntg(g)'] * 100,
    }


    return {
      'influent': {n: v(self.quality.influent.product) for n,v in values.items()},
      'effluent1': {n: v(effluent1) for n,v in values.items()},
      'effluent2': {n: v(effluent2) for n,v in values.items()},
      'gas1': {n: v(gas1) for n,v in gas_values.items()},
      'gas2': {n: v(gas2) for n,v in gas_values.items()}
    } 