from .model import Model
from .submodels.balance import Balance
import math
import numpy as np
from .tower.onda import run_onda
from .tower.engelstichlmair import run_engelstichlmair
from .tower.mackoviak import run_mackoviak
from .tower.water_properties import Water
from .tower.air_properties import Air
from .tower.packing_properties import packing
from .tower.compounds import Chemical




class Toweraeration(Model, Balance):
    parametric_model = ['model', 'toweraeration', 'aeration']
    def __init__(self, config, pp: dict = {}) -> None:
        super().__init__(config, pp)
        self.configuration = config.get('configuration', {})
        self.rq = float(self.parameters['rq'])
        self.diameter = float(self.parameters['diameter'])
        self.packing_type = self.parameters['packingmaterial']
        self.packing_height = float(self.parameters['bed_height'])
        self.min_capacity = float(self.parameters['minimal_capacity'])
        self.capacity = float(self.parameters['nominal_capacity'])
        self.max_capacity = float(self.parameters['maximal_capacity'])
        self.compound = self.configuration.get('model_component', 'CO2')
        self.temp_g = float(self.parameters['ambient_temperature'])

        self.totalpressuredrop = 0 
        self.g_density = Air(self.temp_g, 1.023e5).density()
        self.operationparams={}
        self.removalrates = {}
        self.eng_stickl = None
        
    @property
    def deltaPtotal(self):
        return self.totalpressuredrop

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
        print(((Pin+delta_p)/Pin))
        return Pavg
    @property
    def engel_stickl(self):
        if self.quality.influent.product:
            temp= self.quality.influent.product.temperature 
        else:
            temp=10
        return run_engelstichlmair(temp,self.temp_g, self.packing_type)
    
    @staticmethod
    def operationpoint(capacity, RQ, diameter, engel_stickl_object):

        column_is_flooding = False
        try:
            dp_dry,dp_tot, h_tot ,F, flooding_factor= engel_stickl_object.operating_point(capacity, RQ, diameter)
            if isinstance(dp_tot, complex):
                raise ValueError("dp_tot is a complex number.")
            if isinstance(h_tot, complex):
                raise ValueError("h_tot is a complex number.")
        except Exception as e:
            print(f"An error occurred : {e}")
            dp_dry,dp_tot, h_tot ,F, flooding_factor = 0, 0, 0, 0,0
            column_is_flooding = True
        return [dp_tot, h_tot, F, flooding_factor, column_is_flooding]

    @property
    def context(self):
        ctx = super().context
        ctx['blower_power'] = self.blower_power
        ctx['deltaPtotal'] = self.deltaPtotal
        ctx['Air_density'] = self.g_density
        ctx['packing'] = packing()[self.packing_type]
        ctx['engel_stickl'] = self.engel_stickl
        ctx['operationpoint'] = self.operationpoint
        return ctx
      
    def get_NTU(self,T_liq,T_gas,flow,diameter, packing_height, packing, RQ, compound, c_in, c_gas,HTU_ov):

        comp=Chemical(T_liq,T_gas)
        Hc= comp.properties()[compound]['Henry'] #dimensionless Henry
        Sf=Hc*RQ
        #Calculate efficiency
        z = np.exp((packing_height*(Sf-1))/(HTU_ov*Sf))
        c_out_eq=c_gas/Hc # ist l, c+in ist p
        c_out = (Sf*c_out_eq*z-Sf*c_out_eq+Sf*c_in-c_in)/(Sf*z-1)
        efficiency= ((c_in-c_out)/c_in)
        
        c_g_o=c_gas+(c_in-c_out)/RQ
        NTU_ov=(Sf/(Sf-1)) * np.log((c_in-c_gas/Hc)*(Sf-1)/((c_out-c_gas/Hc)*Sf)+(1/Sf))
       
        return efficiency

    def calculate_efficiency(self,compound, RQ, packing_height,capacity, solution=0): 
        influent = self.quality.influent.product
        T_liq= influent.temperature
        T_gas= self.temp_g
        flow = capacity
        packing = self.packing_type
        diameter=self.diameter
        if self.compound == 'CO2':
            c_gas = 0.82/16/1000
        else:
            c_gas=0

        if compound != 'CO2' and compound != 'Mtg' and compound != 'Oxg':
            if influent.extraneous['VOC'][compound] >0 :
                c_in=influent.extraneous['VOC'][compound]
            else:
                c_in =0.0000001
        else:
            c_in = influent.total(compound, units='mmol')

        if compound == 'Oxg':
            solution = influent.copy()
            oxg_in = influent.total("Oxg", "mmol")
            o2_in = influent.total("O2", "mmol")

            delta = o2_in - oxg_in        
            solution.add('Oxg', delta, 'mmol')
            c_in =solution.total("Oxg", "mmol")
            c_gas =0.208*101325/(8.31446*(273.15+T_gas)) #9.4 mmol/l == 260mg/l
            


        HTU_ov = run_onda(T_liq,T_gas,flow,diameter, packing_height, packing, RQ, compound, c_in, c_gas)
        
        efficiency= self.get_NTU(T_liq,T_gas,flow,diameter, packing_height, packing, RQ, compound, c_in, c_gas,HTU_ov)
        
        return efficiency


    def oxygen_transfer(self, solution):
        o2_in_gas = 9.4 # mol/m³
        o2_in = self.quality.influent.product.total("O2", "mmol")
        o2_efficiency = self.calculate_efficiency('Oxg', self.rq,self.packing_height, self.capacity)      
        c_O2_out =-(o2_efficiency*o2_in-o2_in)
        c_o2_change = abs(o2_in-c_O2_out)
        #print(c_o2_change)
        return c_o2_change
    
    def unitcheck(self,solution):
        # mg/l is the default unit for  VOC influent and effluent
        for i in self.scenario['metaData']['customMicroComponents']['VOC']:
            if i['name'] in solution.extraneous['VOC']:
                if i['unit'] == 'ng/l':
                    solution.extraneous['VOC'][i['name']] = self.quality.influent.product.extraneous['VOC'][i['name']]/1000000
                elif i['unit'] == 'μg/l':
                    solution.extraneous['VOC'][i['name']] = self.quality.influent.product.extraneous['VOC'][i['name']]/1000
        return solution


    def run_quality(self, type, total_inflow, solution):
        solution = self.unitcheck(solution.copy())
        self.eng_stickl = run_engelstichlmair(self.quality.influent.product.temperature,self.temp_g, self.packing_type)

        ## gets called by solver
        co2_removal= self.calculate_efficiency('CO2',self.rq, self.packing_height, self.capacity)
        ch4_removal= self.calculate_efficiency('Mtg',self.rq, self.packing_height, self.capacity)
        o2_change = self.oxygen_transfer(self.quality.influent.product)
        solution.remove_fraction('CO2', co2_removal)
        solution.remove_fraction('Mtg', ch4_removal)
        for key in self.quality.influent.product.extraneous['VOC']:
            if self.quality.influent.product.extraneous['VOC'][key] >0:
                removal = self.calculate_efficiency(key,self.rq,self.packing_height, self.capacity)
                solution.extraneous['VOC'][key] = self.quality.influent.product.extraneous['VOC'][key] * (1-removal)
        solution.add('O2',o2_change , 'mmol')
        return solution

    def generate_tables(self):
        tables = super().generate_tables()

        tables[0]['sections'].append({
            'name': 'removalrates',
            'namespace': 'toweraeration',
            'precision': 0,
            })
        tables[0]['outputs'].append({
            'name': 'CO2',
            'uom': '%',
            'precision': 1,
            'namespace': 'toweraeration',
            'section': 'removalrates',
            'indent': False,
            'min': max(self.calculate_efficiency('CO2',self.rq,self.packing_height, self.min_capacity),0),
            'nom': max(self.calculate_efficiency('CO2',self.rq,self.packing_height, self.capacity),0),
            'max': max(self.calculate_efficiency('CO2',self.rq,self.packing_height,self.max_capacity),0)})
        tables[0]['outputs'].append({
            'name': 'Methane',
            'uom': '%',
            'precision': 1,
            'namespace': 'toweraeration',
            'section': 'removalrates',
            'indent': False,
            'min': max(self.calculate_efficiency('Mtg',self.rq,self.packing_height, self.min_capacity),0),
            'nom': max(self.calculate_efficiency('Mtg',self.rq,self.packing_height, self.capacity),0),
            'max': max(self.calculate_efficiency('Mtg',self.rq,self.packing_height,self.max_capacity),0)})
        for VOC in self.quality.influent.product.extraneous['VOC']:
            if self.quality.influent.product.extraneous['VOC'][VOC] >0:
                tables[0]['outputs'].append({
                    'name': VOC,
                    'uom': '%',
                    'precision': 1,
                    'namespace': 'toweraeration',
                    'section': 'removalrates',
                    'indent': False,
                    'min': max(self.calculate_efficiency(VOC,self.rq,self.packing_height, self.min_capacity),0),
                    'nom': max(self.calculate_efficiency(VOC,self.rq,self.packing_height, self.capacity),0),
                    'max': max(self.calculate_efficiency(VOC,self.rq,self.packing_height, self.max_capacity),0)
                })
 
        return tables

    def design(self):
        
        influent= self.quality.influent.product
        ## gets called by design GUI
        liquid = Water(influent.temperature)
        rho_l = liquid.density()        # kg/m³
        p=1.023e5
        gas = Air(self.temp_g,p)
        rho_g = gas.density()           # kg/m³
        Area= math.pi*float(self.diameter)**2/4            # m² d in m
        # Column operation
        u_l = self.capacity/Area/3600             # m³/m²/s liquid loading
        ## flooding and operating charts
        def Capacity_gas(u_g):
            return u_g*math.sqrt(rho_g/(rho_l-rho_g))
        def Capacity_liq(u_l):
            return u_l*math.sqrt(rho_l/(rho_l-rho_g))

        werkpunt_hydro = [{'x': Capacity_liq(u_l), 'y': Capacity_gas(u_l*self.rq)}]

        werkpunt_quality =[{'x': self.rq, 'y': self.calculate_efficiency(self.compound,self.rq,self.packing_height, self.capacity)}]
        
        Liquid_capacity= np.linspace(0.01, 0.1, 30)#capacity liquid m/s
        

        Gas_capacity_flooding, _=self.eng_stickl.flooding_line(Liquid_capacity,1)
        Gas_capacity_loading, _=self.eng_stickl.flooding_line(Liquid_capacity,0.65)

        flooding = [{'x':Liquid_capacity[x] , 'y': Gas_capacity_flooding[x]} for x in range(len(Liquid_capacity))]
        operating = [{'x': Liquid_capacity[x] , 'y': Gas_capacity_loading[x]} for x in range(len(Liquid_capacity))]
        ## Efficiency loading and height charts
        Rq_space = np.linspace(0.1,100,100)

        heights = [1,2,3,4, self.packing_height]
        height_charts = {}
        if self.compound != 'CO2' and self.compound != 'Mtg' and influent.extraneous['VOC'][self.compound] >0:
            print("Gets called")            
            VOC_c =[{'x': rq, 'y': (1-self.calculate_efficiency(self.compound,rq,self.packing_height, self.capacity))*influent.extraneous['VOC'][self.compound]} for rq in Rq_space]
        else:
            VOC_c = [{'x': 0, 'y': 0} for rq in Rq_space]

        for h in range(len(heights)):
            intermediary =[]
            for k in Rq_space:
                p=1
                intermediary.append({'x': k, 'y':self.calculate_efficiency(self.compound,k,heights[h], self.capacity)})
            if h == len(heights)-1:
                height_charts['Werkpunt: '+ str(heights[h])]=intermediary
            else:
                height_charts[heights[h]] =intermediary  
            
        column_is_flooding = False
        try:
            dp_dry,dp_tot, h_tot ,F, flooding_factor= self.eng_stickl.operating_point(self.capacity, self.rq, self.diameter)
            if isinstance(dp_tot, complex):
                raise ValueError("dp_tot is a complex number.")
            if isinstance(h_tot, complex):
                raise ValueError("h_tot is a complex number.")
        except Exception as e:
            print(f"An error occurred : {e}")
            dp_dry,dp_tot, h_tot ,F, flooding_factor = 0, 0, 0, 0,0
            column_is_flooding = True
        
       
     

        return {
            'influent': {
                'pH': self.quality.influent.product.pH,
                'O2': self.quality.influent.product.total('O2', 'mg'),
                'CO2': self.quality.influent.product.total('CO2', 'mg'),
                'CH4': self.quality.influent.product.total('Mtg') * 16,
                
                
            },
            'effluent': {
                'pH': self.quality.effluent.product.pH,
                'O2': self.quality.effluent.product.total('O2', 'mg'),
                'CO2': self.quality.effluent.product.total('CO2', 'mg'),
                'CH4': self.quality.effluent.product.total('Mtg') * 16 
            },
            'model': {
                'F': F,
                'liquid_load': u_l*3600,
                'flooding_factor': flooding_factor*100,
                'liquid_holdup': h_tot*100,
                'pressure_drop': dp_tot/100,
            },
            'charts': {
                'flooding': flooding,
                'operating': operating,
                'working_point': werkpunt_hydro,
                'efficiency_height': height_charts,
                'efficiency_workpoint': werkpunt_quality,
                'column_is_flooding': column_is_flooding,
                'VOC_concentration': VOC_c,
                'VOC': influent.extraneous['VOC']
            }
        }



