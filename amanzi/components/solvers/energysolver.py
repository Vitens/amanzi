from .solver import Solver

class EnergySolver(Solver):

  def solve(self, until=None):

    if until: # dont run in design mode
      return
    
    total_distribution = self.scenario.solvers['quantity'].summary()['total_distribution'] * 1e6
    # sum energy consumption for each model
    for m in self.scenario.models.values():
      outputs = [o for o in m.output_parameters.values() if o.category == 'energy' and o.uom == 'kWh/m3' and not o.hidden(m.context)]

      # specific energy consumption in kWh/m3 produced by the model
      m.energy.model_specific_consumption = energy_consumption = sum([o.calculate(m.context) for o in outputs])
      # total energy consumption per year
      m.energy.total_consumption = energy_consumption * m.quantity.outflow['product'] * 1e6 # total energy consumption per year
      # specific energy consumption in kWh/m3 produced by the treatment plant

      # total production in m3/y
      m.energy.specific_consumption = m.energy.total_consumption / total_distribution

      
  def summary(self):

    return {
      'model_specific_consumptions': {m.name: m.energy.model_specific_consumption for m in self.scenario.models.values()},
      'specific_consumptions': {m.name: m.energy.specific_consumption for m in self.scenario.models.values()},
      'total_consumptions': {m.name: m.energy.total_consumption for m in self.scenario.models.values()},
      'total_consumption': sum([m.energy.total_consumption for m in self.scenario.models.values()]),
      'total_specific_consumption': sum([m.energy.specific_consumption for m in self.scenario.models.values()])
    }

