from .solver import Solver

class EnergySolver(Solver):

  def solve(self, until=None):

    total_distribution = self.scenario.solvers['quantity'].summary()['total_distribution'] * 1e6
    # sum energy consumption for each model
    for m in self.scenario.models.values():
      outputs = [o for o in m.output_parameters.values() if o.category == 'energy' and o.uom == 'kWh/m3' and not o.hidden(m.context)]

      # specific energy consumption in kWh/m3 produced by the model
      m.energy.model_specific_consumption = energy_consumption = sum([m.get_output(o.name) for o in outputs])
      # total energy consumption per year
      m.energy.total_consumption = energy_consumption * m.quantity.outflow['product'] * 1e6 # total energy consumption per year
      # specific energy consumption in kWh/m3 produced by the treatment plant

      # total production in m3/y
      m.energy.specific_consumption = m.energy.total_consumption / total_distribution

      
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

    order = sorted(results, key=lambda x: x[2])
    models = [x[0] for x in order]
    metrics = [x[1] for x in order]



    return {
      'order': models,
      'models': metrics,
      'metrics': [
        {'name': 'total_consumption', 'value': sum([m.energy.total_consumption for m in self.scenario.models.values()])/1e3, 'uom': 'MWh/y', 'precision': 0, 'positive': False},
        {'name': 'total_specific_consumption', 'value': sum([m.energy.specific_consumption for m in self.scenario.models.values()]), 'uom': 'kWh/m3', 'precision': 3, 'positive': False}
      ]
    }

