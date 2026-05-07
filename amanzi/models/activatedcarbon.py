from .model import Model
from .submodels.balance import Balance
import math
from .tower.compounds import Chemical
from .breakthrough import BreakthroughInput, select_breakthrough_solver

import warnings
warnings.simplefilter("ignore")
from .submodels.loss import Loss
# import os
# srt_dir = os.getcwd()
# import bisect
# import pandas as pd
import logging

# from .PSDM import PSDM
# from .PSDM import PSDM_functions


logging.basicConfig(level=logging.DEBUG)

class Activatedcarbon(Model, Loss):
    parametric_model = ['base','model','activatedcarbon', 'filtration']

    def __init__(self, config, pp: dict = {}) -> None:
        super().__init__(config, pp)
        self.configurations = config.get('configuration', {})


        config = config.get('configuration', {})
        config = config.get('parameters', {})

        self.loss = self.get_output('backwash_loss')
        self.sprayaeration = config.get('spray', False)


        self.packing_height = float(config.get('bed_height', 2.5))
        self.dimension = float(config.get('diameter', 2))
        self.packing_type = config.get('packing_type', 'NORA Supra 0.8')
        self.volumeflow = float(config.get('nominal_capacity', 100))
        self.packing_volume = self.packing_height * math.pi * (self.dimension/2)**2
        self.capacity = float(config.get('nominal_capacity', 100))
        self.compoundList = self.configurations.get('compound', {'x':0})
        self.advanced = config.get('advanced', False)
        self.fixed_replacement = config.get('fixed_replacement', True)
        self.renewal = int(config.get('replacement_interval', 1000))
        self.replacement_loading = float(config.get('replacement_loading', 0.5))
        self.filternumber = int(config.get('units', 1))
        self.apparent_density = float(config.get('apparent_density', 0.5))
        self.particle_density = float(config.get('particle_density', 0.5))
        self.particle_diameter = float(config.get('particle_diameter', 0.04))
        self.bed_porosity = float(config.get('bed_porosity', 0.4))
        self.particle_porosity = float(config.get('particle_porosity', 0.5))
        self.waste_solution = None
        self.OMV_capacity = config.get('OMV_capacity',{})
        


    @property
    def backwash_programme(self):

        programme = self.parameters.get('backwash_programme', [])
        return programme
    @property
    def compound_removal_rates(self):
        removal_rates={}
        for PFAS in self.scenario['metaData']['customMicroComponents']['PFAS']:
            removal_rates[PFAS['name']] = PFAS['removalAKF']
        for Other in self.scenario['metaData']['customMicroComponents']['Other']:
            removal_rates[Other['name']] = Other['removalAKF']
        return removal_rates

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
        
    @staticmethod
    def kozeny_carman(p, v, d):
        d /= 1e3 # convert to mm
        v /= 3600 # convert to m/s
        return 180 * 1.3e-6 / 9.81 * (1-p)**2 / p**3 * v/d**2


    @property
    def context(self):
        ctx = super().context
        ctx['_backwash_duration'] = self._backwash_duration
        ctx['_backwash_volume'] = self._backwash_volume
        ctx['_backwash_max_rate'] = self._backwash_max_rate
        ctx['kozeny_carman'] = self.kozeny_carman
        ctx['aerated'] = self.aerated if hasattr(self, 'aerated') else self.quality.influent.product

        return ctx
    
    
    
    def wastestream_calculation(self, solution):
        return solution
    # def calculate_efficiency(self, compound, solution): 
    #     #Freundlich Isotherm parameters
    #     #Diffusion koefficient for film diffusion from water to GAC from compound file'
        
    #     t_in_seconds = 134776000
    #     resolution = 100
    #     volume_flow_rate = self.volumeflow/3600 #m³/s
    #     height = self.packing_height            #m
    #     crosssection = math.pi * (self.dimension/2)**2  #m²
    #     filmdiffusion =  Chemical(20,20).properties()['CO2']['Diff_water']*1000#m²/s should be m/s thats why *1000
    #     freundlich_k = self.freundlich_k
    #     freundlich_n = self.freundlich_n
                
    #     cadet_model = CADETMODEL()
    #     model=cadet_model.create_and_run_model(t_in_seconds, [solution.total('CO2', 'mol')*1000],  resolution, volume_flow_rate, height, crosssection, filmdiffusion,freundlich_k, freundlich_n)

    #     efficiency= 1-(model.root.output.solution.unit_001.solution_outlet[3][0]/solution.total('CO2', 'mol'))

    #     return efficiency
    
    # def PSDMcalculation(self, solution):
    #     os.chdir(srt_dir)
         
    #     water_type = 'Organic Free'
    #     chem_type = 'halogenated alkenes'
    #     nr=4 # number of radial collocation points (int, default = 14)
    #     nz=8 # number of axial collocation points (int, default = 19)
    #     ne=2  # number of finite elements

    #     particlePorosity=self.particle_porosity
    #     particleRadius=self.particle_diameter*0.5/10 # from mm -> cm
    #     apparentDensity= self.apparent_density/1000 #kg/m³ -> g/cm³
    #     particleDensity= self.particle_density/1000 #kg/m³ -> g/cm³
    #     length= self.packing_height*100 #from m -> cm
    #     diameter= self.dimension*100 #from m ->cm
    #     bedporosity=self.bed_porosity
    #     poreSurfaceRatio= 5 # pore to surface diffusion ratio
    #     tortuosity=1 # tortuosity factor

    #     massGAC=bedporosity*apparentDensity*length*math.pi*(diameter/2)**2
    #     flowrate= self.capacity*1e6/60 #from m³/h -> ml/min
    #     volumebed= length*math.pi*(diameter/2)**2 #cm³
    #     volumeflow = flowrate*60*24 # ml/day
    #     EBCT=volumebed/flowrate 
    #     #print(EBCT)


    #     data = {    'name': ['carbonID', 'rad',       'epor', 'psdfr', 'rhop', 'rhof', 'L', 'wt', 'flrt', 'diam', 'tortu', 'influentID', 'effluentID'],	
    #                 'value': ['F400', particleRadius, particlePorosity,  poreSurfaceRatio,  apparentDensity,  particleDensity,  length, massGAC, flowrate,  diameter,    tortuosity, 'influent', 'effluent'],
    #             } 
    #     #default time is days

    #     # data = { 'name': ['carbonID', 'rad', 'epor',    'psdfr', 'rhop', 'rhof', 'L',   'wt', '         flrt',   'diam',   'tortu', 'influentID', 'effluentID', 'units', 'time','mass_mul' ,'t_mult', 'flow_mult', 'flow_type'],	
    #     # 'value':        ['F400',    0.0513,    '0.641',    '5', '0.803', '0.62', '180', '8500000', '1892705.892',  '366',   '1', 'influent', 'effluent',        'ug', 'days',   '1.0',      '1440',     '0.001',        'ml'],
    #     # 'units':        ['',        'cm',       '',         '',  'g/ml', 'g/ml', 'm',       'kg',       'gpm',      'm',     '',    '',         '',             '',     '',     '',     '', '', ''],	} 
    #     df = pd.DataFrame(data, index=data['name'])
    #     df.name=data['value'][0]
    #     # Setting of influent water profile, with compound concentrations in ng/l as default
    #     data_conc={}
    #     PFASproperties = {}
    #     for compound in self.quality.influent.product.extraneous['PFAS']:
    #         data_conc['influent', compound] = [self.quality.influent.product.extraneous['PFAS'][compound], self.quality.influent.product.extraneous['PFAS'][compound]]
    #         data_conc['F400', compound] = [0, 0]

    #         PFASproperties[compound] = [float(self.compoundList[compound][0]),float(self.compoundList[compound][1]),float(self.compoundList[compound][2])]

    #     logging.warning(f"PFAS properties: {PFASproperties}")
    #     #index = pd.MultiIndex.from_tuples([(0, 'influent'), (1000, 'F400')], names=['time', 'carbonID'])
    #     index = pd.Index([0, self.renewal*2], name='time')
    #     df_conc = pd.DataFrame(data_conc, index=index)
    #     df_conc.columns = pd.MultiIndex.from_tuples([(col[0], col[1]) for col in df_conc.columns], names=['type', 'compound'])
    #     #df_conc.columns.levels[0]='compound'

    #     index = ['K', '1/n', 'q'] # Freundlich parameters and loading
    #     # PSDM model assumes units of (ug/g)(L/ug)**(1/n) for K and 1/n (unitless) and 'q' is solid phase concentration (ug/g)
    #     # Numbers used fulfill the criteria
    #     df_kData = pd.DataFrame(PFASproperties, index=index)  # K, 1/n, q
    #     data_k = {
    #         'PFBS': [456.94, 0.411, 1], #PSDM PFAS Excel
    #         'PFPeS': [1521, 0.3521, 1],#PSDM PFAS Excel
    #         'PFHxS': [3832.9, 0.3136, 1], #PSDM PFAS Excel
    #         'PFHpS': [4588.9, 0.286, 1],#PSDM PFAS Excel
    #         'PFOS': [7222, 0.2525, 1],#PSDM PFAS Excel
    #         'PFHxS': [3840, 0.3134, 1],#PSDM PFAS Excel
    #         'PFDS': [0.1, 1, 1], #No values could be found
    #         'TFA': [2.3*(1000/(1000**0.343)), 0.343, 1], # 2.3 (mg/g)(l/mg)^1/n ; 1/n: 0.343 ; Source: Polypyrrole-Tailored Activated Carbon for Trifluoroacetate Removal from Groundwater
    #         'PFBA': [255, 0.4942, 1],#PSDM PFAS Excel
    #         'PFPeA': [1160, 0.4252, 1],#PSDM PFAS Excel
    #         'PFHxA': [4179, 0.3607, 1],#PSDM PFAS Excel
    #         'PFHpA': [498, 0.3144, 1],#PSDM PFAS Excel
    #         'PFOA': [1718, 0.2808, 1],#PSDM PFAS Excel
    #         'PFDA': [6371, 0.2415, 1],#PSDM PFAS Excel
    #         'PFUnDA': [14603, 0.2233, 1],#PSDM PFAS Excel
    #         'PFDoDA': [18106, 0.2076, 1],#PSDM PFAS Excel
    #         'PFTrDA': [25862, 0.1972, 1],#PSDM PFAS Excel
    #         'PFTeDA': [30582, 0.1858, 1] #PSDM PFAS Excel
    #     }
    #     # df_kData = pd.DataFrame(PFASproperties, index=index)

    #     #Reference for PFAS data ITRC PFAS Technical and regulartory Guidance document
    #     # MW , MolarVol ,BP(Boling Point),Density ,Solubility (unused), VaporPress (unused)
    #     index = ['MW', 'MolarVol', 'BP', 'Density', 'Solubility', 'VaporPress']
    #     data_properties = {
    #         'PFBS': [300.1, 163.9, 198, 1.83, 0,0], # PSDM PFAS Excel
    #         'PFPeS': [350, 190.2, 225, 1.84, 0, 0],#ITRC
    #         'PFHpS': [450, 238, 226,1.89, 0, 0], #ITRC
    #         'PFOS': [500, 237, 189, 1.8, 0, 0],  # PSDM PFAS Excel
    #         'PFHxS':  [400, 217, 239, 1.84, 0, 0], # PSDM PFAS Excel
    #         'PFDS':  [600, 310.9 , 255, 1.93, 0, 0], #ITRC
    #         'TFA':  [114, 129.7, 72, 1.489, 0, 0], #merckmillipore.com
    #         'PFBA':  [214, 129.72, 121, 1.65, 0, 0], # PSDM PFAS Excel
    #         'PFPeA':  [264, 154, 139, 1.71, 0, 0],#ITRC
    #         'PFHxA':  [314, 182, 157, 1.69, 0, 0],  # PSDM PFAS Excel
    #         'PFHpA': [364, 212.9, 175, 1.71, 0, 0],   # PSDM PFAS Excel
    #         'PFOA': [500, 217, 145, 1.84, 0,0],  # PSDM PFAS Excel
    #         'PFDA':  [514, 292, 184, 1.79, 0,0], # PSDM PFAS Excel
    #         'PFUnDA':  [564.1,304.8 , 238.4, 1.85, 0, 0], #ITRC
    #         'PFDoDA':  [614.1, 328.3, 249, 1.87, 0, 0],#ITRC
    #         'PFTrDA':  [664.1, 345.8, 261, 1.92, 0, 0],#ITRC
    #         'PFTeDA':  [714.1, 368, 270, 1.94, 0, 0],#ITRC
    #     }

    #     df_properties = pd.DataFrame(data_properties, index=index)
        
    #     #print(df_properties)

    #     #print(chem_data)
    #     #Simulation length is currently set to 2 times the replacement interval
    #     #Can be manually set with duration = x days

    #     column = PSDM.PSDM(df['value'], df_properties, df_conc,\
    #                             nz=nz,\
    #                             nr=nr,\
    #                             ne=ne,\
    #                             chem_type=chem_type,\
    #                             water_type=water_type,\
    #                             k_data=df_kData,\
    #                             solver='BDF'
    #                             )
            
    #     print('Starting example multicomponent simulation\n', 'This may take several minutes')
       
    #     all_results = column.run_psdm()
    #     #print(f"Results for PFUnDA : {all_results['PFUnDA'](all_results['PFUnDA'].x)}")
       
    #     for i in all_results.keys():
    #         idx = all_results[i].x

    #     return all_results

    def compound_removal_efficiency(self, group, name, metadata_item):
        configured = next(
            (item for item in self.scenario['metaData']['customMicroComponents'][group] if item['name'] == name),
            metadata_item
        )
   

        return configured['removalAKF']

    def simpleExtraneousRemoval(self, solution):  
        components = getattr(self, 'scenario', {}).get('metaData', {}).get('customMicroComponents', {})
        for i in components.get('PFAS', []):
            name= i['name']
            removal_efficiency = self.compound_removal_efficiency('PFAS', name, i)
            if name in solution.extraneous['PFAS']:
                solution.extraneous['PFAS'][name]=solution.extraneous['PFAS'][name]*(1-(float(removal_efficiency)/100))
        for i in components.get('Other', [])  :
            name= i['name']
            removal_efficiency = self.compound_removal_efficiency('Other', name, i)
            if name in solution.extraneous['Other']:
                solution.extraneous['Other'][name]=solution.extraneous['Other'][name]*(1-(float(removal_efficiency)/100))    
        return solution
    
    def breakthrough_input(self, solution):
        parameters = self.parameters
        components = getattr(self, 'scenario', {}).get('metaData', {}).get('customMicroComponents', {})
        volume = self.output_parameters['volume'].calculate(super().context)

        return BreakthroughInput(
            influent_pfas=solution.extraneous.get('PFAS', {}),
            metadata_pfas=components.get('PFAS', []),
            bed_volume_m3=volume,
            flow_m3_h=float(parameters.get('nominal_capacity', self.capacity)),
            apparent_density_kg_m3=float(parameters.get('apparent_density', self.apparent_density)),
            particle_density_kg_m3=float(parameters.get('particle_density', self.particle_density)),
            bed_porosity=float(parameters.get('bed_porosity', self.bed_porosity)),
            particle_diameter_mm=float(parameters.get('particle_diameter', self.particle_diameter)),
            replacement_interval_days=float(parameters.get('replacement_interval', self.renewal)),
            replacement_loading=float(parameters.get('replacement_loading', self.replacement_loading)),
            max_bed_volumes=parameters.get('breakthrough_bed_volumes'),
            points=int(parameters.get('breakthrough_points', 200)),
            axial_dispersion_m2_s=float(parameters.get('axial_dispersion', 1e-8)),
            mass_transfer_coefficient_s=float(parameters.get('mass_transfer_coefficient', 0.002)),
            particle_porosity=float(self.particle_porosity),
            column_length=float(self.packing_height),
        )

    def breakthrough_calculation(self, solution):
        solver_name = (self.parameters.get('breakthrough_solver') or 'psdm').lower()
        # Keep legacy option names working after switching to PSDM as default.
        if solver_name in {'fallback', 'default'}:
            solver_name = 'psdm'
        solver = select_breakthrough_solver(solver_name)
        return solver.run(self.breakthrough_input(solution))

    def should_run_breakthrough(self):
        return bool(self.parameters.get('run_breakthrough', False))

    def _bed_volumes_at_replacement(self):
        volume = self.output_parameters['volume'].calculate(super().context)
        flow_m3_h = float(self.parameters.get('nominal_capacity', self.capacity))
        replacement_interval_days = float(self.parameters.get('replacement_interval', self.renewal))
        return flow_m3_h * 24 * replacement_interval_days / max(volume, 1e-9)

    @staticmethod
    def _interpolate_curve(series, x_value):
        if not series:
            return 0
        if x_value <= series[0]['x']:
            return series[0]['y']
        for index in range(1, len(series)):
            left = series[index - 1]
            right = series[index]
            if x_value <= right['x']:
                span = right['x'] - left['x']
                if span == 0:
                    return right['y']
                fraction = (x_value - left['x']) / span
                return left['y'] + (right['y'] - left['y']) * fraction
        return series[-1]['y']

    def advancedExtraneousRemoval(self, solution, breakthrough_result=None):
        # if breakthrough_result is None and not self.should_run_breakthrough():
        #     return self.simpleExtraneousRemoval(solution)

        effluent = solution.deepcopy()
        result = breakthrough_result or self.breakthrough_calculation(solution)
        target_bed_volumes = self._bed_volumes_at_replacement()
        filter_count = max(int(self.parameters.get('units', self.filternumber)), 1)
        staggered = self.parameters.get('staggered_replacement', False)

        for compound, series in result.breakthrough.items():
            if compound not in effluent.extraneous.get('PFAS', {}):
                continue

            if staggered:
                ratios = [
                    self._interpolate_curve(series, target_bed_volumes * (index + 1) / filter_count)
                    for index in range(filter_count)
                ]
                ratio = sum(ratios) / len(ratios)
            else:
                ratio = self._interpolate_curve(series, target_bed_volumes)

            effluent.extraneous['PFAS'][compound] = solution.extraneous['PFAS'][compound] * ratio

        return effluent


    
    def spray_aeration(self, solution):
        solution = solution.deepcopy()


        co2_removal_efficiency = self.parameters['co2_removal_efficiency']
        ch4_removal_efficiency = self.parameters['ch4_removal_efficiency']
        o2_saturation = self.parameters['o2_saturation']

        # calculate oxygen saturation and CO2 removal
        air = self.pp.add_gas({f'O2(g)': 0.21, 'Ntg(g)': 0.79, 'CO2(g)': 0.043/100}, fixed_pressure=True, fixed_volume=False, volume=1000, pressure=1)

        saturated = solution.deepcopy().interact(air)

        max_o2 = saturated.total('O2')
        min_co2 = saturated.total('CO2')

        saturated.forget()

        o2_to_add = max(0, max_o2 * o2_saturation - solution.total('O2'))
        co2_to_remove = (solution.total('CO2')-min_co2) * co2_removal_efficiency
        ch4_to_remove = solution.total('Mtg') * ch4_removal_efficiency

        solution.change({ "O2": o2_to_add, "CO2": -co2_to_remove, "Mtg": -ch4_to_remove })

        # replace inert oxygen with free oxygen

        # effciency_co2 = self.calculate_efficiency('CO2', RQ , fall_height)
        # effciency_ch4 = self.calculate_efficiency('Mtg', RQ , fall_height)
        # effciency_O2 = self.calculate_efficiency('Oxg', RQ , fall_height)

        # max Oxygen saturation linear interpolation dependend on water temperature (5-20 Celsius)
        # mg/l to mmol/l
        return solution
    def unitcheck(self,solution):
        # ng/l is the default unit for PFAS influent and effluent
        components = getattr(self, 'scenario', {}).get('metaData', {}).get('customMicroComponents', {})
        for i in components.get('PFAS', []):
            if i['name'] in solution.extraneous['PFAS']:
                if i['unit'] == 'mg/l':
                    solution.extraneous['PFAS'][i['name']] = self.quality.influent.product.extraneous['PFAS'][i['name']]*1000000
                elif i['unit'] == 'μg/l':
                    solution.extraneous['PFAS'][i['name']] = self.quality.influent.product.extraneous['PFAS'][i['name']]*1000
        return solution


    def run_quality(self, type, total_inflow,solution):

        if(type == 'flush'):
            # add load to waste solution
            self.waste_solution = self.wastestream_calculation(solution.deepcopy())
            return self.waste_solution

        if (type == 'product'):
            solution = solution.deepcopy()
            if(self.sprayaeration):
                solution = self.spray_aeration(solution)
                self.aerated = solution.deepcopy()

            if self.advanced:
                effluent = self.advancedExtraneousRemoval(solution)
            else:
                effluent = self.simpleExtraneousRemoval(solution)

            return effluent
               
        return solution
    
    

    # def find_closest(self,nums, target):
    #     # Find the position where target should be inserted to maintain sorted order
    #     pos = bisect.bisect_left(nums, target)

    #     # If the target is the first element or exactly matches an element in the list
    #     if pos == 0:
    #         return 0
    #     if pos == len(nums):
    #         return len(nums) - 1

    #     # If target is not in nums, check the closest number (either before or after)
    #     before = nums[pos - 1]
    #     after = nums[pos]

    #     if after - target < target - before:
    #         return pos
    #     else:
    #         return pos - 1

    def design(self):
        influent = self.quality.influent.product.deepcopy()
        eff = {}
        peqPFAS={}
        sum4=[]
        sum20=[]
        peq2={}
        breakthrough_result = None
        volumeGAC = self.output_parameters['volume'].calculate(super().context) # m³
        if self.advanced and self.should_run_breakthrough() and influent.extraneous.get('PFAS'):
            breakthrough_result = self.breakthrough_calculation(influent)
            eff = breakthrough_result.breakthrough
            peqPFAS = breakthrough_result.peq_pfas
            sum4 = breakthrough_result.sum4_pfas
            sum20 = breakthrough_result.sum20_pfas
        # if self.compoundList != {} and self.compoundList.values() != [0] and self.advanced == True:
        #     PSDMcalculation = self.PSDMcalculation(self.quality.influent.product)
        #     dict_keys = list(PSDMcalculation.keys())
        #     for i in self.scenario['metaData']['customMicroComponents']['PFAS']:
        #         if i['name'] in self.quality.influent.product.extraneous['PFAS']:
        #             peq2[i['name']] = i['PEQ']
  
        #     eff = {}
        #     solEffluent=self.quality.effluent.product.extraneous['PFAS']
        #     peq1=[0] * len(PSDMcalculation[dict_keys[0]].x)
        #     sum4=[0] * len(PSDMcalculation[dict_keys[0]].x)
        #     sum20=[0] * len(PSDMcalculation[dict_keys[0]].x)
        #     length= self.packing_height*100 #cm
        #     diameter= self.dimension*100 #cm
        #     bedporosity=0.4
        #     massGAC=bedporosity* 0.5*length*math.pi*(diameter/2)**2
        #     flowrate= self.capacity*1e6/60 #ml/min
        #     volumebed= length*math.pi*(diameter/2)**2 #cm³
        #     volumeflow = flowrate*60*24 # ml/day
        #     bedvolumesPerDay=volumeflow/volumebed
        #     for key in PSDMcalculation:

        #         idx = PSDMcalculation[key].x
        #         #print(PSDMcalculation[key](idx))               
        #         eff[key] = [{'x': idx[k]*bedvolumesPerDay , 'y': PSDMcalculation[key](idx)[k]/self.quality.influent.product.extraneous['PFAS'][key] } for k in range(len(PSDMcalculation[key].x))]

        #         for k in range(len(PSDMcalculation[key].x)):
        #             if key == dict_keys[0]:
        #                 peq1[k] = PSDMcalculation[key](idx)[k]*peq2[key]
        #             else:
        #                 peq1[k] = PSDMcalculation[key](idx)[k]*peq2[key]+peq1[k]
        #             if key in ['PFOA', 'PFOS', 'PFHxS', 'PFHpS']:
        #                 sum4[k] = sum4[k]+PSDMcalculation[key](idx)[k]*peq2[key]
        #             if key in ['PFOA', 'PFOS', 'PFHxS', 'PFHpS', 'PFHxS', 'PFHpS', 'PFDS', 'PFBA', 'PFPeA', 'PFHxA', 'PFHpA', 'PFOA', 'PFDA', 'PFUnDA', 'PFDoDA', 'PFTrDA', 'PFTeDA']:
        #                 sum20[k] = sum20[k]+PSDMcalculation[key](idx)[k]*peq2[key]
        #     #print(eff['PFUnDA'])
        #     peqPFAS = [{'x': idx[k]*bedvolumesPerDay , 'y': peq1[k] } for k in range(len(PSDMcalculation[key].x))]
        #     sum4= [{'x': idx[k]*bedvolumesPerDay , 'y': sum4[k] } for k in range(len(PSDMcalculation[key].x))]
        #     sum20= [{'x': idx[k]*bedvolumesPerDay , 'y': sum20[k] } for k in range(len(PSDMcalculation[key].x))]


        if(self.sprayaeration):
            influent = self.spray_aeration(influent.deepcopy())
            self.aerated = influent.deepcopy()
        if self.advanced:
            effluent = self.advancedExtraneousRemoval(influent.deepcopy(), breakthrough_result)
        else:
            effluent = self.simpleExtraneousRemoval(influent.deepcopy())


        #print(eff) 
        #Assuming the same adsorption capacity for all compounds in mg/m³ GAC
        #Average adsorption capacity for PFAS 
        volumeGAC =self.output_parameters['volume'].calculate(super().context) # m³
        adsorption_capacities = {}
        for value in self.scenario['metaData']['customMicroComponents']['PFAS']:
            adsorption_capacities[value['name']] = value['adsorptionCapacity_simple']
        average_adsorption_capacity = sum(adsorption_capacities.values())/max(len(adsorption_capacities), 1)*1000 #mg/kgGAC
        capacityFactor = self.apparent_density*average_adsorption_capacity #mg/m³GAC
        if 'PFAS' in self.quality.influent.product.extraneous and self.quality.influent.product.extraneous['PFAS'] != {}:
            sumPFASinGAC = (sum(self.quality.influent.product.extraneous['PFAS'].values())-sum(self.quality.effluent.product.extraneous['PFAS'].values()))*1e-6 #sum of all PFAS in mg/l
        else:
            sumPFASinGAC = 0.00000000001
        if 'Other' in self.quality.influent.product.extraneous and self.quality.influent.product.extraneous['Other'] != {}:
            sumOtherinGAC = (sum(self.quality.influent.product.extraneous['Other'].values())-sum(self.quality.effluent.product.extraneous['Other'].values()))*1e-6 #sum of all Other in mg/l
        else:
            sumOtherinGAC = 0.00000000001
        # volumeGAC: int | float = (self.packing_height* math.pi * (self.dimension/2)**2) 
        if self.fixed_replacement:
            regeneration = self.renewal
        else:
            regeneration = (volumeGAC *capacityFactor / ((sumPFASinGAC+sumOtherinGAC)*self.capacity*1000))*self.replacement_loading/24 #capcity divided by amount of organics adsorbed per day

        color_removal_efficiency = 0
        toc_removal_efficiency = 0

        for i in self.scenario['metaData']['customMicroComponents']['Other']:
            if i['name'] == 'Color':
                color_removal_efficiency = i['removalAKF']
            if i['name'] == 'TOC':
                toc_removal_efficiency = i['removalAKF']

        if 'Color' in self.quality.influent.product.extraneous and self.quality.influent.product.extraneous['Color'] != {}:
            color_removal_efficiency = self.quality.influent.product.extraneous['Color']*color_removal_efficiency
        if 'TOC' in self.quality.influent.product.extraneous and self.quality.influent.product.extraneous['TOC'] != {}:
            toc_removal_efficiency = self.quality.influent.product.extraneous['TOC']*toc_removal_efficiency

        influentOMV = {}
        influentOMV['Color'] = self.quality.influent.product.extraneous['Color']
        influentOMV['TOC'] = self.quality.influent.product.extraneous['TOC']
        for key in self.quality.influent.product.extraneous['PFAS']:
            influentOMV[key] = self.quality.influent.product.extraneous['PFAS'][key]

        effluentOMV = {}
        effluentOMV['Color'] = self.quality.effluent.product.extraneous['Color']*color_removal_efficiency
        effluentOMV['TOC'] = self.quality.effluent.product.extraneous['TOC']*toc_removal_efficiency
        for key in self.quality.effluent.product.extraneous['PFAS']:
            effluentOMV[key] = self.quality.effluent.product.extraneous['PFAS'][key]

        return {
            'influent': influentOMV
            ,
            'effluent': effluentOMV
            ,
            'model': {
                'regeneration': regeneration,
                'EBCT' : self.packing_volume/(self.volumeflow/60),
                'peqPFAS':peqPFAS,
                'sum4PFAS': sum4,
                'sum20PFAS': sum20,
                'Volume': self.packing_volume,
                'breakthrough': eff,
                'PFAS': self.quality.influent.product.extraneous['PFAS']
            }
        }
    @property
    def emitter_solutions(self):
        return {'waste': self.waste_solution}