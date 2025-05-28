from pprint import pprint as pprint
from .model import Model
from .submodels.loss import Loss
from .tower.compounds import Chemical
import math
import numpy as np
from .tower.air_properties import Air
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class Sandfiltration(Model, Loss):
    parametric_model = ['base', 'model', 'filtration','sprayaerator']

    def __init__(self, config, pp):
        super().__init__(config, pp)

        config = config.get('configuration', {})
        config = config.get('parameters', {})

        self.loss = self.get_output('backwash_loss')
        self.load = 0
        self.waste_solution = None
        self.sprayaeration = config.get('spray', False)
        # self.sauter = float(self.parameters['sauter_diameter'])
        self.fall_height = float(self.parameters['fall_height_to_media'])
        self.configuration = config.get('configuration', {})
        self.compound = self.configuration.get('model_component', 'CO2')
        self.removed_iron = 0
        self.waste_iron = 0

        self.RQ = float(self.parameters['rq'])

    def oxidize(self, solution, from_element, to_element, oxygen_consumption, efficiency=1):
        solution = solution.copy()
        to_exchange = solution.total(from_element) * 0.999999 # prevent negative concentrations
        oxygen_available = solution.total("O2") # free oxygen

        to_exchange = min(to_exchange, oxygen_available / oxygen_consumption)
        to_exchange = to_exchange * efficiency

        # print(f"Oxidizing {from_element} to {to_element} with {to_exchange} oxygen")
        solution.change({from_element: -to_exchange, to_element: to_exchange})

        return solution
    
    @property
    def backwash_programme(self):
        config = self.config.get('configuration', {})
        programme = config.get('backwash_programme', [])
        return programme
    
    @property
    def _backwash_duration(self):
        return sum([p['time'] for p in self.backwash_programme]) / 60

    @property
    def _backwash_volume(self):
        surface = self.output_parameters['surface_area'].calculate(super().context)
        return sum([p['water'] * surface * p['time']/3600 for p in self.backwash_programme])

    @property
    def _backwash_max_rate(self):
        return max([p['water'] for p in self.backwash_programme] + [0])
    @property
    def airDensity(self):
        return Air(float(self.parameters['ambient_temperature']), 1.023e5).density()
        
    @staticmethod
    def kozeny_carman(p, v, d):
        d /= 1e3 # convert to mm
        v /= 3600 # convert to m/s
        return 180 * 1.3e-6 / 9.81 * (1-p)**2 / p**3 * v/d**2
    
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
    @staticmethod
    def backwash_bed_expansion(particle_size, max_rate):
        # Formula has a high sensitivity for viscosity --> temperature influence that is not implemented yet
        backwashvelocity = max_rate / 3600 # m/s
        particle_size = particle_size/1000 # convert to m
        expansion_table = []
        viscosity = 1.1375e-3 # Pa.s at 15 Celsius
        filtertowater_density = 2.6
        Filterporosity = 0.38
        for i in range(0,31):
            ExpandedFilterporosity = (Filterporosity+ i/100)/(1+i/100)
            velocity = (9.81*(filtertowater_density-1)*(ExpandedFilterporosity**3)*(particle_size**1.8)/(((1-ExpandedFilterporosity)**0.8)*(viscosity**0.8)*130))**(1/1.2) 
            expansion_table.append(velocity*100)
        #interpolate to find the expansion at the backwash velocity
        return np.interp(backwashvelocity, expansion_table, range(0,31))/100

    @staticmethod
    def backwash_headloss(particle_size, max_rate , layer_height):
        backwashvelocity = max_rate / 3600 # m/s
        particle_size = particle_size/1000 # convert to m
        viscosity = 1.1375e-3 # Pa.s at 15 Celsius
        Filterporosity = 0.38
        headloss = 130 * layer_height * backwashvelocity**1.2 * (1-Filterporosity)**1.8 * viscosity**0.8 / (9.81*(Filterporosity**3)*particle_size**1.8)
        return headloss/1000 # convert to mH2O


    @property
    def context(self):
        ctx = super().context
        ctx['_backwash_duration'] = self._backwash_duration
        ctx['_backwash_volume'] = self._backwash_volume
        ctx['_backwash_max_rate'] = self._backwash_max_rate
        ctx['kozeny_carman'] = self.kozeny_carman
        ctx['blower_power'] = self.blower_power
        ctx['Air_density'] = self.airDensity
        ctx['backwash_bed_expansion'] = self.backwash_bed_expansion
        ctx['backwash_headloss'] = self.backwash_headloss
        ctx['aerated'] = self.aerated if hasattr(self, 'aerated') else self.quality.influent.product

        return ctx

    def filtrate(self, solution):
        # suppress removal of elements if set to True
        fe_removal_efficiency = 1
        if self.parameters['suppress_iron_removal']:
            fe_removal_efficiency = self.parameters['iron_removal_efficiency']
        nh4_removal_efficiency = 1
        if self.parameters['suppress_ammonium_removal']:
            nh4_removal_efficiency = self.parameters['ammonium_removal_efficiency']
        mn_removal_efficiency = 1
        if self.parameters['suppress_manganese_removal']:
            mn_removal_efficiency = self.parameters['manganese_removal_efficiency']


        influent = solution.copy()
        # replace inert oxygen with free oxygen
        influent.change({ "O2": influent.total("Oxg"), "Oxg": -influent.total("Oxg")*0.99999})

        # oxidize methane
        after_ch4 = self.oxidize(influent, "Mtg", "CH4", 2)

        fe_oxidation= self.oxidize(after_ch4, "[Fe+2]", "Fe+2", 0.25, fe_removal_efficiency)
        after_fe = fe_oxidation.desaturate("Fe(OH)3(a)", 0)
        self.removed_iron = after_ch4.total('Fe', 'mg')-after_fe.total('Fe', 'mg')
        
        # oxidize h2
        after_h2s = self.oxidize(after_fe, "[S-2]", "S-2", 2)



        after_nh4 = self.oxidize(after_h2s, "[N-3]", "N-3", 2, nh4_removal_efficiency)
        after_no2 = self.oxidize(after_nh4, "[N+3]", "N+3", 2)
        after_mn = self.oxidize(after_no2, "[Mn+2]", "Mn+2", 0.5, mn_removal_efficiency).desaturate("Manganite", to_si=0)

        effluent = after_mn.copy()

        return effluent, [influent, after_ch4, after_fe, after_h2s, after_nh4, after_no2, after_mn]
    
    def calculate_efficiency(self,compound, RQ, fall_height):
        # polynominla fit of  TU Delft dresden Nozzle curve
        # Currently a workaround
        x = fall_height
        y = -0.4424*x**4 + 1.8483*x**3 - 2.9011*x**2 + 2.2391*x + 0.0255
        efficiency = y

        #d_sauter = 0.00025 # m sauter diameter function of presure/ nozzle/ volume flow.
        # A = math.pi*(d_sauter**2)/4
        # V = math.pi*(d_sauter**3)/6
        # g=9.81
        # c_v= 0.95 # nozzle sprecific parameter
        # alpha = 45 # angle of the nozzle outflow
        # t = 2*c_v * math.sin(alpha)*np.sqrt(4*fall_height/g)
        # t =np.sqrt(2*fall_height/g) ## exposure time, simple     
        # comp=Chemical(self.quality.influent.product.temperature,20)
        # D_comp= comp.properties()[compound]['Diff_water']#diffusion coefficient
        # print(f'Diffusion coefficient for {compound}: {D_comp}')
        # k2=2*(A/V)*np.sqrt(D_comp*t/(math.pi)) #gas transfer coefficient
        # efficiency= 1-np.exp(-k2)

        return efficiency

    def wastestream_calculation(self, solution):
        if self.parameters['backwash_control'] == 'volume':
            captured_iron = self.removed_iron  * self.parameters['runvolume']/1000
        else:
            captured_iron = self.removed_iron * self.parameters['nominal_capacity'] *self.parameters['runtime']/1000
        self.waste_iron = captured_iron/self._backwash_volume *1000
        solution = solution.copy()
        solution.change({'Fe': self.waste_iron}, units='mg')
        return solution
    
    def spray_aeration(self, solution, compound, RQ, fall_height):
        solution = solution.copy()

        # replace inert oxygen with free oxygen
        # solution.change({ "O2": solution.total("Oxg"), "Oxg": -solution.total("Oxg")*0.99999})

        effciency_co2 = self.calculate_efficiency('CO2', RQ , fall_height)
        effciency_ch4 = self.calculate_efficiency('Mtg', RQ , fall_height)
        effciency_O2 = self.calculate_efficiency('Oxg', RQ , fall_height)

        # max Oxygen saturation linear interpolation dependend on water temperature (5-20 Celsius)
        # mg/l to mmol/l
        O2_max = (-0.2366*self.quality.influent.product.temperature + 13.801) /32
        o2_in = self.quality.influent.product.total("O2", "mmol")
        O2_change = abs((O2_max-o2_in)*effciency_O2)
        solution.remove_fraction('CO2', effciency_co2)
        solution.remove_fraction('Mtg', effciency_ch4)
        solution.add('O2',O2_change , 'mmol')
        return solution

    def run_quality(self, type, total_inflow, solution):

        if(type == 'flush'):
            # add load to waste solution
            self.waste_solution = self.wastestream_calculation(solution.copy())
            return self.waste_solution
        
        if(type == 'product'):
            # influent
            solution = solution.copy()
            print(f"Solution before spray in mmol: {solution.total('O2', 'mmol')}")
            logging.debug(f"Solution before spray in mg: {solution.total('O2', 'mg')}")

            if(self.sprayaeration):
                solution = self.spray_aeration(solution, self.compound, self.RQ, self.fall_height)
                self.aerated = solution.copy()

            effluent, _ = self.filtrate(solution)

            return effluent
        return solution


    def design(self):
        values = {
            'pH': lambda s: s.pH,
            'O2': lambda s: s.total("O2", 'mg') ,
            'CO2': lambda s: s.total("CO2", 'mg'),
            'HCO3': lambda s: s.total("HCO3", 'mg'),
            'CH4': lambda s: s.total("Mtg") * 16e3,
            'Fe': lambda s: s.total("Fe", 'mg'),
            'NH4': lambda s: s.total("[N-3]") * 18,
            'NO2': lambda s: s.total("[N+3]") * 46,
            'NO3': lambda s: s.total("NO3", 'mg'),
            'Mn': lambda s: s.total("Mn", 'mg'),
        }
        results = {}

        if(self.sprayaeration):
            solution = self.spray_aeration(self.quality.influent.product, self.compound, self.RQ, self.fall_height)
            labels = ["spray", "methane_oxidation", "iron_removal", "h2s_oxidation", "nitrification", "denitrification", "manganese_removal"]
            step_results = {}
            for n, v in values.items():
                step_results[n] = v(self.quality.influent.product.copy())
            results["influent"]= step_results
            
        else:
            labels = ["influent", "methane_oxidation", "iron_removal", "h2s_oxidation", "nitrification", "denitrification", "manganese_removal"]
            solution = self.quality.influent.product.copy()

        effluent, steps = self.filtrate(solution)

        for i, step in enumerate(steps):

            step_results = {}

            for n, v in values.items():
                step_results[n] = v(step)
            
            results[labels[i]] = step_results

        return {
            'steps': labels,
            'values': results,
            'names': list(values.keys())
        }

    @property
    def emitter_solutions(self):
        return {'waste': self.waste_solution}