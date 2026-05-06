from .model import Model
from .submodels.balance import Balance
from math import log
import numpy as np
from .tower.air_properties import Air

class Plate(Model, Balance):
    parametric_model = ['base','model', 'plate', 'aeration']
    def __init__(self, config, pp: dict = {}) -> None:
        super().__init__(config, pp)
        self.rq = float(self.parameters['RQ'])
        self.recirculation = float(self.parameters['recirculation'])
        self.efficiency = float(self.parameters['efficiency'])
        self.totalpressuredrop = 0 
        self.temp_g = 20
        self.g_density = Air(self.temp_g, 1.023e5).density()
        self.change_per_step = {}

    @staticmethod
    def blower_power(Qair,Tair, delta_p, efficiency, air_density):
        Pin = 101325 # Pa
        R = 8.31446 # J/(mol*K)
        kappa = 1.4
        Mair = 28.97e-3 # kg/mol
        Tair = Tair + 273.15 # C to K
        Pavg = Qair * air_density* R * Tair *(kappa/(kappa-1)) * (((Pin+delta_p)/Pin)**((kappa-1)/kappa)-1)/(efficiency*Mair)
        # conversion J to kWh
        Pavg = Pavg / 3600000
        return Pavg
    
    @property
    def deltaPtotal(self):
        return self.totalpressuredrop
    @property
    def context(self):
        ctx = super().context
        ctx['blower_power'] = self.blower_power
        ctx['Air_density'] = self.g_density
        return ctx
    
    def aerate(self, influent, RQ, recirculation):
        
        air_comps = {
            'O2(g)': 0.208,
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
            air = self.pp.add_gas(gas_comp,  pressure=1, volume=RQ, fixed_pressure=True, fixed_volume=False)
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


    def run_quality(self, type, total_inflow, solution):
        aerated, _ = self.aerate(solution, self.rq, self.recirculation)
        return aerated
    
    def design(self):
        effluent, effluent_gas = self.aerate(self.quality.influent.product, self.rq, self.recirculation)

        ph_data = []
        si_data = []

        ch4_data = []
        co2_data = []
        o2_data = []


        RQs = np.linspace(1, 50, 100)
        # sweep RQ
        for rq in RQs:
            eff, gas = self.aerate(self.quality.influent.product, rq, self.recirculation)
            ph_data.append({'x': rq, 'y': eff.pH})
            si_data.append({'x': rq, 'y': eff.si('Calcite')})

            ch4_data.append({'x': rq, 'y': eff.total('Mtg') * 16040})
            co2_data.append({'x': rq, 'y': eff.total('CO2', 'mg')})
            o2_data.append({'x': rq, 'y': eff.total('O2', 'mg') })

        return {
            'influent': {
                'pH': self.quality.influent.product.pH,
                'ch4': self.quality.influent.product.total('Mtg') * 16040,
                'n2': self.quality.influent.product.total('Ntg') * 28.0134,
                'co2': self.quality.influent.product.total('CO2', 'mg'),
                'h2s': self.quality.influent.product.total('H2S', 'mg'),
                'o2': self.quality.influent.product.total('O2', 'mg'),
            },
            'effluent': {
                'pH': self.quality.effluent.product.pH,
                'ch4': self.quality.effluent.product.total('Mtg') * 16040,
                'n2': self.quality.effluent.product.total('Ntg') * 28.0134,
                'co2': self.quality.effluent.product.total('CO2','mg'),
                'h2s': self.quality.effluent.product.total('H2S','mg'),
                'o2': self.quality.effluent.product.total('O2', 'mg'),
            },
            'gas': {
                'ch4': effluent_gas.dry_fractions['Mtg(g)'] * 100,
                'n2': effluent_gas.dry_fractions['Ntg(g)'] * 100,
                'co2': effluent_gas.dry_fractions['CO2(g)'] * 100,
                'o2': effluent_gas.dry_fractions['O2(g)'] * 100,
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