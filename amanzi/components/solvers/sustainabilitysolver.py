from .solver import Solver

class SustainabilitySolver(Solver):

  def solve(self, until=None):

    total_distribution = self.scenario.solvers['quantity'].summary()['total_distribution'] * 1e6
    # sum energy consumption for each model
    for m in self.scenario.models.values():
      outputs = [o for o in m.output_parameters.values() if o.category == 'sustainability' and o.uom == 'gCO2-eq/m3' and not o.hidden(m.context)]

      # specific co2-eq emissions in gCO2-eq/m3 produced by the model
      m.sustainability.model_specific_emission = emission = sum([m.get_output(o.name) for o in outputs])
      # total co2-eq emissions per year in ton CO2-eq/y
      m.sustainability.total_emission = emission * m.quantity.outflow['product'] * 1e6 / 1e6 # total energy consumption per year
      # specific energy consumption in kWh/m3 produced by the treatment plant
      # total production in m3/y
      m.sustainability.specific_emission = 1e6 * m.sustainability.total_emission / total_distribution

      
  def summary(self):

    total_emission = sum([m.sustainability.total_emission for m in self.scenario.models.values()])
    total_specific_emission = sum([m.sustainability.specific_emission for m in self.scenario.models.values()])

    return {
      'model_specific_emission': {m.name: m.sustainability.model_specific_emission for m in self.scenario.models.values()},
      'specific_emissions': {m.name: m.sustainability.specific_emission for m in self.scenario.models.values()},
      'total_emissions': {m.name: m.sustainability.total_emission for m in self.scenario.models.values()},
      'total_emission': total_emission,
      'total_specific_emission': total_specific_emission,
      'metrics': [
        {'name': 'total_emission', 'value': total_emission, 'uom': 'ton CO2-eq/y'},
        {'name': 'total_specific_emission', 'value': total_specific_emission, 'uom': 'gCO2-eq/m3'},
      ]
    }

