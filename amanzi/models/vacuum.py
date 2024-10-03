from .model import Model
from .submodels.balance import Balance
import numpy as np
from math import log

class Vacuum(Model, Balance):
    parametric_model = ['base', 'model', 'vacuum', 'gasprocessing']
    def __init__(self, config, pp: dict = {}) -> None:
        super().__init__(config, pp)
        config = config.get('configuration', {})
        config = config.get('parameters', {})
        self.pressure = float(config.get('vacuum_pressure', 0.2))

        self.gas = None

    def degass(self, solution, pressure):
      # make gas phase
      gas_phase = self.pp.add_gas({'Ntg(g)':0, 'Mtg(g)': 0, 'CO2(g)':0, 'Oxg(g)': 0, 'H2O(g)': 0, 'H2Sg(g)': 0}, pressure = pressure, fixed_pressure = True, fixed_volume = False)

      # degassed
      degassed = solution.copy()

      degassed.interact(gas_phase)

      return degassed, gas_phase

    def run_quality(self, type, total_inflow, solution):
      degassed, self.gas = self.degass(solution, self.pressure)
      return degassed

    @property
    def context(self):
       ctx = super().context
       ctx['_gas'] = self.gas

       return ctx

    def design(self):
      effluent, effluent_gas = self.degass(self.quality.influent.product, self.pressure)

      pressures = np.linspace(0.03, 0.5, 100)

      ph_data = []
      si_data = []
      ch4_data = []
      n2_data = []
      co2_data = []
      h2s_data = []
      volumes = []
      normal_volumes = []

      dry_ch4 = []
      dry_n2 = []
      dry_co2 = []

      wet_ch4 = []
      wet_n2 = []
      wet_co2 = []
      wet_h2o = []

      for p in pressures:
        eff, gas = self.degass(self.quality.influent.product, p)

        si_data.append({'x': p, 'y': eff.si('Calcite')})
        ph_data.append({'x': p, 'y': eff.pH})
        ch4_data.append({'x': p, 'y': eff.total('Mtg') * 16})
        n2_data.append({'x': p, 'y': eff.total('Ntg') * 28})
        co2_data.append({'x': p, 'y': eff.total('CO2','mg')})
        h2s_data.append({'x': p, 'y': eff.total('H2S','mg')})

        normal_volumes.append({'x': p, 'y': gas.volume*p})
        volumes.append({'x': p, 'y': gas.volume})

        dry_ch4.append({'x': p, 'y': gas.dry_fractions['Mtg(g)'] * 100})
        dry_n2.append({'x': p, 'y': gas.dry_fractions['Ntg(g)'] * 100})
        dry_co2.append({'x': p, 'y': gas.dry_fractions['CO2(g)'] * 100})

        wet_ch4.append({'x': p, 'y': gas.fractions['Mtg(g)'] * 100})
        wet_n2.append({'x': p, 'y': gas.fractions['Ntg(g)'] * 100})
        wet_co2.append({'x': p, 'y': gas.fractions['CO2(g)'] * 100})
        wet_h2o.append({'x': p, 'y': gas.fractions['H2O(g)'] * 100})

      return {
         'influent': {
            'pH': self.quality.influent.product.pH,
            'ch4': self.quality.influent.product.total('Mtg') * 16.04e3,
            'n2': self.quality.influent.product.total('Ntg') * 28.0134,
            'co2': self.quality.influent.product.total('CO2','mg'),
            'h2s': self.quality.influent.product.total('H2S','mg'),
         },
         'effluent': {
            'pH': effluent.pH,
            'ch4': effluent.total('Mtg') * 16.04e3,
            'n2': effluent.total('Ntg') * 28,
            'co2': effluent.total('CO2','mg'),
            'h2s': effluent.total('H2S','mg'),
         },
         'gas_dry': {
            'ch4': effluent_gas.dry_fractions['Mtg(g)'] * 100,
            'n2': effluent_gas.dry_fractions['Ntg(g)'] * 100,
            'co2': effluent_gas.dry_fractions['CO2(g)'] * 100,
            'h2s': effluent_gas.dry_fractions['H2Sg(g)'] * 100,
            'volume': effluent_gas.volume,
            'normal_volume': effluent_gas.volume * self.pressure,
         },
        'charts': {
           'pH': ph_data,
           'SI': si_data, 
           'ch4': ch4_data,
           'n2': n2_data,
            'co2': co2_data,
            'h2s': h2s_data,
            'normal_volume': normal_volumes,
            'volume': volumes,
            'dry_ch4': dry_ch4,
            'dry_n2': dry_n2,
            'dry_co2': dry_co2,
            'wet_ch4': wet_ch4,
            'wet_n2': wet_n2,
            'wet_co2': wet_co2,
            'wet_h2o': wet_h2o,
        }

      }
