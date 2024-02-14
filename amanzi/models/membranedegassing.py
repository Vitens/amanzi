from .model import Model
from .submodels.balance import Balance

class Membranedegassing(Model, Balance):

  def __init__(self, config, pp: dict = {}) -> None:
    super().__init__(config, pp)
    self.configuration = config.get('configuration', {})
  

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

  def run_model(self, type, total_inflow, solution):

    rq1 = [float(self.configuration['stages'][0]['nitrogen_rq']), float(self.configuration['stages'][0]['carbon_dioxide_rq'])]
    rq2 = [float(self.configuration['stages'][1]['nitrogen_rq']), float(self.configuration['stages'][1]['carbon_dioxide_rq'])]

    vacuum1 = float(self.configuration['stages'][0]['vacuum'])
    vacuum2 = float(self.configuration['stages'][1]['vacuum'])

    effluent1, effluent2, gas1, gas2 = self.degass(solution, rq1, vacuum1, rq2, vacuum2)

    if(self.configuration.get('num_stages', 1) == 1):
      return effluent1
    return effluent2


  def design(self):

    rq1 = [float(self.configuration['stages'][0]['nitrogen_rq']), float(self.configuration['stages'][0]['carbon_dioxide_rq'])]
    rq2 = [float(self.configuration['stages'][1]['nitrogen_rq']), float(self.configuration['stages'][1]['carbon_dioxide_rq'])]

    vacuum1 = float(self.configuration['stages'][0]['vacuum'])
    vacuum2 = float(self.configuration['stages'][1]['vacuum'])

    effluent1, effluent2, gas1, gas2 = self.degass(self.influent, rq1, vacuum1, rq2, vacuum2)


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
      'influent': {n: v(self.influent) for n,v in values.items()},
      'effluent1': {n: v(effluent1) for n,v in values.items()},
      'effluent2': {n: v(effluent2) for n,v in values.items()},
      'gas1': {n: v(gas1) for n,v in gas_values.items()},
      'gas2': {n: v(gas2) for n,v in gas_values.items()}
    } 