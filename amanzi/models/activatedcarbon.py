from .model import Model
from .submodels.balance import Balance
import math
import numpy as np
from .tower.compounds import Chemical
from .CADET.modelsetup import CADETMODEL
import warnings
warnings.simplefilter("ignore")
import os
srt_dir = os.getcwd()
import bisect
import pandas as pd
import matplotlib.pyplot as plt

from .PSDM import PSDM
from .PSDM import PSDM_functions



class Activatedcarbon(Model, Balance):

    def __init__(self, config, pp: dict = {}) -> None:
        super().__init__(config, pp)

        self.configuration = config.get('configuration', {})
        self.packing_height = float(self.configuration.get('packing_height', 2.5))
        self.dimension = float(self.configuration.get('diameter', 2))
        self.packing_type = self.configuration.get('packing_type', 'NORA Supra 0.8')
        self.volumeflow = float(self.configuration.get('volumeflow', 100))
        self.packing_volume = self.packing_height * math.pi * (self.dimension/2)**2
        self.capacity = float(self.configuration.get('capacity', 100))
        self.compoundList = self.configuration.get('compound', {'x':0})
        self.advanced = self.configuration.get('advanced', False)
        self.renewal = int(self.configuration.get('interval', 1000))
        self.filternumber = int(self.configuration.get('filternumber', 1))
        
        

    def calculate_efficiency(self, compound, solution): 
        #Freundlich Isotherm parameters
        #Diffusion koefficient for film diffusion from water to GAC from compound file'
        
        t_in_seconds = 134776000
        resolution = 100
        volume_flow_rate = self.volumeflow/3600 #m³/s
        height = self.packing_height            #m
        crosssection = math.pi * (self.dimension/2)**2  #m²
        filmdiffusion =  Chemical(20,20).properties()['CO2']['Diff_water']*1000#m²/s should be m/s thats why *1000
        freundlich_k = self.freundlich_k
        freundlich_n = self.freundlich_n
                
        cadet_model = CADETMODEL()
        model=cadet_model.create_and_run_model(t_in_seconds, [solution.total('CO2', 'mol')*1000],  resolution, volume_flow_rate, height, crosssection, filmdiffusion,freundlich_k, freundlich_n)

        efficiency= 1-(model.root.output.solution.unit_001.solution_outlet[3][0]/solution.total('CO2', 'mol'))

        return efficiency
    def PSDMcalculation(self, solution):
        

        os.chdir(srt_dir)
         
        water_type = 'Organic Free'
        chem_type = 'halogenated alkenes'
        nr=4
        nz=8
        ne=2

        particleRadius=0.04 #cm
        apparentD= 0.5
        particleD=0.5
        length= self.packing_height*100 #cm
        diameter= self.dimension*100 #cm
        bedporosity=0.4
        massGAC=bedporosity* apparentD*length*math.pi*(diameter/2)**2
        flowrate= self.capacity*1e6/60 #ml/min
        volumebed= length*math.pi*(diameter/2)**2 #cm³
        volumeflow = flowrate*60*24 # ml/day
        EBCT=volumebed/flowrate 
        #print(EBCT)


        data = {    'name': ['carbonID', 'rad', 'epor', 'psdfr', 'rhop', 'rhof', 'L', 'wt', 'flrt', 'diam', 'tortu', 'influentID', 'effluentID'],	
                    'value': ['F400', particleRadius, 0.641,    5,     apparentD,   particleD,  length, massGAC, flowrate,   diameter,    1, 'influent', 'effluent'],
                } 
        #default time is days

        # data = {    'name': ['carbonID', 'rad', 'flrt','epor', 'psdfr', 'rhop', 'rhof', 'L', 'wt',  'diam', 'tortu', 'influentID', 'effluentID', 'units', 'time','mass_mul' ,'t_mult', 'flow_mult', 'flow_type'],	
        # 'value': ['F400', 0.0513,1892705.892, 0.641, 5, 0.803, 0.62, 180, 8500000,  366, 1, 'influent', 'effluent', 'ug', 'days', 1.0, 1440, 0.001, 'ml'],
        # 'units': ['', 'cm', '', '', 'g/ml', 'g/ml', 'm', 'kg', 'gpm', 'm', '', '', '', '', '', '', '', '', ''],	} 
        df = pd.DataFrame(data, index=data['name'])
        df.name=data['value'][0]
        data_conc={}
        PFASproperties = {}
        for compound in self.influent.extraneous['PFAS']:
            data_conc['influent', compound] = [self.influent.extraneous['PFAS'][compound], self.influent.extraneous['PFAS'][compound]]
            data_conc['F400', compound] = [0, 0]

            PFASproperties[compound] = [float(self.compoundList[compound][0]),float(self.compoundList[compound][1]),float(self.compoundList[compound][2])]


        #index = pd.MultiIndex.from_tuples([(0, 'influent'), (1000, 'F400')], names=['time', 'carbonID'])
        index = pd.Index([0, self.renewal*2], name='time')
        df_conc = pd.DataFrame(data_conc, index=index)
        df_conc.columns = pd.MultiIndex.from_tuples([(col[0], col[1]) for col in df_conc.columns], names=['type', 'compound'])
        #df_conc.columns.levels[0]='compound'


       
        
        index = ['K', '1/n', 'q']
        df_kData = pd.DataFrame(PFASproperties, index=index)
        # K, 1/n, q
        data_k = {
            'PFBS': [456.94, 0.411, 1], #PSDM PFAS Excel
            'PFPeS': [1521, 0.3521, 1],#PSDM PFAS Excel
            'PFHxS': [3832.9, 0.3136, 1], #PSDM PFAS Excel
            'PFHpS': [4588.9, 0.286, 1],#PSDM PFAS Excel
            'PFOS': [7222, 0.2525, 1],#PSDM PFAS Excel
            'PFHxS': [3840, 0.3134, 1],#PSDM PFAS Excel
            'PFDS': [0.1, 1, 1], #No values could be found
            'TFA': [2.3*(1000/(1000**0.343)), 0.343, 1], # 2.3 (mg/g)(l/mg)^1/n ; 1/n: 0.343 ; Source: Polypyrrole-Tailored Activated Carbon for Trifluoroacetate Removal from Groundwater
            'PFBA': [255, 0.4942, 1],#PSDM PFAS Excel
            'PFPeA': [1160, 0.4252, 1],#PSDM PFAS Excel
            'PFHxA': [4179, 0.3607, 1],#PSDM PFAS Excel
            'PFHpA': [498, 0.3144, 1],#PSDM PFAS Excel
            'PFOA': [1718, 0.2808, 1],#PSDM PFAS Excel
            'PFDA': [6371, 0.2415, 1],#PSDM PFAS Excel
            'PFUnDA': [14603, 0.2233, 1],#PSDM PFAS Excel
            'PFDoDA': [18106, 0.2076, 1],#PSDM PFAS Excel
            'PFTrDA': [25862, 0.1972, 1],#PSDM PFAS Excel
            'PFTeDA': [30582, 0.1858, 1] #PSDM PFAS Excel
        }


        index = ['K', '1/n', 'q']

        # df_kData = pd.DataFrame(PFASproperties, index=index)
        # MW , MolarVol ,BP(Boling Point),Density ,Solubility (unused), VaporPress (unused)
        #Reference for PFAS data ITRC PFAS Technical and regulartory Guidance document
        NaN=0
        data_properties = {
            'PFBS': [300.1, 163.9, 198, 1.83, 0,0], # PSDM PFAS Excel
            'PFPeS': [350, 190.2, 225, 1.84, 0, 0],#ITRC
            'PFHpS': [450, 238, 226,1.89, 0, 0], #ITRC
            'PFOS': [500, 237, 189, 1.8, 0, 0],  # PSDM PFAS Excel
            'PFHxS':  [400, 217, 239, 1.84, 0, 0], # PSDM PFAS Excel
            'PFDS':  [600, 310.9 , 255, 1.93, 0, 0], #ITRC
            'TFA':  [114, 129.7, 72, 1.489, 0, 0], #merckmillipore.com
            'PFBA':  [214, 129.72, 121, 1.65, 0, 0], # PSDM PFAS Excel
            'PFPeA':  [264, 154, 139, 1.71, 0, 0],#ITRC
            'PFHxA':  [314, 182, 157, 1.69, 0, 0],  # PSDM PFAS Excel
            'PFHpA': [364, 212.9, 175, 1.71, 0, 0],   # PSDM PFAS Excel
            'PFOA': [500, 217, 145, 1.84, 0,0],  # PSDM PFAS Excel
            'PFDA':  [514, 292, 184, 1.79, 0,0], # PSDM PFAS Excel
            'PFUnDA':  [564.1,304.8 , 238.4, 1.85, 0, 0], #ITRC
            'PFDoDA':  [614.1, 328.3, 249, 1.87, 0, 0],#ITRC
            'PFTrDA':  [664.1, 345.8, 261, 1.92, 0, 0],#ITRC
            'PFTeDA':  [714.1, 368, 270, 1.94, 0, 0],#ITRC
        }

        index = ['MW', 'MolarVol', 'BP', 'Density', 'Solubility', 'VaporPress']
        df_properties = pd.DataFrame(data_properties, index=index)
        
        #print(df_properties)

        #print(chem_data)

        column = PSDM.PSDM(df['value'], df_properties, df_conc,\
                                nz=nz,\
                                nr=nr,\
                                ne=ne,\
                                chem_type=chem_type,\
                                water_type=water_type,\
                                k_data=df_kData,\
                                solver='BDF')
            
        print('Starting example multicomponent simulation\n', 'This may take several minutes')
       
        all_results = column.run_psdm()
        for i in all_results.keys():
            idx = all_results[i].x
            #print(all_results[i](idx))
        return all_results

    
    def simpleExtraneousRemoval(self, solution):  
        for i in self.scenario['metaData']['customMicroComponents']['PFAS']:
            name= i['name']
            removal_efficiency = i['removalAKF']
            if name in solution.extraneous['PFAS']:
                solution.extraneous['PFAS'][name]=solution.extraneous['PFAS'][name]*(1-float(removal_efficiency))
        for i in self.scenario['metaData']['customMicroComponents']['Other']  :
            name= i['name']
            removal_efficiency = i['removalAKF']
            if name in solution.extraneous['Other']:
                solution.extraneous['Other'][name]=solution.extraneous['Other'][name]*(1-float(removal_efficiency))    
        return solution
    
    def advancedExtraneousRemoval(self, solution):
        # Calculation of average effluent concentration for each compound
        # Using the regeneration of the GAC filter assuming equal distatnces between each regeneration of a filter
        PSDMcalculation = self.PSDMcalculation(self.influent)
        solEffluent=solution.extraneous['PFAS']
        for key in PSDMcalculation:
            idx = PSDMcalculation[key].x
            for j in range(self.filternumber):
                divider = self.renewal/(j+1)
                pos=self.find_closest(idx,divider)
                linFactor= (divider-idx[pos])/divider
                #linear interpolation 
                Effluentconc=PSDMcalculation[key](idx)[pos]+PSDMcalculation[key](idx)[pos]*linFactor
                if j == 0:
                    solEffluent[key]= Effluentconc*(1/(self.filternumber))
                else:
                    solEffluent[key]= solEffluent[key]+Effluentconc*(1/(self.filternumber))
        return solution
    
    def unitcheck(self,solution):
        # ng/l is the default unit for PFAS influent and effluent
        for i in self.scenario['metaData']['customMicroComponents']['PFAS']:
            if i['name'] in solution.extraneous['PFAS']:
                print(f"PFAS: {i['name']} {solution.extraneous['PFAS'][i['name']]}")
                if i['unit'] == 'mg/l':
                    solution.extraneous['PFAS'][i['name']] = self.influent.extraneous['PFAS'][i['name']]*1000000
                elif i['unit'] == 'μg/l':
                    solution.extraneous['PFAS'][i['name']] = self.influent.extraneous['PFAS'][i['name']]*1000
        return solution


    def run_model(self, type, total_inflow,solution):
        solution = self.unitcheck(solution.copy())

        if self.advanced == False:
            solution = self.simpleExtraneousRemoval(solution.copy())

        if self.advanced == True:
            solution = self.advancedExtraneousRemoval(solution.copy())


        #solution = effluent
       
        return solution
    
    

    def find_closest(self,nums, target):
        # Find the position where target should be inserted to maintain sorted order
        pos = bisect.bisect_left(nums, target)

        # If the target is the first element or exactly matches an element in the list
        if pos == 0:
            return 0
        if pos == len(nums):
            return len(nums) - 1

        # If target is not in nums, check the closest number (either before or after)
        before = nums[pos - 1]
        after = nums[pos]

        if after - target < target - before:
            return pos
        else:
            return pos - 1

    def design(self):          
        eff = {}
        peqPFAS={}
        sum4=[]
        sum20=[]
        peq2={}
        if self.compoundList != {} and self.compoundList.values() != [0] and self.advanced == True:
            PSDMcalculation = self.PSDMcalculation(self.influent)
            dict_keys = list(PSDMcalculation.keys())
            for i in self.scenario['metaData']['customMicroComponents']['PFAS']:
                if i['name'] in self.influent.extraneous['PFAS']:
                    peq2[i['name']] = i['PEQ']
  
            eff = {}
            solEffluent=self.solution.extraneous['PFAS']
            peq1=[0] * len(PSDMcalculation[dict_keys[0]].x)
            sum4=[0] * len(PSDMcalculation[dict_keys[0]].x)
            sum20=[0] * len(PSDMcalculation[dict_keys[0]].x)
            length= self.packing_height*100 #cm
            diameter= self.dimension*100 #cm
            bedporosity=0.4
            massGAC=bedporosity* 0.5*length*math.pi*(diameter/2)**2
            flowrate= self.capacity*1e6/60 #ml/min
            volumebed= length*math.pi*(diameter/2)**2 #cm³
            volumeflow = flowrate*60*24 # ml/day
            bedvolumesPerDay=volumeflow/volumebed
            for key in PSDMcalculation:

                idx = PSDMcalculation[key].x
                #print(PSDMcalculation[key](idx))               
                eff[key] = [{'x': idx[k]*bedvolumesPerDay , 'y': PSDMcalculation[key](idx)[k]/self.influent.extraneous['PFAS'][key] } for k in range(len(PSDMcalculation[key].x))]

                for k in range(len(PSDMcalculation[key].x)):
                    if key == dict_keys[0]:
                        peq1[k] = PSDMcalculation[key](idx)[k]*peq2[key]
                    else:
                        peq1[k] = PSDMcalculation[key](idx)[k]*peq2[key]+peq1[k]
                    if key in ['PFOA', 'PFOS', 'PFHxS', 'PFHpS']:
                        sum4[k] = sum4[k]+PSDMcalculation[key](idx)[k]*peq2[key]
                    if key in ['PFOA', 'PFOS', 'PFHxS', 'PFHpS', 'PFHxS', 'PFHpS', 'PFDS', 'PFBA', 'PFPeA', 'PFHxA', 'PFHpA', 'PFOA', 'PFDA', 'PFUnDA', 'PFDoDA', 'PFTrDA', 'PFTeDA']:
                        sum20[k] = sum20[k]+PSDMcalculation[key](idx)[k]*peq2[key]

            peqPFAS = [{'x': idx[k]*bedvolumesPerDay , 'y': peq1[k] } for k in range(len(PSDMcalculation[key].x))]
            sum4= [{'x': idx[k]*bedvolumesPerDay , 'y': sum4[k] } for k in range(len(PSDMcalculation[key].x))]
            sum20= [{'x': idx[k]*bedvolumesPerDay , 'y': sum20[k] } for k in range(len(PSDMcalculation[key].x))]


            
        

        #print(eff) 
        #Assuming the same adsorption capacity for all compounds in mg/m³ GAC
        iodineNumber = 1000 #g/kg GAC
        bedporosity = 0.5
        GACdensity = 500 #kg/m³
        capacityFactor = GACdensity*bedporosity*iodineNumber*1000 #mg/m³ GAC
        if 'PFAS' in self.influent.extraneous and self.influent.extraneous['PFAS'] != {}:
            sumPFASinGAC = (sum(self.influent.extraneous['PFAS'].values())-sum(self.solution.extraneous['PFAS'].values()))*1e-6 #sum of all PFAS in mg/l
        else:
            sumPFASinGAC = 0.00000000001
        if 'Other' in self.influent.extraneous and self.influent.extraneous['Other'] != {}:
            sumOtherinGAC = (sum(self.influent.extraneous['Other'].values())-sum(self.solution.extraneous['Other'].values()))*1e-6 #sum of all Other in mg/l
        else:
            sumOtherinGAC = 0.00000000001
        volumeGAC = (self.packing_height* math.pi * (self.dimension/2)**2) 
        regeneration = (volumeGAC *capacityFactor / ((sumPFASinGAC+sumOtherinGAC)*self.capacity*1000)) #capcity divided by amount of organics adsorbed per hour

        relevantInfluent = self.influent.extraneous['PFAS'].copy()
        relevantInfluent.update(self.influent.extraneous['Other'])
        relevantEffluent = self.solution.extraneous['PFAS'].copy()
        relevantEffluent.update(self.solution.extraneous['Other'])
        #print(relevantEffluent)



        
        return {
            'influent': relevantInfluent
            ,
            'effluent': relevantEffluent
            ,
            'model': {
                'regeneration': regeneration/(24*365),
                'EBCT' : self.packing_volume/(self.volumeflow/60),
                'peqPFAS':peqPFAS,
                'sum4PFAS': sum4,
                'sum20PFAS': sum20,
                'Volume': self.packing_volume,
                'breakthrough': eff
            }
        }