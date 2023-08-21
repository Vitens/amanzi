from .model import Model
from .submodels.balance import Balance
from math import log
import numpy as np

class Plate(Model, Balance):
    def __init__(self, config, pp: dict = {}) -> None:
        super().__init__(config, pp)
        self.configuration = config.get('configuration', {})

        self.rq = float(self.configuration.get('rq', 10))
        self.recirculation = float(self.configuration.get('recirculation', 0)) / 100
        self.efficiency = float(self.configuration.get('efficiency', 10)) / 100

        self.change_per_step = {}
    
    def aerate(self, influent, RQ, recirculation):

        air_comps = {
            'Oxg(g)': 0.208,
            'Ntg(g)': 0.7916,
            'CO2(g)': 0.0004,
            'Mtg(g)': 0,
            'H2Sg(g)': 0,
            'H2O(g)': 0,
        }

        gas_comp = air_comps.copy()

        iterations = 1 if recirculation == 0 else 3

        RQ *= self.efficiency

        for _ in range(iterations):
            # copy influent
            inf = influent.copy()
            # process air
            air = self.pp.add_gas(gas_comp, volume=RQ, pressure=1, fixed_pressure=True, fixed_volume=False)
            # interact
            inf.interact(air)

            # amount of off gas
            off_gas = air.fractions
            off_gas_volume = air.volume
        
            # amount of fresh gas
            fresh_gas_volume = RQ - off_gas_volume * recirculation
            fresh_gas_fraction = fresh_gas_volume / RQ
            off_gas_fraction = 1 - fresh_gas_fraction

            # process air quality
            for comp in gas_comp:
                gas_comp[comp] = (air_comps[comp] * fresh_gas_fraction + off_gas[comp] * off_gas_fraction)
        
        return inf, air


    def run_model(self, type, total_inflow, solution):
        aerated, _ = self.aerate(solution, self.rq, self.recirculation)
        return aerated
    
    def design(self):
        print('plate', self.influent.number)
        effluent, effluent_gas = self.aerate(self.influent, self.rq, self.recirculation)

        ph_data = []
        si_data = []

        ch4_data = []
        co2_data = []
        o2_data = []


        RQs = np.linspace(1, 50, 100)
        # sweep RQ
        for rq in RQs:
            eff, gas = self.aerate(self.influent, rq, self.recirculation)
            ph_data.append({'x': rq, 'y': eff.pH})
            si_data.append({'x': rq, 'y': eff.si('Calcite')})

            ch4_data.append({'x': rq, 'y': eff.total('Mtg') * 16040})
            co2_data.append({'x': rq, 'y': eff.total('CO2', 'mg')})
            o2_data.append({'x': rq, 'y': eff.total('Oxg') * 32})

        return {
            'influent': {
                'pH': self.influent.pH,
                'ch4': self.influent.total('Mtg') * 16040,
                'n2': self.influent.total('Ntg') * 28.0134,
                'co2': self.influent.total('CO2', 'mg'),
                'h2s': self.influent.total('H2S', 'mg'),
                'o2': self.influent.total('Oxg') * 32,
            },
            'effluent': {
                'pH': effluent.pH,
                'ch4': effluent.total('Mtg') * 16040,
                'n2': effluent.total('Ntg') * 28.0134,
                'co2': effluent.total('CO2','mg'),
                'h2s': effluent.total('H2S','mg'),
                'o2': effluent.total('Oxg') * 32,
            },
            'gas': {
                'ch4': effluent_gas.dry_fractions['Mtg(g)'] * 100,
                'n2': effluent_gas.dry_fractions['Ntg(g)'] * 100,
                'co2': effluent_gas.dry_fractions['CO2(g)'] * 100,
                'o2': effluent_gas.dry_fractions['Oxg(g)'] * 100,
                'h2s': effluent_gas.dry_fractions['H2Sg(g)'] * 100,
                'volume': effluent_gas.volume / self.efficiency,
            },
            'charts': {
                'pH': ph_data,
                'SI': si_data,
                'ch4': ch4_data,
                'co2': co2_data,
                'o2': o2_data,
            }

        }