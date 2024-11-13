from .solver import Solver
from pprint import pprint as pprint

class EnergySolver(Solver):

  def solve(self, until=None):

    total_distribution = self.scenario.solvers['quantity'].summary()['total_distribution'] * 1e6
    # sum energy consumption for each model
    models = self.scenario.models if not until else {until: self.scenario.models[until]}
    for m in models.values():
      outputs = [o for o in m.output_parameters.values() if o.category == 'energy' and o.uom == 'kWh/m3' and not o.hidden(m.context) and o.parent is None]

      # specific energy consumption in kWh/m3 produced by the model
      m.energy.model_specific_consumption = energy_consumption = sum([m.get_output(o.name) for o in outputs])

      # total energy consumption per year
      if m.type == 'groundwater':
        m.energy.total_consumption = energy_consumption * m.quantity.outflow['product'] * 1e6 # total energy consumption per year
      else:
        m.energy.total_consumption = energy_consumption * m.quantity.inflow['product'] * 1e6 # total energy consumption per year

      # specific energy consumption in kWh/m3 produced by the treatment plant
      # total production in m3/y
      m.energy.specific_consumption = m.energy.total_consumption / total_distribution

    # gather hydraulic losses from connections
    hydraulic_loss = 0
    for _,c in self.scenario.connections.items():
      if c.hydraulics.efficiency is not None:
        hydraulic_loss += 1/3600 * c.quantity.flow * c.hydraulics.headloss * 9.81 * 1e6 * 1/c.hydraulics.efficiency
    
    self.total_hydraulic_loss = hydraulic_loss
    self.specific_hydraulic_loss = hydraulic_loss / total_distribution
    

  def summary(self):

    results = []

    for _,m in self.scenario.models.items():
      results.append([
        m.name, [
          {'name': 'specific_consumption', 'value': m.energy.specific_consumption, 'uom': 'kWh/m3', 'precision': 3, 'positive': False},
          {'name': 'model_specific_consumption', 'value': m.energy.model_specific_consumption, 'uom': 'kWh/m3', 'precision': 3, 'positive': False},
          {'name': 'total_consumption', 'value': m.energy.total_consumption/1e3, 'uom': 'MWh/y', 'precision': 0, 'positive': False}
        ],
        m.index
      ])
    
    if self.total_hydraulic_loss > 0:
      results.append([
        'Hydraulic losses', [
          {'name': 'specific_consumption', 'value': self.specific_hydraulic_loss, 'uom': 'kWh/m3', 'precision': 3, 'positive': False},
          {'name': 'model_specific-consumption', 'value': self.specific_hydraulic_loss, 'uom': 'MWh/y', 'precision': 0, 'positive': False},
          {'name': 'total_consumption', 'value': self.total_hydraulic_loss/1e3, 'uom': 'MWh/y', 'precision': 0, 'positive': False}
        ],
        1
      ])

    

    order = sorted(results, key=lambda x: x[2])
    models = [x[0] for x in order]
    metrics = [x[1] for x in order]

    total_consumption = sum([m.energy.total_consumption for m in self.scenario.models.values()])/1e3 + self.total_hydraulic_loss/1e3
    specific_consumption = sum([m.energy.specific_consumption for m in self.scenario.models.values()]) + self.specific_hydraulic_loss

    specific_consumption_distribution = sum([m.energy.specific_consumption for m in self.scenario.models.values() if m.type == 'output'])
    
    specific_consumption_production = specific_consumption - specific_consumption_distribution

    return {
      'order': models,
      'models': metrics,
      'total_consumption': total_consumption,
      'specific_consumption': specific_consumption,
      'specific_consumption_distribution': specific_consumption_distribution,
      'specific_consumption_production': specific_consumption_production,
      'metrics': [
        {'name': 'specific_consumption_production', 'value': specific_consumption_production, 'uom': 'kWh/m3', 'precision': 3, 'positive': False},
        {'name': 'specific_consumption_distribution', 'value': specific_consumption_distribution, 'uom': 'kWh/m3', 'precision': 3, 'positive': False},
        {'name': 'total_specific_consumption', 'value': specific_consumption, 'uom': 'kWh/m3', 'precision': 3, 'positive': False, 'group': 'total'},
        {'name': 'total_consumption', 'value': total_consumption, 'uom': 'MWh/y', 'precision': 0, 'positive': False, 'group': 'total'}
      ]
    }

