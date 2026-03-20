import numpy as np
from .model import Model
from .submodels.loss import Loss
from .tower.compounds import Chemical
from .submodels.balance import Balance
import math
from .tower.air_properties import Air
import time
import pandas as pd
# from openpyxl import load_workbook
# import xlsxwriter
import warnings
warnings.simplefilter("ignore")

class Marblefiltration(Model, Loss):
    parametric_model = ['base', 'model', 'marblefiltration', 'filtration', 'sprayaerator']
    def __init__(self, config, pp: dict = {}) -> None:
        super().__init__(config, pp)
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
        # self.create_arrays()

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

    @staticmethod
    def kozeny_carman(p, v, d):
        d /= 1e3 # convert to mm
        v /= 3600 # convert to m/s
        return 180 * 1.3e-6 / 9.81 * (1-p)**2 / p**3 * v/d**2
    
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

## Simulation approach from Gerit Jan, could not make it work atm.         
    def create_arrays(self):
        # Import various data including sieve analysis from excel file        
        self.number_of_heights = self.parameters['number_of_heights']
        self.number_of_fractions = self.parameters['number_of_fractions']
        self.number_of_runs = self.parameters['number_of_runs']
        
        F = self.number_of_runs + 1
        G = self.number_of_heights * 10  # number of heights X 2 for sufficient refill possibilities
        H = self.number_of_fractions

        # Initialize arrays for sieve analysis
        self.sieve_size = np.array([0.0]); self.sieve_size = np.repeat(self.sieve_size, 16)
        self.weight_per_sieve = np.array([0.0]); self.weight_per_sieve = np.repeat(self.weight_per_sieve, 16)
        self.total_weight_sieve_analysis = 0.0
        self.passage_percentage = np.array([0.0]); self.passage_percentage = np.repeat(self.passage_percentage, 16)

        # Arrays for bed layer calculations
        self.layer_mixture = []                                  # Mixture of water qualities from bed layer fractions
        self.bed_layer_height_sum_top0_ascending = np.zeros((F,G,H))            # Start counting at 0m at filter top (needed for iron removal, manganese removal, nitrification and marble dissolution)
        self.bed_layer_height_sum_top2_descending = np.zeros((F,G,H))          # Start counting at "2"m at filter top (needed for creating figures - bed height above and 0m at bottom)
        self.bed_layer_height_partial = np.zeros((F,G,H))                      # Thickness per bed height starting from filter bed top
        self.bed_layer_height_partial_temporary = np.zeros((F,G,H))            # Same as above but temporary for calculation
        self.height_counter = np.zeros((F))                                    # Counts number of bed heights, including refills
        self.filter_surface_portion_grain = np.zeros((F,G,H))                 # Size (0-1) of grain fraction portion in bed height  
        self.filter_surface_portion_grain_temporary = np.zeros((F,G,H))       # Same as above but temporary for calculation
        self.volume_grain_fraction = np.zeros((F,G,H))                        # Volume of grain fraction in respective bed height
        self.grain_count = np.zeros((F,G,H))                                  # Number of grains in a bed height
        self.grain_diameter = np.zeros((F+1,G,H))                       # Grain diameter
        self.grain_diameter_new_01 = np.zeros((F,G,H))                  # Grain diameter after CaCO3 dissolution
        self.bed_layer_after_refill = np.zeros((F,G,H))                 # New bed height if filter is refilled

        # Arrays for water quality parameters
        self.iron = np.zeros((F,G,H))                                   # Iron content influent bed layer
        self.iron_after_ox = np.zeros((F,G,H))                         # Iron content after oxidation
        self.iron_print = np.zeros((F,G,H))                            # Iron content after softening = print
        self.acid_iron = np.zeros((F,G,H))                             # Acid production from iron oxidation
        self.acid_manganese = np.zeros((F,G,H))                        # Acid production from manganese oxidation
        self.acid_ammonium = np.zeros((F,G,H))                         # Acid production from ammonium oxidation
        self.acid_total = np.zeros((F,G,H))                            # Sum of acid productions from iron, manganese and ammonium
        self.acid_per_height = np.zeros((F,G,H))                       # Acid production per (filter bed) height in mg/l
        self.acid_mol = np.zeros((F,G,H))                              # Acid production per (filter bed) height in mol/l
        self.manganese = np.zeros((F,G,H))                             # Manganese content influent bed layer
        self.manganese_after_ox = np.zeros((F,G,H))                    # Manganese content after oxidation
        self.manganese_print = np.zeros((F,G,H))                       # Manganese content after softening = print
        self.ammonium = np.zeros((F,G,H))                             # Ammonium content influent bed layer
        self.ammonium_after_ox = np.zeros((F,G,H))                    # Ammonium content after oxidation
        self.ammonium_print = np.zeros((F,G,H))                       # Ammonium content after softening = print
        self.pH = np.zeros((F,G,H))                                   # pH influent bed layer
        self.pH_after_ox = np.zeros((F,G,H))                         # pH after Fe, Mn and NH4 oxidation bed layer fraction
        self.pH_after_softening = np.zeros((F,G,H))                  # pH bicarbonate content
        self.pH_print = np.zeros((F,G,H))                            # pH after mixing waters from bed layer fractions of same bed layer
        self.CO2 = np.zeros((F,G,H))                                 # Carbon dioxide content raw water
        self.CO2_after_ox = np.zeros((F,G,H))                       # Carbon dioxide content after iron, manganese and ammonium oxidation
        self.CO2_after_softening = np.zeros((F,G,H))                # Carbon dioxide content after CaCO3 dissolution
        self.CO2_print = np.zeros((F,G,H))                          # Carbon dioxide content after mixing waters from bed layer fractions of same bed layer
        self.HCO3 = np.zeros((F,G,H))                               # Bicarbonate content incoming bed layer
        self.HCO3_after_ox = np.zeros((F,G,H))                      # Bicarbonate content after iron, manganese and ammonium oxidation
        self.HCO3_after_softening = np.zeros((F,G,H))               # Bicarbonate content after CaCO3 dissolution
        self.HCO3_print = np.zeros((F,G,H))                         # Bicarbonate content after mixing waters from bed layer fractions of same bed layer
        self.CO3 = np.zeros((F,G,H))                                # Carbonate content incoming bed layer
        self.CO3_after_ox = np.zeros((F,G,H))                       # Carbonate content after iron, manganese and ammonium oxidation
        self.CO3_after_softening = np.zeros((F,G,H))                # Carbonate content after CaCO3 dissolution
        self.TAC_print = np.zeros((F,G,H))                          # TAC content after mixing waters from bed layer fractions of same bed layer
        self.EC_after_mix = np.zeros((F,G,H))                       # Conductivity after mixing waters from bed layer fractions of same bed layer
        self.EC_print = np.zeros((F,G,H))                           # Same as above
        self.Ca = np.zeros((F,G,H))                                 # Calcium content incoming bed layer
        self.Ca_after_ox = np.zeros((F,G,H))                        # Calcium content after iron, manganese and ammonium oxidation
        self.Ca_after_softening = np.zeros((F,G,H))                 # Calcium content after CaCO3 dissolution
        self.Ca_print = np.zeros((F,G,H))                           # Calcium content after mixing waters from bed layer fractions of same bed layer
        self.Mg = np.zeros((F,G,H))                                 # Magnesium content incoming bed layer
        self.agr_CO2 = np.zeros((F,G,H))                     # Aggressive CO2 content incoming water
        self.agr_CO2_after_ox = np.zeros((F,G,H))            # Aggressive CO2 content after iron, manganese and ammonium oxidation
        self.agr_CO2_after_softening = np.zeros((F,G,H))     # Aggressive CO2 content after CaCO3 dissolution
        self.agr_CO2_after_mix = np.zeros((F,G,H))           # Aggressive CO2 content after mixing waters from bed layer fractions of same bed layer
        self.agr_CO2_print = np.zeros((F,G,H))               # Same as above
        self.SI_after_ox = np.zeros((F,G,H))                        # Saturation Index after iron, manganese and ammonium oxidation
        self.SI_after_softening = np.zeros((F,G,H))                 # Saturation Index after CaCO3 dissolution
        self.SI_after_mix = np.zeros((F,G,H))                       # Saturation Index after mixing waters from bed layer fractions of same bed layer
        self.SI_print = np.zeros((F,G,H))                           # Same as above
        self.SO4 = np.zeros((F,G,H))                                # Sulfate content incoming water
        self.Cl = np.zeros((F,G,H))                                 # Chloride content incoming water
        self.Cl_print = np.zeros((F,G,H))                           # Chloride content after mixing waters from bed layer fractions of same bed layer
        self.Na = np.zeros((F,G,H))                                 # Sodium content incoming water
        self.NO3 = np.zeros((F,G,H))                                # Nitrate content incoming water
        self.dissolved_CaCO3_print = np.zeros((F,G,H))              # Amount of dissolved CaCO3
        self.a_half_height_agr_CO2 = np.zeros((F,G,H))       # Half height = a*log(aggressive CO2) + b
        self.b_half_height_agr_CO2 = np.zeros((F,G,H))       # Half height = a*log(aggressive CO2) + b
        self.half_height_agr_CO2 = np.zeros((F,G,H))         # The half height aggressive CO2 in meters
        self.delta_dissolvable_CaCO3_by_agr_CO2 = np.zeros((F,G,H))  # Amount of CaCO3 that dissolves due to aggressive CO2
        self.agr_CO2_start = np.zeros((F,G,H))               # Aggressive CO2 content incoming water
        self.pH_equilibrium_after_softening = np.zeros((F,G,H))     # Equilibrium pH after CaCO3 dissolution
        self.tot = 0                                                # Initialize to zero
        self.acid_total[-1] = 0                                     # Initialize to zero
        
        self.runs = []
        self.height_after_run = []
        self.pH_after_run = []
        self.SI_after_run = []
        self.agrCO2_after_run = []
        self.number_of_heights_after_run = []        
    def sieve_analysis(self):
        count = 0
        total_weight_sieve_analysis = 0
        
        # workbook = xlrd.open_workbook(self.file_location)
        # sheet = workbook.sheet_by_index(0)
        number_of_sieves = self.parameters['number_of_sieves']

        sieve_size = np.array([0.0]); sieve_size = np.repeat(sieve_size, number_of_sieves+1)                    # define sieve size array
        weight_sieve_size = np.array([0.0]); weight_sieve_size = np.repeat(weight_sieve_size, number_of_sieves+1)  # define array for weight on sieves 
        passage_percentage = np.array([0.0]); passage_percentage = np.repeat(passage_percentage, number_of_sieves+1) # define array for percentage on sieves
        sizesFromExcel = [0.888,1.03,1.423,1.499,1.845,1.975,2.1725]
        weightsFromExcel = [5,5,40,10,30,5,5]


        for i in range(0, number_of_sieves):
            sieve_size[i+1] = sizesFromExcel[i]  # fill with data from Excel
            weight_sieve_size[i+1] = weightsFromExcel[i]  # fill with data from Excel
            
        # sheet = workbook.sheet_by_index(1)    
        self.bed_height_start = self.parameters['bed_height_start']
        self.number_of_heights_at_start = self.number_of_heights
        sieve_size[0] = sieve_size[1]*0.9           # define smallest sieve size (bin content belongs to smallest sieve size -10%)
        
        for i in range(0, number_of_sieves+1):                                
            if weight_sieve_size[i]>0:
                count += 1
                total_weight_sieve_analysis += weight_sieve_size[i]
        
        self.passage_percentage = np.array([0.0])  # create arrays
        self.passage_percentage = np.repeat(self.passage_percentage, number_of_sieves+1)
        self.sieve_size_print = np.array([0.0])
        self.sieve_size_print = np.repeat(self.sieve_size_print, number_of_sieves+1)

        for i in range(0, number_of_sieves+1):
            self.passage_percentage[i] = self.passage_percentage[i-1] + weight_sieve_size[i]/total_weight_sieve_analysis*100
            self.sieve_size_print[i] = sieve_size[i]

        # linear regression between sieve analysis points
        for i in range(0, number_of_sieves):
            a = np.array([0.0]); a = np.repeat(a, number_of_sieves)      # define array a-constants y = ax + b
            b = np.array([0.0]); b = np.repeat(b, number_of_sieves)      # define array b-constants y = ax + b

        for i in range(0, number_of_sieves):                            # set up equations for straight lines
            a[i] = (self.passage_percentage[i+1] - self.passage_percentage[i])/(self.sieve_size_print[i+1] - self.sieve_size_print[i])
            b[i] = -self.sieve_size_print[i]* a[i] + self.passage_percentage[i]
            
        for j in range(0, self.number_of_heights):
            for i in range(0, self.number_of_fractions):
                if i*100.0/self.number_of_fractions + 0.5*100.0/self.number_of_fractions < self.passage_percentage[1]:
                    self.grain_diameter[0,j,i] = ((i*100.0/self.number_of_fractions + 0.5*100.0/self.number_of_fractions)-b[0])/a[0]
                elif i*100.0/self.number_of_fractions + 0.5*100.0/self.number_of_fractions < self.passage_percentage[2]:
                    self.grain_diameter[0,j,i] = ((i*100.0/self.number_of_fractions + 0.5*100.0/self.number_of_fractions)-b[1])/a[1]
                elif i*100.0/self.number_of_fractions + 0.5*100.0/self.number_of_fractions < self.passage_percentage[3]:
                    self.grain_diameter[0,j,i] = ((i*100.0/self.number_of_fractions + 0.5*100.0/self.number_of_fractions)-b[2])/a[2]
                elif i*100.0/self.number_of_fractions + 0.5*100.0/self.number_of_fractions < self.passage_percentage[4]:
                    self.grain_diameter[0,j,i] = ((i*100.0/self.number_of_fractions + 0.5*100.0/self.number_of_fractions)-b[3])/a[3]
                elif i*100.0/self.number_of_fractions + 0.5*100.0/self.number_of_fractions < self.passage_percentage[5]:
                    self.grain_diameter[0,j,i] = ((i*100.0/self.number_of_fractions + 0.5*100.0/self.number_of_fractions)-b[4])/a[4]
                elif i*100.0/self.number_of_fractions + 0.5*100.0/self.number_of_fractions < self.passage_percentage[6]:
                    self.grain_diameter[0,j,i] = ((i*100.0/self.number_of_fractions + 0.5*100.0/self.number_of_fractions)-b[5])/a[5]
                elif i*100.0/self.number_of_fractions + 0.5*100.0/self.number_of_fractions < self.passage_percentage[7]:
                    self.grain_diameter[0,j,i] = ((i*100.0/self.number_of_fractions + 0.5*100.0/self.number_of_fractions)-b[6])/a[6]
                elif i*100.0/self.number_of_fractions + 0.5*100.0/self.number_of_fractions < self.passage_percentage[8]:
                    self.grain_diameter[0,j,i] = ((i*100.0/self.number_of_fractions + 0.5*100.0/self.number_of_fractions)-b[7])/a[7]
                elif i*100.0/self.number_of_fractions + 0.5*100.0/self.number_of_fractions < self.passage_percentage[9]:
                    self.grain_diameter[0,j,i] = ((i*100.0/self.number_of_fractions + 0.5*100.0/self.number_of_fractions)-b[8])/a[8]
                elif i*100.0/self.number_of_fractions + 0.5*100.0/self.number_of_fractions < self.passage_percentage[10]:
                    self.grain_diameter[0,j,i] = ((i*100.0/self.number_of_fractions + 0.5*100.0/self.number_of_fractions)-b[9])/a[9]
                elif i*100.0/self.number_of_fractions + 0.5*100.0/self.number_of_fractions < self.passage_percentage[11]:
                    self.grain_diameter[0,j,i] = ((i*100.0/self.number_of_fractions + 0.5*100.0/self.number_of_fractions)-b[10])/a[10]
                elif i*100.0/self.number_of_fractions + 0.5*100.0/self.number_of_fractions < self.passage_percentage[12]:
                    self.grain_diameter[0,j,i] = ((i*100.0/self.number_of_fractions + 0.5*100.0/self.number_of_fractions)-b[11])/a[11]
                elif i*100.0/self.number_of_fractions + 0.5*100.0/self.number_of_fractions < self.passage_percentage[13]:
                    self.grain_diameter[0,j,i] = ((i*100.0/self.number_of_fractions + 0.5*100.0/self.number_of_fractions)-b[12])/a[12]
                else:
                    q=1 # kind of stop ;-)
                    
        # Convert sieve analysis to grain size distribution over filter bed height. Both ascending and descending from filter bed top
        self.bed_layer_height_partial_start = self.bed_height_start/self.number_of_heights # calculate height step size
        self.bed_layer_height_sum_top2_descending[0,0,0] = self.bed_height_start        
         
        for j in range(1, self.number_of_heights):  # descending from bed height (e.g. 2 m) to 0 m
            self.bed_layer_height_sum_top2_descending[0,j,0] = self.bed_layer_height_sum_top2_descending[0,j-1,0] - self.bed_layer_height_partial_start
    
        self.bed_layer_height_sum_top0_ascending[0,0,0] = self.bed_layer_height_partial_start

        for j in range(1, self.number_of_heights):  # ascending from 0 m to bed height (e.g. 2 m)
            self.bed_layer_height_sum_top0_ascending[0,j,0] = self.bed_layer_height_sum_top0_ascending[0,j-1,0] + self.bed_layer_height_partial_start    
        
        for j in range(0, self.number_of_heights):
            for i in range(0, self.number_of_fractions):
                self.bed_layer_height_partial[0,j,i] = self.bed_layer_height_partial_start  # define bed layer heights
        
        for j in range(0, self.number_of_heights):
            for i in range(0, self.number_of_fractions):
                self.filter_surface_portion_grain[0,j,i] = 1.0/self.number_of_fractions # divide filter surface at each bed height into equal portions (number of fractions)
                self.grain_diameter[2,0,i] = self.grain_diameter[0,0,i] # needed when refilling filter; grain distribution of new layers    
    def oxidation(self):
        # import various data; including sieve analysis from excel file
        # workbook = xlrd.open_workbook(self.file_location)
        # sheet = workbook.sheet_by_index(2)
        
        # similar to sandfiltration maybe adjust 
        self.Fe_height_start = self.parameters['Fe_height_start']
        self.Fe_height_end = self.parameters['Fe_height_end']
        self.NH4_height_start = self.parameters['NH4_height_start']
        self.NH4_height_end = self.parameters['NH4_height_end']
        self.Mn_height_start = self.parameters['Mn_height_start']
        self.Mn_height_end = self.parameters['Mn_height_end']

        # sheet = workbook.sheet_by_index(3)
        # implement waterquality phreeqpython solution
        self.iron[0,0,0] = self.quality.influent.product.total('Fe')   
        self.manganese[0,0,0] = self.quality.influent.product.total('Mn') 
        self.ammonium[0,0,0] = self.quality.influent.product.total('NH4') 
    
                
        # iron, manganese and ammonium content cannot be 0 "simulation cannot divide by 0....."
        if self.iron[0,0,0] < 0.001:
            self.iron[0,0,0] = 0.0009
        if self.manganese[0,0,0] < 0.001:
            self.manganese[0,0,0] = 0.0009
        if self.ammonium[0,0,0] < 0.001:
            self.ammonium[0,0,0] = 0.0009
            
        # calculation RC-s log functions removal Fe, Mn and NH4; y = a*log(x) + b
        self.a_iron = -(math.log(self.iron[0,0,0]) - math.log(0.0009))/(self.Fe_height_end-self.Fe_height_start)
        self.a_manganese = -(math.log(self.manganese[0,0,0]) - math.log(0.0009))/(self.Mn_height_end-self.Mn_height_start)
        self.a_ammonium = -(math.log(self.ammonium[0,0,0]) - math.log(0.0009))/(self.NH4_height_end-self.NH4_height_start)
        self.b_iron = math.log(self.iron[0,0,0])
        self.b_manganese = math.log(self.manganese[0,0,0])
        self.b_ammonium = math.log(self.ammonium[0,0,0])                   
    def acidification(self):
        # import various data including sieve analysis from excel file
        # workbook = xlrd.open_workbook(self.file_location)
        
        # sheet = workbook.sheet_by_index(1)        
        self.filtration_velocity = self.parameters['filtration_rate']
        self.filter_surface = self.parameters['filter_surface']
        self.bed_height_start = self.parameters['bed_height_start']
        self.bed_height_refill = self.parameters['bed_height_refill']
                
        # sheet = workbook.sheet_by_index(2)
        self.correction_factor = 0.8 #sheet.cell_value(1,2)
        self.volume_filtered = self.parameters['volume_filtered']
        
        # sheet = workbook.sheet_by_index(0)
        self.porosity = self.parameters['marble_porosity']
        self.grain_shape = self.parameters['grain_shape']
        self.density = self.parameters['marble_density']
               
        for i in range(0, self.number_of_fractions):           # 1st layer fractions get raw water
            self.k = int(0)
            # sheet = workbook.sheet_by_index(3)
            self.Temp = self.quality.influent.temperature
            self.Ca[0,0,i] = self.quality.influent.product.total('Ca')
            self.Mg[0,0,i] = self.quality.influent.product.total('Mg')
            self.pH[0,0,i] = self.quality.influent.product.pH
            print("pH: ", self.pH[0,0,i], " CF: ", self.correction_factor, "Vf: ", self.filtration_velocity)
            self.HCO3[0,0,i] = self.quality.influent.product.total('HCO3')
            self.iron[0,0,i] = self.quality.influent.product.total('Fe')
            self.manganese[0,0,i] = self.quality.influent.product.total('Mn')
            self.ammonium[0,0,i] = self.quality.influent.product.total('NH4')
            self.SO4[0,0,i] = self.quality.influent.product.total('SO4')
            self.Cl[0,0,i] = self.quality.influent.product.total('Cl')
            self.Na[0,0,i] = self.quality.influent.product.total('Na')
            self.NO3[0,0,i] = self.quality.influent.product.total('NO3')
            self.charge = 2*self.Ca[0,0,i] + 2*self.Mg[0,0,i] + self.Na[0,0,i] - self.HCO3[0,0,i] - self.Cl[0,0,i] - 2*self.SO4[0,0,i] - self.NO3[0,0,i] # Fe and Mn not included due to direct oxidation which is not the case
            self.Na[0,0,i] += (-self.charge)                                                                      # balance ions using chloride
            self.iron_after_ox[0,-1,0] = self.iron[0,0,i]                                                       # for "loop"
            
            ## pHreeqc calculates pH from CO2. The lab calculates CO2 content from pH. Starting point is CO2 content. This can still change pH by a few 0.01s!
            # self.k1 = 10**(-356.3094-0.06091964*(273.15+self.Temp)+21834.37/(273.15+self.Temp)+
            #                126.8339*math.log10(273.15+self.Temp)-1684915/(273.15+self.Temp)**2)# k1 lime-carbon dioxide equilibrium at actual temperature
            # self.CO2[0,0,i]=(10**(-self.pH[0,0,i])*(self.HCO3[0,0,i])/(self.k1))  # calculation CO2 content from pH and HCO3
            self.CO2[0,0,i] = self.quality.influent.product.total('CO2')
                        
            ## input of raw water data in a solution called "raw"
            raw = self.pp.add_solution({'Ca':self.Ca[0,0,0],
                                   'Mg':self.Mg[0,0,0],
                                   'Alkalinity': str(self.HCO3[0,0,0]) +' as HCO3',
                                   'pH': self.pH[0,0,0],
                                   'SO4':self.SO4[0,0,0],
                                   'Cl':self.Cl[0,0,0],
                                   'Na':self.Na[0,0,0],
                                   'temp':self.Temp,
                                   'NO3':self.NO3[0,0,0]})
            
            self.inflow = raw.copy()                      # inflow = raw
        
        print (" "),print (raw.pH)
        # print ("calculated HCO3 =      ",raw.total('HCO3')*61.0," mg/l")
        # print ("Calculated pH =        ",raw.pH)
        # print ("Calculated CO2 =       ",raw.total('CO2')*44.0," mg/l")
        # print ("EC =                 ",raw.sc20/100)
        # print ("Calculated aggr. CO2 = ",raw.aggCO2*44.0," mg/l")        
        
        for k in range(0,self.number_of_runs):                # run through number of runs; in principle 1 ;-)
            # calculate Fe, Mn and NH4 conversion and CO2 formation over height
            print('run:                   ',k)
            self.acid_total[self.k,0,-1] = 0                   # for loop
            self.acid_per_height[self.k,0,0] = 0                # zeros
            self.iron_after_ox[self.k,-1,0] = self.iron[0,0,0]        # for loop
            self.manganese_after_ox[self.k,-1,0] = self.manganese[0,0,0]    # for loop
            self.ammonium_after_ox[self.k,-1,0] = self.ammonium[0,0,0]  # for loop
            self.extra_layers = 0                           # zeros
            self.height_counter[self.k] = int(self.number_of_heights)    # height_counter counts number of bed layers, especially important after refilling :-)
            self.inflow = raw.copy()                      # inflow = raw
            # ADJUST LATER DUE TO CHANGING INCOMING RAW WATER QUALITY
            #qual_start = []                           # define array
            #qual_per_layer = []                       # define array
            #qual_start.append(inflow.copy())         # add inflow quality to array qual_start
            
            print (format(sum(self.bed_layer_height_partial[self.k,:,0]),'.3f'), (" m bed; number of heights "), self.number_of_heights )         # print to follow simulation progress
            
            for j in range(0,self.number_of_heights):                     # simulate over number of bed heights
                i = 0
                self.pH_print[self.k,j,i] = self.inflow.pH                      # get pH from array and include in print array
                self.Ca_print[self.k,j,i] = self.inflow.total('Ca')*40.1   # get calcium from array and include in print array
                self.HCO3_print[self.k,j,i] = self.inflow.total('HCO3')*61.0 # get HCO3 from array and include in print array
                self.SI_print[self.k,j,i] = self.inflow.si('Calcite')           # get SI from array and include in print array
                self.agr_CO2_print[self.k,j,i] = self.inflow.aggCO2*44          # get aggressive CO2 content from array and include in print array
                self.CO2_print[self.k,j,i] = self.inflow.total('CO2')*44.0 # get aggressive CO2 content from array and include in print array
                self.EC_print[self.k,j,i] = self.inflow.sc20/100                 # get conductivity from array and include in print array
                self.Cl_print[self.k,j,i] = self.inflow.total('Cl')*35.5   # get chloride from array and include in print array
                self.TAC_print[self.k,j,i] = self.inflow.total('CO3') + self.inflow.total('HCO3') + self.inflow.total('CO2') # calculate TAC from sum of CO2, HCO3 and CO3
                
                if self.bed_layer_height_sum_top0_ascending[self.k,j,i] > self.Fe_height_start: # calculate iron removal progress over height still 1st order
                    self.iron_after_ox[self.k,j,0] = math.exp(self.a_iron * self.bed_layer_height_sum_top0_ascending[self.k,j,0] + self.b_iron)
                    self.iron[self.k,j,0] = self.iron_after_ox[self.k,j-1,0]
                    self.acid_iron[self.k,j,0] = (self.iron[self.k,j,0] - self.iron_after_ox[self.k,j,0]) * 1.57
            
                if self.bed_layer_height_sum_top0_ascending[self.k,j,i] > self.Mn_height_start: # calculate manganese removal progress over height still 1st order
                    self.manganese_after_ox[self.k,j,0] = math.exp(self.a_manganese * (self.bed_layer_height_sum_top0_ascending[self.k,j,0]-self.Mn_height_start) + self.b_manganese)
                    self.manganese[self.k,j,0] = self.manganese_after_ox[self.k,j-1,0]
                    self.acid_manganese[self.k,j,0] = (self.manganese[self.k,j,0] - self.manganese_after_ox[self.k,j,0]) * 1.6
                elif self.bed_layer_height_sum_top0_ascending[self.k,j,i] <= self.Mn_height_start:
                    self.manganese_after_ox[self.k,j,i] = self.manganese[self.k,0,0]   
        
                if self.bed_layer_height_sum_top0_ascending[self.k,j,i] > self.NH4_height_start: # calculate nitrification progress over height still 1st order
                    self.ammonium_after_ox[self.k,j,i] = math.exp(self.a_ammonium * (self.bed_layer_height_sum_top0_ascending[self.k,j,i]-self.NH4_height_start) + self.b_ammonium)
                    self.ammonium[self.k,j,0] = self.ammonium_after_ox[self.k,j-1,0]
                    self.acid_ammonium[self.k,j,i] = (self.ammonium[self.k,j,0] - self.ammonium_after_ox[self.k,j,i]) * 4.9
                elif self.bed_layer_height_sum_top0_ascending[self.k,j,i] <= self.NH4_height_start:
                    self.ammonium_after_ox[self.k,j,i] = self.ammonium[self.k,0,0]
                
                self.acid_total[self.k,j,i] = self.acid_total[self.k,j,i] + self.acid_iron[self.k,j,i] + self.acid_manganese[self.k,j,i] + self.acid_ammonium[self.k,j,i] # add total acid formed by oxidation processes
                self.acid_per_height[self.k,j,i] = self.acid_total[self.k,j,i] - self.acid_total[self.k,j,i-1] # acid formation from oxidation processes per height
                self.acid_mol[self.k,j,i] = self.acid_per_height[self.k,j,i]/44   # convert to moles
                self.total_height = 0.0                           # zeros
                self.total_layer_volume = 0.0                      # zeros 
                 
                
                for i in range(0,self.number_of_fractions):
                    self.acid_mol[self.k,j,i] = self.acid_mol[self.k,j,0]         # fill in acid formation for each fraction at same bed height
        
                mixture = {}                                  # define a MIX     
                qual_start = []                               # define array (empty array)
                
                for i in range(0,self.number_of_fractions):            # calculate "number_of_fractions" times per bed layer height
                    qual_start.append(self.inflow.copy())         # copy new water quality
                    qual_start[i].add('HCl',self.acid_mol[k,j,i])  # "dose" acid from oxidation (Fe, Mn and NH4)
                    
                    self.agr_CO2_after_ox[self.k,j,i] = qual_start[i].aggCO2*44           # aggressive CO2 content after oxidation processes at that height
                    self.pH_after_ox[self.k,j,i] = qual_start[i].pH                       # pH after oxidation processes at that height
                    self.HCO3_after_ox[self.k,j,i] = qual_start[i].total('HCO3')*61  # HCO3 after oxidation processes at that height
                    self.Ca_after_ox[self.k,j,i] = qual_start[i].total('Ca')*40.1    # Ca after oxidation processes at that height
                    self.SI_after_ox[self.k,j,i] = qual_start[i].si('Calcite')            # SI after oxidation processes at that height
                    #########################################################################################################################  
                    # calculation half-height aggressive CO2 from filtration rate(^0.65 to 0.359), porosity, grain shape, grain diameter and density #  (0.087*self.filtration_velocity+0.5652) 
                    #self.half_height_agr_CO2[self.k,j,i] = self.filtration_velocity **(0.359) * self.correction_factor * self.porosity * 1000 * self.grain_shape * self.grain_diameter[self.k,j,i] ** (0.087*self.filtration_velocity+0.5652) / 1000 * 1000 / self.density
                    self.half_height_agr_CO2[self.k,j,i] = self.filtration_velocity **(0.65) * self.correction_factor * self.porosity * 1000 * self.grain_shape * self.grain_diameter[self.k,j,i] ** (0.4) / 1000 * 1000 / self.density
                    #self.half_height_agr_CO2[self.k,j,i] = self.filtration_velocity **(0.359) * self.correction_factor * self.porosity * 1000 * self.grain_shape * self.grain_diameter[self.k,j,i] ** (0.087*self.filtration_velocity+0.5652) / 1000 * 1000 / self.density
                    ########################################################################################################################
                    # determine a and b:  y = a math.logx + b
                    self.a_half_height_agr_CO2[self.k,j,i] = (math.log(self.agr_CO2_after_ox[self.k,j,i] / 2) - math.log(self.agr_CO2_after_ox[self.k,j,i])) /self.half_height_agr_CO2[self.k,j,i]
                    self.b_half_height_agr_CO2[self.k,j,i] = math.log(self.agr_CO2_after_ox[self.k,j,i])
            
                    # calculate aggressive CO2 content after flow through bed layer height of relevant fraction 
                    self.agr_CO2_after_mix[self.k,j,i] = math.exp(self.a_half_height_agr_CO2[self.k,j,i] * self.bed_layer_height_partial[self.k,j,i] + self.b_half_height_agr_CO2[self.k,j,i])
            
                    # convert change in aggressive carbon dioxide content over bed layer height of relevant fraction to amount of soluble CaCO3
                    self.delta_dissolvable_CaCO3_by_agr_CO2[self.k,j,i] = (self.agr_CO2_after_ox[self.k,j,i] - self.agr_CO2_after_mix[self.k,j,i])/44
                                    
                    # dissolve CaCO3 amount calculated above
                    qual_start[i].add('CaCO3',self.delta_dissolvable_CaCO3_by_agr_CO2[self.k,j,i])
            
                    self.agr_CO2_after_softening[self.k,j,i] = qual_start[i].aggCO2*44           # aggressive CO2 content after acidification over bed layer height of certain fraction
                    self.pH_after_softening[self.k,j,i] = qual_start[i].pH                       # pH after acidification over bed layer height of certain fraction
                    self.HCO3_after_softening[self.k,j,i] = qual_start[i].total('HCO3')*61  # HCO3 after acidification over bed layer height of certain fraction
                    self.Ca_after_softening[self.k,j,i] = qual_start[i].total('Ca')*40.1    # calcium after acidification over bed layer height of certain fraction
                    self.SI_after_softening[self.k,j,i] = qual_start[i].si('Calcite')            # SI after acidification over bed layer height of certain fraction
                      
                    mixture[qual_start[i]] = self.filter_surface_portion_grain[self.k,j,i]    # add qual_start[i] to mixture in volume size: filter_surface_portion_grain[k,j,i] 
                        
                    volume_1_grain = 4.0 / 3.0 * math.pi * (self.grain_diameter[self.k,j,i] / 2.0 / 1000) ** 3   # volume of 1 grain in m3
                    volume_grain_layer = self.bed_layer_height_partial[self.k,j,i] * (1.0 - self.porosity) * self.filter_surface_portion_grain[self.k,j,i]        # bed_layer_height * part 1 grain size = volume material in layer in m3/m bed layer height 
                    number_grains_in_layer = volume_grain_layer / volume_1_grain                     # number of grains in layer
                    dissolved_CaCO3 = (self.agr_CO2_after_ox[self.k,j,i] - self.agr_CO2_after_mix[self.k,j,i]) /44 * 100 / 1000 * self.volume_filtered * self.filter_surface_portion_grain[self.k,j,i] / self.filter_surface # dissolved amount of CaCO3 in kg
                    self.dissolved_CaCO3_print[self.k,j,i] = dissolved_CaCO3
                    volume_dissolved_CaCO3 = dissolved_CaCO3 / self.density                              # m3
                    new_volume_grains = volume_grain_layer - volume_dissolved_CaCO3                    # volume after dissolving lime
                                                                     
                    if new_volume_grains <= 0:                                                        # if negative new volume then:
                        self.grain_diameter_new_01[self.k,j,i] = 0.000 
                        new_volume_grains = 0.0                                                       # gone = gone ;-)
                        self.grain_diameter[self.k+1,j,i] = self.grain_diameter_new_01[self.k,j,i]                       #
                        self.total_layer_volume = self.total_layer_volume + new_volume_grains /(1.0-self.porosity) # actually + 0
                        self.volume_grain_fraction[self.k+1,j,i] = new_volume_grains /(1.0-self.porosity)           # also just 0
                
                    else:                                                                                # if positive new volume then:
                        self.grain_diameter_new_01[self.k,j,i] = 2.0 * (3.0 * new_volume_grains / number_grains_in_layer / 4.0 / math.pi) ** (1.0 / 3.0) * 1000.0 # new grain diameter in mm
                        self.grain_diameter[self.k+1,j,i] = self.grain_diameter_new_01[self.k,j,i]                       # new smaller grain diameter
                        self.total_layer_volume = self.total_layer_volume + new_volume_grains /(1.0-self.porosity) # new volume relevant layer
                        self.volume_grain_fraction[self.k+1,j,i] = new_volume_grains /(1.0-self.porosity)           # new volume fraction
                   
                for o in range(0,self.number_of_fractions):
                    self.bed_layer_height_partial[self.k+1,j,o] = self.total_layer_volume                                    # equals total_layer_volume because it's per m2! 
                    self.filter_surface_portion_grain[self.k+1,j,o] = self.volume_grain_fraction[self.k+1,j,o]/self.total_layer_volume # volume part of grain vs total volume
            
                self.bed_layer_height_sum_top0_ascending[self.k+1,j,0] = self.bed_layer_height_sum_top0_ascending[self.k+1,j-1,0] + self.total_layer_volume # calculate new bed height by adding each new bed layer height
                self.bed_layer_height_sum_top2_descending[self.k+1,j,0] = self.bed_layer_height_sum_top0_ascending[self.k+1,self.number_of_heights-1,0] - self.bed_layer_height_sum_top0_ascending[self.k+1,i,0] + self.bed_layer_height_sum_top0_ascending[self.k+1,0,0]
        
                for p in range(0,self.number_of_heights):
                    self.bed_layer_height_sum_top2_descending[self.k+1,p,0] = self.bed_layer_height_sum_top0_ascending[self.k+1,self.number_of_heights-1,0] - self.bed_layer_height_sum_top0_ascending[self.k+1,p,0]+self.bed_layer_height_sum_top0_ascending[self.k+1,0,0]
        
                ## MIX X-number (fractions) water qualities from horizontal layer
                self.inflow = self.pp.mix_solutions(mixture)           #
                self.agr_CO2_after_mix[self.k+1,j,0]= self.inflow.aggCO2*44    # get aggressive CO2 content after mix
                self.EC_after_mix[self.k+1,j,0]= self.inflow.sc20/100           # EC -same-
                
                for q in range(0,self.number_of_fractions):            # clear memory
                    qual_start[q].forget()
                        
            tot = 0.0   
            # check if filter height falls below refill limit
    
            if self.bed_layer_height_sum_top2_descending[self.k+1,0,0] < self.bed_height_refill:
                self.extra_layers =int((self.bed_height_start - self.bed_layer_height_sum_top2_descending[self.k+1,0,0])/(self.bed_height_start/self.number_of_heights_at_start))
                        
                #shift all diameters and partial heights by number of "extra layers" new material layers come on top
                for j in range(0,self.number_of_heights):
                    for i in range(0,self.number_of_fractions):
                        self.grain_diameter_new_01[self.k,j+self.extra_layers,i] = self.grain_diameter[self.k+1,j,i]
                        self.bed_layer_height_partial_temporary[self.k,j+self.extra_layers,i] = self.bed_layer_height_partial[self.k+1,j,i]
                        self.filter_surface_portion_grain_temporary[self.k,j+self.extra_layers,i]= self.filter_surface_portion_grain[self.k+1,j,i]
                for j in range(0,self.extra_layers):
                    for i in range(0,self.number_of_fractions):
                        self.grain_diameter_new_01[self.k,j,i] = self.grain_diameter[2,0,i]
                        self.bed_layer_height_partial_temporary[self.k,j,i] = self.bed_layer_height_partial_start
                        self.filter_surface_portion_grain_temporary[self.k,j,i] = 1.0/self.number_of_fractions
                self.number_of_heights = self.number_of_heights + self.extra_layers
                
                for j in range(0,self.number_of_heights):
                    for i in range(0,self.number_of_fractions):
                        self.grain_diameter[self.k+1,j,i] = self.grain_diameter_new_01[self.k,j,i]
                        self.bed_layer_height_partial[self.k+1,j,i] = self.bed_layer_height_partial_temporary[self.k,j,i]
                        self.filter_surface_portion_grain[self.k+1,j,i] = self.filter_surface_portion_grain_temporary[self.k,j,i]
                    tot = tot + self.bed_layer_height_partial[self.k+1,j,i]
        
        
                self.bed_layer_height_sum_top0_ascending[self.k+1,0,0] = self.bed_layer_height_partial[self.k+1,0,0]
                self.bed_layer_height_sum_top2_descending[self.k+1,0,0] = tot  
        
                for j in range(1,self.number_of_heights):
                    self.bed_layer_height_sum_top0_ascending[self.k+1,j,0] = self.bed_layer_height_sum_top0_ascending[self.k+1,j-1,0]+self.bed_layer_height_partial[self.k+1,j,0]
                    self.bed_layer_height_sum_top2_descending[self.k+1,j,0] = self.bed_layer_height_sum_top2_descending[self.k+1,j-1,0]-self.bed_layer_height_partial[self.k+1,j,0]
        
        print (" "), print(raw.pH)
        # print ("calculated HCO3 =      ", raw.total('HCO3')*61.0, " mg/l")
        # print ("Calculated pH =        ", raw.pH)
        # print ("Calculated CO2 =       ", raw.total('CO2')*44.0, " mg/l")
        # print ("EC =                   ", raw.sc20/100)
        # print ("Calculated aggr. CO2 = ", raw.aggCO2*44.0, " mg/l")

        for k in range(0, self.number_of_runs):                # loop through number of runs; in principle 1 ;-)
            # calculate Fe, Mn and NH4 conversion and CO2 formation over height
            print('run:', k)
            self.acid_total[self.k,0,-1] = 0                   # for loop
            self.acid_per_height[self.k,0,0] = 0               # zeros
            self.iron_after_ox[self.k,-1,0] = self.iron[0,0,0]        # for loop
            self.manganese_after_ox[self.k,-1,0] = self.manganese[0,0,0]    # for loop
            self.ammonium_after_ox[self.k,-1,0] = self.ammonium[0,0,0]  # for loop
            self.extra_layers = 0                           # zeros
            self.height_counter[self.k] = int(self.number_of_heights)    # height_counter counts number of bed layers, especially important after refilling :-)
            self.inflow = raw.copy()                      # inflow = raw
            # ADJUST LATER DUE TO CHANGING INCOMING RAW WATER QUALITY
            #qual_start = []                           # define array
            #qual_per_layer = []                       # define array
            #qual_start.append(inflow.copy())         # add inflow quality to qual_start array
            
            print (format(sum(self.bed_layer_height_partial[self.k,:,0]),'.3f'), (" m bed; number of heights "), self.number_of_heights )         # print to follow simulation progress
            
            for j in range(0,self.number_of_heights):                     # simulate over number of bed heights
                i = 0
                self.pH_print[self.k,j,i] = self.inflow.pH                      # get pH from array and add to print array
                self.Ca_print[self.k,j,i] = self.inflow.total('Ca')*40.1   # get calcium from array and add to print array
                self.HCO3_print[self.k,j,i] = self.inflow.total('HCO3')*61.0 # get HCO3 from array and add to print array
                self.SI_print[self.k,j,i] = self.inflow.si('Calcite')           # get SI from array and add to print array
                self.agr_CO2_print[self.k,j,i] = self.inflow.aggCO2*44          # get aggressive CO2 content from array and add to print array
                self.CO2_print[self.k,j,i] = self.inflow.total('CO2')*44.0 # get aggressive CO2 content from array and add to print array
                self.EC_print[self.k,j,i] = self.inflow.sc20/100                 # get conductivity from array and add to print array
                self.Cl_print[self.k,j,i] = self.inflow.total('Cl')*35.5   # get chloride from array and add to print array
                self.TAC_print[self.k,j,i] = self.inflow.total('CO3') + self.inflow.total('HCO3') + self.inflow.total('CO2') # calculate TAC from sum of CO2, HCO3 and CO3
                
                if self.bed_layer_height_sum_top0_ascending[self.k,j,i] > self.Fe_height_start: # calculate iron removal progress over height still 1st order
                    self.iron_after_ox[self.k,j,0] = math.exp(self.a_iron * self.bed_layer_height_sum_top0_ascending[self.k,j,0] + self.b_iron)
                    self.iron[self.k,j,0] = self.iron_after_ox[self.k,j-1,0]
                    self.acid_iron[self.k,j,0] = (self.iron[self.k,j,0] - self.iron_after_ox[self.k,j,0]) * 1.57
            
                if self.bed_layer_height_sum_top0_ascending[self.k,j,i] > self.Mn_height_start: # calculate manganese removal progress over height still 1st order
                    self.manganese_after_ox[self.k,j,0] = math.exp(self.a_manganese * (self.bed_layer_height_sum_top0_ascending[self.k,j,0]-self.Mn_height_start) + self.b_manganese)
                    self.manganese[self.k,j,0] = self.manganese_after_ox[self.k,j-1,0]
                    self.acid_manganese[self.k,j,0] = (self.manganese[self.k,j,0] - self.manganese_after_ox[self.k,j,0]) * 1.6
                elif self.bed_layer_height_sum_top0_ascending[self.k,j,i] <= self.Mn_height_start:
                    self.manganese_after_ox[self.k,j,i] = self.manganese[self.k,0,0]   
        
                if self.bed_layer_height_sum_top0_ascending[self.k,j,i] > self.NH4_height_start: # calculate nitrification progress over height still 1st order
                    self.ammonium_after_ox[self.k,j,i] = math.exp(self.a_ammonium * (self.bed_layer_height_sum_top0_ascending[self.k,j,i]-self.NH4_height_start) + self.b_ammonium)
                    self.ammonium[self.k,j,0] = self.ammonium_after_ox[self.k,j-1,0]
                    self.acid_ammonium[self.k,j,i] = (self.ammonium[self.k,j,0] - self.ammonium_after_ox[self.k,j,i]) * 4.9
                elif self.bed_layer_height_sum_top0_ascending[self.k,j,i] <= self.NH4_height_start:
                    self.ammonium_after_ox[self.k,j,i] = self.ammonium[self.k,0,0]
                
                self.acid_total[self.k,j,i] = self.acid_total[self.k,j,i] + self.acid_iron[self.k,j,i] + self.acid_manganese[self.k,j,i] + self.acid_ammonium[self.k,j,i] # sum acid formed by oxidation processes total
                self.acid_per_height[self.k,j,i] = self.acid_total[self.k,j,i] - self.acid_total[self.k,j,i-1] # acid formation oxidation processes per height
                self.acid_mol[self.k,j,i] = self.acid_per_height[self.k,j,i]/44   # convert to moles
                self.total_height = 0.0                           # zeros
                self.total_layer_volume = 0.0                      # zeros 
                 
                
                for i in range(0,self.number_of_fractions):
                    self.acid_mol[self.k,j,i] = self.acid_mol[self.k,j,0]         # fill in acid formation for each fraction at same bed height
        
                mixture = {}                                  # define a MIX     
                qual_start = []                               # define array (empty array)
                
                for i in range(0,self.number_of_fractions):            # calculate "number_of_fractions" times per bed layer height
                    qual_start.append(self.inflow.copy())         # copy new water quality
                    qual_start[i].add('HCl',self.acid_mol[k,j,i])  # "dose" acid from oxidation (Fe, Mn and NH4)
                    
                    self.agr_CO2_after_ox[self.k,j,i] = qual_start[i].aggCO2*44           # aggressive CO2 content after oxidation processes at that height
                    self.pH_after_ox[self.k,j,i] = qual_start[i].pH                       # pH after oxidation processes at that height
                    self.HCO3_after_ox[self.k,j,i] = qual_start[i].total('HCO3')*61  # HCO3 after oxidation processes at that height
                    self.Ca_after_ox[self.k,j,i] = qual_start[i].total('Ca')*40.1    # Ca after oxidation processes at that height
                    self.SI_after_ox[self.k,j,i] = qual_start[i].si('Calcite')            # SI after oxidation processes at that height
                    #########################################################################################################################  
                    # calculate half-height aggressive CO2 from filtration velocity(^0.65 to 0.359), porosity, grain shape, grain diameter and density #  (0.087*self.filtration_velocity+0.5652) 
                    #self.half_height_agr_CO2[self.k,j,i] = self.filtration_velocity **(0.359) * self.correction_factor * self.porosity * 1000 * self.grain_shape * self.grain_diameter[self.k,j,i] ** (0.087*self.filtration_velocity+0.5652) / 1000 * 1000 / self.density
                    self.half_height_agr_CO2[self.k,j,i] = self.filtration_velocity **(0.65) * self.correction_factor * self.porosity * 1000 * self.grain_shape * self.grain_diameter[self.k,j,i] ** (0.4) / 1000 * 1000 / self.density
                    #self.half_height_agr_CO2[self.k,j,i] = self.filtration_velocity **(0.359) * self.correction_factor * self.porosity * 1000 * self.grain_shape * self.grain_diameter[self.k,j,i] ** (0.087*self.filtration_velocity+0.5652) / 1000 * 1000 / self.density
                    ########################################################################################################################
                    # determine a and b:  y = a math.logx + b
                    self.a_half_height_agr_CO2[self.k,j,i] = (math.log(self.agr_CO2_after_ox[self.k,j,i] / 2) - math.log(self.agr_CO2_after_ox[self.k,j,i])) /self.half_height_agr_CO2[self.k,j,i]
                    self.b_half_height_agr_CO2[self.k,j,i] = math.log(self.agr_CO2_after_ox[self.k,j,i])
            
                    # calculate aggressive CO2 content after flow through bed layer height of relevant fraction
                    self.agr_CO2_after_softening[self.k,j,i] = math.exp(self.a_half_height_agr_CO2[self.k,j,i] * self.bed_layer_height_partial[self.k,j,i] + self.b_half_height_agr_CO2[self.k,j,i])
            
                    # convert change in aggressive carbon dioxide content over bed layer height of relevant fraction to amount of soluble CaCO3
                    self.delta_dissolvable_CaCO3_by_agr_CO2[self.k,j,i] = (self.agr_CO2_after_ox[self.k,j,i] - self.agr_CO2_after_softening[self.k,j,i])/44
                                    
                    # dissolve CaCO3 amount calculated above
                    qual_start[i].add('CaCO3',self.delta_dissolvable_CaCO3_by_agr_CO2[self.k,j,i])
            
                    self.agr_CO2_after_softening[self.k,j,i] = qual_start[i].aggCO2*44           # aggressive CO2 content after deacidification over bed layer height of specific fraction
                    self.pH_after_softening[self.k,j,i] = qual_start[i].pH                       # pH after deacidification over bed layer height of specific fraction
                    self.HCO3_after_softening[self.k,j,i] = qual_start[i].total('HCO3')*61  # HCO3 after deacidification over bed layer height of specific fraction
                    self.Ca_after_softening[self.k,j,i] = qual_start[i].total('Ca')*40.1    # calcium after deacidification over bed layer height of specific fraction
                    self.SI_after_softening[self.k,j,i] = qual_start[i].si('Calcite')            # SI after deacidification over bed layer height of specific fraction
                      
                    mixture[qual_start[i]] = self.filter_surface_portion_grain[self.k,j,i]    # add qual_start[i] to mixture in volume size: filter_surface_portion_grain[k,j,i]
                        
                    volume_1_grain = 4.0 / 3.0 * math.pi * (self.grain_diameter[self.k,j,i] / 2.0 / 1000) ** 3   # volume of 1 grain in m3
                    volume_grain_layer = self.bed_layer_height_partial[self.k,j,i] * (1.0 - self.porosity) * self.filter_surface_portion_grain[self.k,j,i]        # bed_layer_height * portion 1 grain size = volume material in layer in m3/m bed layer height
                    number_grains_in_layer = volume_grain_layer / volume_1_grain                     # number of grains in layer
                    dissolved_CaCO3 = (self.agr_CO2_after_ox[self.k,j,i] - self.agr_CO2_after_softening[self.k,j,i]) /44 * 100 / 1000 * self.volume_filtered * self.filter_surface_portion_grain[self.k,j,i] / self.filter_surface # dissolved amount of CaCO3 in kg
                    self.dissolved_CaCO3_print[self.k,j,i] = dissolved_CaCO3
                    volume_dissolved_CaCO3 = dissolved_CaCO3 / self.density                              # m3
                    new_volume_grains = volume_grain_layer - volume_dissolved_CaCO3                    # volume after dissolving lime
                                                                     
                    if new_volume_grains <= 0:                                                        # if negative new volume then:
                        self.grain_diameter_new_01[self.k,j,i] = 0.000 
                        new_volume_grains = 0.0                                                       # gone = gone ;-)
                        self.grain_diameter[self.k+1,j,i] = self.grain_diameter_new_01[self.k,j,i]                       #
                        self.total_layer_volume = self.total_layer_volume + new_volume_grains /(1.0-self.porosity) # actually + 0
                        self.volume_grain_fraction[self.k+1,j,i] = new_volume_grains /(1.0-self.porosity)           # also just 0
                
                    else:                                                                                # if positive new volume then:
                        self.grain_diameter_new_01[self.k,j,i] = 2.0 * (3.0 * new_volume_grains / number_grains_in_layer / 4.0 / math.pi) ** (1.0 / 3.0) * 1000.0 # new grain diameter in mm
                        self.grain_diameter[self.k+1,j,i] = self.grain_diameter_new_01[self.k,j,i]                       # new smaller grain diameter
                        self.total_layer_volume = self.total_layer_volume + new_volume_grains /(1.0-self.porosity) # new volume relevant layer
                        self.volume_grain_fraction[self.k+1,j,i] = new_volume_grains /(1.0-self.porosity)           # new volume fraction
                   
                for o in range(0,self.number_of_fractions):
                    self.bed_layer_height_partial[self.k+1,j,o] = self.total_layer_volume                                    # equals total_layer_volume because it's per m2!
                    self.filter_surface_portion_grain[self.k+1,j,o] = self.volume_grain_fraction[self.k+1,j,o]/self.total_layer_volume # volume portion of grain vs total volume
            
                self.bed_layer_height_sum_top0_ascending[self.k+1,j,0] = self.bed_layer_height_sum_top0_ascending[self.k+1,j-1,0] + self.total_layer_volume # calculate new bed height by adding each new bed layer height
                self.bed_layer_height_sum_top2_descending[self.k+1,j,0] = self.bed_layer_height_sum_top0_ascending[self.k+1,self.number_of_heights-1,0] - self.bed_layer_height_sum_top0_ascending[self.k+1,i,0] + self.bed_layer_height_sum_top0_ascending[self.k+1,0,0]
        
                for p in range(0,self.number_of_heights):
                    self.bed_layer_height_sum_top2_descending[self.k+1,p,0] = self.bed_layer_height_sum_top0_ascending[self.k+1,self.number_of_heights-1,0] - self.bed_layer_height_sum_top0_ascending[self.k+1,p,0]+self.bed_layer_height_sum_top0_ascending[self.k+1,0,0]
        
                ## MIX X-number (fractions) water qualities from horizontal layer
                self.inflow = self.pp.mix_solutions(mixture)     
                self.layer_mixture.append(self.inflow)      #
                self.agr_CO2_after_mix[self.k+1,j,0]= self.inflow.aggCO2*44    # get aggressive CO2 content after mix
                self.EC_after_mix[self.k+1,j,0]= self.inflow.sc20/100           # EC -same-
                
                for q in range(0,self.number_of_fractions):            # clear memory
                    qual_start[q].forget()
                        
            tot = 0.0   
            # check if filter height falls below refill limit
    
            if self.bed_layer_height_sum_top2_descending[self.k+1,0,0] < self.bed_height_refill:
                self.extra_layers = int((self.bed_height_start - self.bed_layer_height_sum_top2_descending[self.k+1,0,0])/(self.bed_height_start/self.number_of_heights))
                        
                # shift all diameters and partial heights by number of "extra layers" - new material layers come on top
                for j in range(0,self.number_of_heights):
                    for i in range(0,self.number_of_fractions):
                        self.grain_diameter_new_01[self.k,j+self.extra_layers,i] = self.grain_diameter[self.k+1,j,i]
                        self.bed_layer_height_partial_temporary[self.k,j+self.extra_layers,i] = self.bed_layer_height_partial[self.k+1,j,i]
                        self.filter_surface_portion_grain_temporary[self.k,j+self.extra_layers,i]= self.filter_surface_portion_grain[self.k+1,j,i]
                for j in range(0,self.extra_layers):
                    for i in range(0,self.number_of_fractions):
                        self.grain_diameter_new_01[self.k,j,i] = self.grain_diameter[2,0,i]
                        self.bed_layer_height_partial_temporary[self.k,j,i] = self.bed_layer_height_partial_start
                        self.filter_surface_portion_grain_temporary[self.k,j,i] = 1.0/self.number_of_fractions
                self.number_of_heights = self.number_of_heights + self.extra_layers
                
                for j in range(0,self.number_of_heights):
                    for i in range(0,self.number_of_fractions):
                        self.grain_diameter[self.k+1,j,i] = self.grain_diameter_new_01[self.k,j,i]
                        self.bed_layer_height_partial[self.k+1,j,i] = self.bed_layer_height_partial_temporary[self.k,j,i]
                        self.filter_surface_portion_grain[self.k+1,j,i] = self.filter_surface_portion_grain_temporary[self.k,j,i]
                    tot = tot + self.bed_layer_height_partial[self.k+1,j,i]
        
        
                self.bed_layer_height_sum_top0_ascending[self.k+1,0,0] = self.bed_layer_height_partial[self.k+1,0,0]
                self.bed_layer_height_sum_top2_descending[self.k+1,0,0] = tot  
        
                for j in range(1,self.number_of_heights):
                    self.bed_layer_height_sum_top0_ascending[self.k+1,j,0] = self.bed_layer_height_sum_top0_ascending[self.k+1,j-1,0]+self.bed_layer_height_partial[self.k+1,j,0]
                    self.bed_layer_height_sum_top2_descending[self.k+1,j,0] = self.bed_layer_height_sum_top2_descending[self.k+1,j-1,0]-self.bed_layer_height_partial[self.k+1,j,0]
        
            # reset all calculated values of grains and heights after first run back to [0,j,i] for next calculations
            for j in range(0,self.number_of_heights):
                self.bed_layer_height_sum_top0_ascending[0,j,0] = self.bed_layer_height_sum_top0_ascending[1,j,0]
                self.bed_layer_height_sum_top2_descending[0,j,0] = self.bed_layer_height_sum_top2_descending[1,j,0]
                for i in range(0,self.number_of_fractions):
                    self.filter_surface_portion_grain[0,j,i] = self.filter_surface_portion_grain[1,j,i]
                    self.bed_layer_height_partial[0,j,i] = self.bed_layer_height_partial[1,j,i]
                    self.grain_diameter[0,j,i] = self.grain_diameter[1,j,i]
                    self.acid_total[0,j,i] = 0.0 # reset everything to 0!
           
            print (" ")
            print ("water quality before and after marble filtration:" )
            print ("pH       = ",format(raw.pH,'.3f'),"and ", format(self.inflow.pH ,'.3f'))  # get calcium from array and include in print array
            # print ("Calcium  = ",format(raw.total('Ca')*40.1,'.3f'), "and ", format(self.inflow.total('Ca')*40.1,'.3f')) # get HCO3 from array and include in print array  
            # print ("HCO3     = ",format(raw.total('HCO3')*61.0,'.3f'), "and ", format(self.inflow.total('HCO3')*61.0,'.3f')) # get HCO3 from array and include in print array
            # print ("SI       = ",format(raw.si('Calcite'),'.3f') ,"and ",format(self.inflow.si('Calcite'),'.3f'))        # get SI from array and include in print array
            # print ("CO2      = ",format(raw.total('CO2')*44.0,'.3f'), "and ", format(self.inflow.total('CO2')*44.0,'.3f')) # get HCO3 from array and include in print array
            # print ("aggr. CO2 = ", format(raw.aggCO2*44,'.3f'),"and ", format(self.inflow.aggCO2*44, '.3f'))         # get aggressive CO2 content from array and include in print array
            # print ("EC       = ", format(raw.sc20/100,'.3f'),"and ", format(self.inflow.sc20/100,'.3f'))              # get conductivity from array and include in print array
            # print ("TAC      = ", format(raw.total('CO3') + 
            #                             raw.total('HCO3') + 
            #                             raw.total('CO2'),'.3f'),"and ",format(self.inflow.total('CO3') +
            #                                                                       self.inflow.total('HCO3') +
            #                                                                       self.inflow.total('CO2'),'.3f')) # calculate TAC from sum of CO2, HCO3 and CO3
            # print (format(sum(self.bed_layer_height_partial[self.k,:,0]),'.3f'),("m bed; number of heights"),self.number_of_heights);
            # print (self.k,self.height_counter[self.k])
            
            self.runs.append(k)
            self.height_after_run.append(sum(self.bed_layer_height_partial[self.k,:,0]))
            self.pH_after_run.append(self.inflow.pH)
            self.SI_after_run.append(self.inflow.si('Calcite'))
            self.agrCO2_after_run.append(self.inflow.aggCO2*44)
            self.number_of_heights_after_run.append(self.number_of_heights) 
    def methaneoxidation(self, solution):
        solution = solution.copy()
        solution.change({'Mtg': solution.total('Mtg')*0.999999})
        return solution
    def oxygenadjustment(self, solution):
        #Calculate used oxygen
        # per 02(aq) we oxidize 4 Fe2+ ions
        influent =self.quality.influent.product.copy()
        oxygen_for_iron= (influent.total('Fe') - solution.total('Fe'))/4
        oxygen_for_manganese= (influent.total('Mn') - solution.total('Mn'))/4
        oxygen_for_methane= (influent.total('Mtg') - solution.total('Mtg'))/2
        oxygen_for_ammonium= (influent.total('NH4') - solution.total('NH4'))/2
        oxygen_for_nitrate= (influent.total('NO3') - solution.total('NO3'))/2
        oxygen_for_total = oxygen_for_iron + oxygen_for_manganese + oxygen_for_ammonium + oxygen_for_nitrate + oxygen_for_methane
        solution.change({'O2': oxygen_for_total})
        return solution
        
        def endsolution(self, solution):
            effluent = solution.copy()
            print(self.iron_after_ox[0,-1,0])
        
        # effluent.change({'Ca': self.Ca[0,0,0],
        #                  'Mg': self.Mg[0,0,0], 
        #                  'Na': self.Na[0,0,0],
        #                  'Fe': self.iron_after_ox[0,-1,0],
        #                  'Mn': self.manganese[0,0,0],
        #                  'N(5)': self.NO3[0,0,0],
        #                  'N(-3)': self.ammonium[0,0,0],
        #                  'S(6)': self.SO4[0,0,0],
        #                  'Cl': self.Cl[0,0,0],
        #                  'Alkalinity': str(self.HCO3[0,0,0]) + ' as HCO3',
        #                  'pH': self.pH[0,0,0],
        #                  'temp': self.Temp, 
                         
        # })
            return effluent


    def oxidize(self, solution, from_element, to_element, oxygen_consumption, efficiency=1):
        solution = solution.copy()
        to_exchange = solution.total(from_element) * 0.999999 # prevent negative concentrations
        oxygen_available = solution.total("O2") # free oxygen

        to_exchange = min(to_exchange, oxygen_available / oxygen_consumption)
        to_exchange = to_exchange * efficiency

        # print(f"Oxidizing {from_element} to {to_element} with {to_exchange} oxygen")
        solution.change({from_element: -to_exchange, to_element: to_exchange})

        return solution
    def wastestream_calculation(self, solution):
        if self.parameters['backwash_control'] == 'volume':
            captured_iron = self.removed_iron  * self.parameters['runvolume']/1000
        else:
            captured_iron = self.removed_iron * self.parameters['nominal_capacity'] *self.parameters['runtime']/1000
        self.waste_iron = captured_iron/self._backwash_volume *1000
        solution = solution.copy()
        solution.change({'Fe': self.waste_iron}, units='mg')
        solution.saturate("Calcite", 0)
        return solution
    
    def filtrate(self, solution):
        ## Same as sandfiltration.py with the added calcite saturation after each oxidation step
        # suppress removal of elements if set to True


        influent = solution.copy()
        # replace inert oxygen with free oxygen
        influent.change({ "O2": influent.total("Oxg"), "Oxg": -influent.total("Oxg")*0.99999})


        # oxidize methane

        after_ch4 = self.oxidize(influent, "Mtg", "CH4", 2)
        after_ch4 = after_ch4.saturate("Calcite", 0)
            
        after_fe = self.oxidize(after_ch4, "[Fe+2]", "Fe+2", 0.25).desaturate("Fe(OH)3(a)", 0)
        after_fe = after_fe.saturate("Calcite", 0)
        # oxidize h2
        after_h2s = self.oxidize(after_fe, "[S-2]", "S-2", 2)
        after_h2s = after_h2s.saturate("Calcite", 0)


        after_nh4 = self.oxidize(after_h2s, "[N-3]", "N-3", 2)
        after_nh4 = after_nh4.saturate("Calcite", 0)
        after_no2 = self.oxidize(after_nh4, "[N+3]", "N+3", 2)
        after_no2 = after_no2.saturate("Calcite", 0)
        after_mn = self.oxidize(after_no2, "[Mn+2]", "Mn+2", 0.5).desaturate("Manganite", 0)
        after_mn = after_mn.saturate("Calcite", 0)

        effluent = after_mn.copy()

        return effluent, [influent, after_ch4, after_fe, after_h2s, after_nh4, after_no2, after_mn]

    
    def run_quality(self, type, total_inflow, solution):
        if(type == 'flush'):
            # add load to waste solution
            self.waste_solution = self.wastestream_calculation(solution.copy())
            return self.waste_solution
        if(type == 'product'):
            solution  = self.quality.influent.product.copy()
            effluent, _ = self.filtrate(solution)
            return effluent
            # solution  = self.quality.influent.product.copy()
            # effluent, _ = self.filtrate(solution)
            # print(f"Effluent: {effluent}")
            # return effluent

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

        # if(self.sprayaeration):
        #     solution = self.spray_aeration(self.quality.influent.product, self.compound, self.RQ, self.fall_height)
        #     labels = ["spray", "methane_oxidation", "iron_removal", "h2s_oxidation", "nitrification", "denitrification", "manganese_removal"]
        #     step_results = {}
        #     for n, v in values.items():
        #         step_results[n] = v(self.quality.influent.product.copy())
        #     results["influent"]= step_results
            
        # else:
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

        
         
   



