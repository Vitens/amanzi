from .model import Model
from .submodels.splitter import Splitter
import pandas as pd


# Temporary database hardcoded untill implemented globally
MEMBRANES_DATABASE = { 
        "ESPA2-LD": {
          "name": "ESPA2-LD",
          "surface": 40,
          "size": "8x40 (inch * inch)",
          "retention": {
            "Na": 0.9, "Cl": 0.9, "Mg": 0.95, "Ca": 0.95}
        }
      }
membrane_specs =  {
        "nominal_flow": 27.3, #m3/day
        "salt_rejection": 99.7, # %
        "feed_flow_max": 17.0, #m3/h
        "dP_max_element": 1.0, # bar
        "flux_avg": 15., # L/m2h
        "A_e": 40.9, # m2
        "test_conditions": {
            "C_feed": 32000, # mg/L NaCl
            "P_feed": 55, # bar
            "recovery": 10, # %
            "temperature": 25, # C
        }
    }

osm_ratio = 0.08
OSM_SEAWATER_CONST = 0.01
class Membrane(Model, Splitter):
    def __init__(self, config, pp):
        super().__init__(config, pp)
        self.configuration = config.get('configuration', {})
        # self.configuration =  {
        #   "recovery": 0.8,
        #   "flux": 20,
        #   "stacks": 2,
        #   "stages": 3,
        #   "modules": 6,
        #   "vessels": [8, 5, 2],
        #   "membrane": "ESPA2-LD"
        # }        
        self.split = self.configuration.get('recovery', 0.8)
        self.membrane = self.configuration.get('membrane', 'ESPA2-LD')
        self.retention = MEMBRANES_DATABASE[self.membrane].get('retention', {'Na': 0.9, 'Cl': 0.9, 'Mg': 0.5, 'Ca': 0.5})
        self.pv_elements = self.configuration.get('modules', 6)
        self.membrane_surface = self.configuration.get('surface', 40)
        self.stage_config = list(self.configuration['vessels'].values())
        self.stages = self.configuration.get('stages', 3)
        
        self.concentrate = None
        self.stage_results = {}        

    def init_stack(self, total_inflow, Pf):
        for stage in range(self.stages):
            vessels = self.stage_config[stage]
            df = pd.DataFrame(index=range(self.pv_elements))

            df['stage'] = stage
            df['vessels'] = vessels
            df['dP_e'] = 0.2
            df['Qf_e'] = pd.Series(dtype='float64')
            df['Qc_e'] = pd.Series(dtype='float64')
            df['Qp_e'] = pd.Series(dtype='float64')    
            df['J_e'] = pd.Series(dtype='float64')        

            if stage == 0:
                # initialize first element of of first stage
                df.at[0, "Qf_e"] = total_inflow / vessels
                df.at[0, "Pf_e"] = Pf
                df.at[0, "Pc_e"] = Pf - df.at[0, "dP_e"]                
                df.at[0, "NDP_e"] = df.at[0, "Pc_e"] # - minus osmotic pressures                
                df.at[0, "Qp_e"] = df.at[0, "NDP_e"] * self.membrane_surface * self.k_w() / 1000
                df.at[0, "Qc_e"] = df.at[0, "Qf_e"] - df.at[0, "Qp_e"]
                df.at[0, "R_e"] = (df.at[0, "Qp_e"] / df.at[0, "Qf_e"])*100
                df.at[0, "J_e"] = df.at[0, "Qp_e"]*1000/self.membrane_surface

            else:
                # initialize first element based on previous stage            
                prev_df = self.stage_results[stage-1]
                df.at[0, "Qf_e"] = (prev_df.iloc[-1]["Qc_e"] * self.stage_config[stage-1]) / vessels
#                 df.at[0, "Pf_e"] = (prev_df.iloc[-1]["Pc_e"] * self.stage_config[stage-1]) / vessels                 
                df.at[0, "Pf_e"] = prev_df.iloc[-1]["Pc_e"]
                df.at[0, "Pc_e"] = df.at[0, "Pf_e"] - df.at[0, "dP_e"]               
                df.at[0, "NDP_e"] = prev_df.iloc[-1]["NDP_e"] - prev_df.iloc[-1]["dP_e"]
                df.at[0, "Qp_e"] = df.at[0, "NDP_e"] * self.membrane_surface * self.k_w() / 1000
                df.at[0, "Qc_e"] = df.at[0, "Qf_e"] - df.at[0, "Qp_e"]
                df.at[0, "R_e"] = (df.at[0, "Qp_e"] / df.at[0, "Qf_e"])*100
                df.at[0, "J_e"] = df.at[0, "Qp_e"]*1000/self.membrane_surface        


            # Derive subsequent rows (elements) from first row (element)
            for i, row in df.iterrows():
                if  i == 0:
                    continue
                df.at[i, "Qf_e"] = df.at[i-1, "Qc_e"]
                df.at[i, "Pf_e"] = df.at[i-1, "Pc_e"]
                df.at[i, "Pc_e"] = df.at[i, "Pf_e"] - df.at[i, "dP_e"]               
                df.at[i, "NDP_e"] = df.at[i-1, "NDP_e"] - df.at[i-1, "dP_e"]
                df.at[i, "Qp_e"] = df.at[i, "NDP_e"] * self.membrane_surface * self.k_w() / 1000
                df.at[i, "Qc_e"] = df.at[i, "Qf_e"] - df.at[i, "Qp_e"]
                df.at[i, "R_e"] = (df.at[i, "Qp_e"] / df.at[i, "Qf_e"])*100
                df.at[i, "J_e"] = df.at[i, "Qp_e"]*1000/self.membrane_surface


            df["Qp"] = df["Qp_e"] * vessels

            self.stage_results[stage] = df

        stack = pd.concat(self.stage_results.values())
        stack.index.name = 'element'
        stack = stack.reset_index()
        self.stack = stack.round(2)
        return stack
    
    def k_w(self, T=25, Tref=25):
        """Permeability coefficient (L/m2 bar h)"""      
        Q_test = membrane_specs['nominal_flow'] / 24
        SR = membrane_specs['salt_rejection']/100

        R_e_test = membrane_specs['test_conditions']['recovery']/100
        C_f_test = membrane_specs['test_conditions']['C_feed']
        P_f_test = membrane_specs['test_conditions']['P_feed']

        C_c_test = (C_f_test*(1-(R_e_test*(1-(SR))))/(1-(R_e_test)))

        osm_f_test = C_f_test * (osm_ratio/1000)
        osm_c_test = C_c_test * (osm_ratio/1000)
        osm_fc_test = (osm_f_test + osm_c_test)/2
        osm_p_test = OSM_SEAWATER_CONST * osm_fc_test
        d_osm_avg_test = osm_fc_test - osm_p_test
        P_p_test = 0
        
        dP_e = 0.2

        NDP_test = P_f_test - dP_e/2 - d_osm_avg_test - P_p_test

        J_test = Q_test*1000/self.membrane_surface
        K_w = J_test/NDP_test # [m3/m3 bar h]
        
        dT = T-Tref        
        K_w = K_w * (1+0.03*dT) # K_w changes 3% per degree (dT)
        return K_w
    
    @property
    def production(self):
        return self.stack["Qp"].sum()

    @property
    def recovery(self):
        Q_in = self.stack.iloc[0]["Qf_e"] * self.stack.iloc[0]["vessels"]
        return 100*(self.production/Q_in)
    
    @property
    def flux_avg(self):
        return self.stack['J_e'].mean()
        
    
    def solve_staging(self, total_inflow, Pf, target_R, tolerance=1, max_iterations=1000):
        stack = self.init_stack(total_inflow, Pf)
        iteration = 0

        while abs(self.recovery - target_R) > tolerance and iteration < max_iterations:
            diff = self.recovery - target_R
            Pf += 0.1 if diff < 0 else -0.1
            stack = self.init_stack(total_inflow, Pf)
            iteration += 1

        if iteration == max_iterations:
            print("Maximum iterations reached, desired recovery not achieved.")
        print(f"Solved in {iteration} iterations")
        return stack    
    
    @property
    def emitter_solutions(self):
        return {'waste': self.concentrate}

    def run_model(self, type, total_inflow, solution):
        permeate = solution.copy()
        ion_removal = {}

        ion_removal = {}
        for ion, ret in self.retention.items():
            ion_removal[ion] = solution.total(ion, 'mmol') * ret  * -0.99999
        
        permeate.change(ion_removal, 'mmol')

        # Calculate Concentrate:
        ion_removal.update((x, y*-1) for x, y in ion_removal.items())
        concentrate_composition = ion_removal
        # concentrate_composition.update({'-units': 'mmol/l', 'temp': 10})

        # #Rewrite HCO3 and SO4 in terms that PhreeqPython understands
        # concentrate_composition['Alkalinity'] = str(concentrate_composition['HCO3']) + " as HCO3"
        # concentrate_composition['S(6)'] = str(concentrate_composition['SO4']) + " as SO4"

        # #Delete dormant keys
        # del concentrate_composition['HCO3']
        # del concentrate_composition['SO4']
        
        #Create new concentrate solution
        self.concentrate = self.pp.add_solution_simple(concentrate_composition)

        return permeate

    def design(self):
        # print('design!', self.influent.pH)
        # print('vacuum', self.pressure)
        # print(self.configuration)
        print("Designin a Membrane")
        self.solve_staging(100, 10, 80)
        # effluent = self.run_model(None, None, self.influent)
        d = {
            "keys": self.stack.columns.tolist(),
            "data": self.stack.to_dict(orient='records')
        }
        return d
        # pressures = np.linspace(0.03, 1.0, 200)

        # ph_data = []
        # si_data = []
        # ch4_data = []
        # n2_data = []
        # co2_data = []
        # h2s_data = []
        # volumes = []
        # normal_volumes = []

        # for p in pressures:
        #     eff, gas = self.degass(self.influent, p)

        #     si_data.append({'x': p, 'y': eff.si('Calcite')})
        #     ph_data.append({'x': p, 'y': eff.pH})
        #     ch4_data.append({'x': p, 'y': eff.total('Mtg') * 16})
        #     n2_data.append({'x': p, 'y': eff.total('Ntg') * 28})
        #     co2_data.append({'x': p, 'y': eff.total('CO2','mg')})
        #     h2s_data.append({'x': p, 'y': eff.total('H2S','mg')})
        #     normal_volumes.append({'x': p, 'y': gas.volume*self.pressure})
        #     volumes.append({'x': p, 'y': gas.volume})

        # return {
        #     'summary' : {
        #         'surface_area': self.surface_area,
        #         },
        #     'influent': {
        #         'pH': self.influent.pH,
        #         'na': self.influent.total('Na'),
        #         'cl': self.influent.total('Cl'),
        #         'ca': self.influent.total('Ca','mg'),
        #         'mg': self.influent.total('Mg','mg'),
        #     },
        #     'effluent': {
        #         'pH': effluent.pH,
        #         'na': effluent.total('Na'),
        #         'cl': effluent.total('Cl'),
        #         'ca': effluent.total('Ca','mg'),
        #         'mg': effluent.total('Mg','mg'),
        #     },
        #     'concentrate': {
        #         'pH': self.concentrate.pH,
        #         'na': self.concentrate.total('Na'),
        #         'cl': self.concentrate.total('Cl'),
        #         'ca': self.concentrate.total('Ca','mg'),
        #         'mg': self.concentrate.total('Mg','mg'),
        #     },
        #     'flows': {
        #         1 : {
        #             'inlfuent' : 100,
        #             'effluent' : 100 * self.split,
        #             'concentrate' : 100 * (1 - self.split),
        #         },
        #         2 : {
        #             'inlfuent' : 100,
        #             'effluent' : 100 * self.split,
        #             'concentrate' : 100 * (1 - self.split),
        #         },
        #         3 : {
        #             'inlfuent' : 100,
        #             'effluent' : 100 * self.split,
        #             'concentrate' : 100 * (1 - self.split),
        #         },                
        #     },
        #     'pressures': {
        #         1 : {
        #             'inlfuent' : 100,
        #             'effluent' : 100 * self.split,
        #             'concentrate' : 100 * (1 - self.split),
        #         },
        #         2 : {
        #             'inlfuent' : 100,
        #             'effluent' : 100 * self.split,
        #             'concentrate' : 100 * (1 - self.split),
        #         },
        #         3 : {
        #             'inlfuent' : 100,
        #             'effluent' : 100 * self.split,
        #             'concentrate' : 100 * (1 - self.split),
        #         },                
        #     }
            # 'charts': {
            # 'pH': ph_data,
            # 'SI': si_data, 
            # 'ch4': ch4_data,
            # 'n2': n2_data,
            #     'co2': co2_data,
            #     'h2s': h2s_data,
            #     'normal_volume': normal_volumes,
            #     'volume': volumes,
            # }

        # }