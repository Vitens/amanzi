from .model import Model
from .submodels.splitter import Splitter
import pandas as pd
from scipy.optimize import minimize, minimize_scalar
import json
from phreeqpython import PhreeqPython

# Temporary database hardcoded untill implemented globally
# MEMBRANES_DATABASE = { 
#         "ESPA2-LD": {
#           "name": "ESPA2-LD",
#           "surface": 40,
#           "size": "8x40 (inch * inch)",
#           "retention": {
#             "Na": 0.9, "Cl": 0.9, "Mg": 0.95, "Ca": 0.95}
#         }
#       }
MEMBRANES_DATABASE =  {
        "ESPA2-LD": {
            "nominal_flow": 27.3, #m3/day
            "salt_rejection": 99.7, # %
            "retention": {"Na": 0.997, "Cl": 0.997},
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
    }

class Membrane(Model, Splitter):
    def __init__(self, config, pp):
        super().__init__(config, pp)
        self.configuration = config.get('configuration', {}) 
        self.split = self.configuration.get('recovery', 0.8)
        self.membrane = self.configuration.get('membrane', 'ESPA2-LD')
        self.membrane_config = MEMBRANES_DATABASE[self.membrane]
        self.retention = self.membrane_config.get('retention', {'Na': 0.996, 'Cl': 0.996, 'Mg': 0.999, 'Ca': 0.999})
        self.pv_elements = self.configuration.get('modules', 6)
        self.membrane_surface = self.configuration.get('surface', 40)
        self.stacks = self.configuration.get('stacks', 3)
        self.stack = None
        self.stages = self.configuration.get('stages', 3)
        self.stage_config = list(self.configuration['vessels'].values())
        self.stage_results = {}        
        
        self.spacer_height = 0.86e-3 # m
        self.element_length = 1 # m
        self.rho = 1000 # kg/m3
        self.porosity = 0.85 # RO-porosity = 0.8-0.85 (Vrouwenvelder, 2009)
        
        self.concentrate = None

    def velocity(self, Qf):
        total_spacer_width = (self.membrane_surface/self.element_length)/2
        A_effective = self.porosity * self.spacer_height * total_spacer_width
        return (Qf / A_effective) / 3600 # convert m/h to m/s

    def kinematic_viscostiy(self, T=25, T_ref=20):
        kin_v_ref = 1.004e-6 #m2/s
        # kin_v = kin_v_ref * ((T+273 + T_ref+273) / (T_ref+273)) * ((T+273 / T_ref+273))
        return kin_v_ref # kin_v not correct yet, assume kin_v_ref for now

    def head_loss(self, velocity):
        reynolds = velocity * self.spacer_height / self.kinematic_viscostiy(T=25)
        friction_factor = 6.23 * reynolds**-0.3 # p.195 of Water Treatment - Nanofiltration and reverse osmosis
        friction_factor = friction_factor if friction_factor > 0 else 0

        dP = friction_factor * self.element_length * self.rho * velocity**2 / (2 * self.spacer_height) #Pascal
        return dP*1e-5 # convert Pa to bar

    def init_stack(self, Pf):
        for stage in range(self.stages):
            vessels = self.stage_config[stage]
            df = pd.DataFrame(index=range(self.pv_elements))
            df['stage'] = stage
            df['vessels'] = vessels     

            if stage == 0:
                # initialize first element of of first stage
                df.at[0, "Qf_e"] = self.stack_inflow / vessels
                df.at[0, 'v_e'] = self.velocity(df.at[0, "Qf_e"])
                df.at[0, 'dP_e'] = self.head_loss(df.at[0, 'v_e'])
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
                df.at[0, 'v_e'] = self.velocity(df.at[0, "Qf_e"])
                df.at[0, 'dP_e'] = self.head_loss(df.at[0, 'v_e'])
                df.at[0, "Pf_e"] = prev_df.iloc[-1]["Pc_e"]
                df.at[0, "Pc_e"] = df.at[0, "Pf_e"] - df.at[0, "dP_e"]               
                df.at[0, "NDP_e"] = prev_df.iloc[-1]["NDP_e"] - prev_df.iloc[-1]["dP_e"]
                df.at[0, "Qp_e"] = df.at[0, "NDP_e"] * self.membrane_surface * self.k_w() / 1000
                df.at[0, "Qc_e"] = df.at[0, "Qf_e"] - df.at[0, "Qp_e"]
                df.at[0, "R_e"] = (df.at[0, "Qp_e"] / df.at[0, "Qf_e"])*100
                df.at[0, "J_e"] = df.at[0, "Qp_e"]*1000/self.membrane_surface  
                df.at[0, 'v_e'] = self.velocity(df.at[0, "Qf_e"])

            # Derive subsequent rows (elements) from first row (element)
            for i, row in df.iterrows():
                if  i == 0:
                    continue
                df.at[i, "Qf_e"] = df.at[i-1, "Qc_e"]
                df.at[i, 'v_e'] = self.velocity(df.at[i, "Qf_e"])
                df.at[i, 'dP_e'] = self.head_loss(df.at[i, 'v_e'])                
                df.at[i, "Pf_e"] = df.at[i-1, "Pc_e"]
                df.at[i, "Pc_e"] = df.at[i, "Pf_e"] - df.at[i, "dP_e"]               
                df.at[i, "NDP_e"] = df.at[i-1, "NDP_e"] - df.at[i-1, "dP_e"]
                df.at[i, "Qp_e"] = df.at[i, "NDP_e"] * self.membrane_surface * self.k_w() / 1000
                df.at[i, "Qc_e"] = df.at[i, "Qf_e"] - df.at[i, "Qp_e"]
                df.at[i, "R_e"] = (df.at[i, "Qp_e"] / df.at[i, "Qf_e"])*100
                df.at[i, "J_e"] = df.at[i, "Qp_e"]*1000/self.membrane_surface
                df.at[i, 'v_e'] = self.velocity(df.at[i, "Qf_e"])


            df["Qp"] = df["Qp_e"] * vessels
            df.index.name = 'element'
            df.reset_index(inplace=True)
            df = df.round(2)
            df['stage'] = df['stage'] + 1
            df['element'] = df['element'] + 1
            self.stage_results[stage] = df

        self.stack = pd.concat(self.stage_results.values())
        # return self.stack
    
    def k_w(self, T=25, Tref=25):
        """Permeability coefficient (L/m2 bar h)"""      
        Q_test = self.membrane_config['nominal_flow'] / 24
        SR = self.membrane_config['salt_rejection']/100

        OSM_RATIO = 0.08
        OSM_SEAWATER_CONST = 0.01

        R_e_test = self.membrane_config['test_conditions']['recovery']/100
        C_f_test = self.membrane_config['test_conditions']['C_feed']
        P_f_test = self.membrane_config['test_conditions']['P_feed']

        C_c_test = (C_f_test*(1-(R_e_test*(1-SR)))/(1-(R_e_test)))

        osm_f_test = C_f_test * (OSM_RATIO/1000)
        osm_c_test = C_c_test * (OSM_RATIO/1000)
        osm_fc_test = (osm_f_test + osm_c_test)/2
        osm_p_test = OSM_SEAWATER_CONST * osm_fc_test
        d_osm_avg_test = osm_fc_test - osm_p_test
        P_p_test = 0

        test_velocity = self.velocity(Q_test)
        dP_e = self.head_loss(test_velocity)

        NDP_test = P_f_test - dP_e/2 - d_osm_avg_test - P_p_test

        J_test = Q_test*1000/self.membrane_surface
        K_w = J_test/NDP_test # [m3/m3 bar h]
        
        dT = T-Tref        
        K_w = K_w * (1 + 0.03 * dT) # K_w changes 3% per degree (dT)
        return K_w
 
    
    @property
    def recovery(self):
        Q_p = self.stack["Qp"].sum()
        return (Q_p/self.stack_inflow)*100

    @property
    def stack_inflow(self):
        total_inflow = self.inflows['product'] * 1e6 / (365*24) # convert Mm3/year to m3/h
        return total_inflow / self.stacks

    def solve_staging(self, Pf, tolerance=1):
        target_R = self.split * 100
        def recovery_difference(Pf):
            self.init_stack(Pf)
            return abs(self.recovery - target_R)

        result = minimize(recovery_difference, x0=Pf, method='Nelder-Mead', options={"fatol":tolerance})        
        best_Pf = result.x
        self.init_stack(best_Pf)    
        iterations = result.nfev  # The number of function evaluations used by the optimization algorithm  

        if abs(self.recovery - target_R) > tolerance:
            print("Tolerance exceeded, desired recovery not achieved, but approached.")
        else:
            print(f"Solved in {iterations} iterations")

    def solve_staging_qualities(self):
        def solve_qualities(feed, R):
            permeate_composition = {}
            concentrate_composition = {}
            for el, val in feed.species.items():
                ret = self.retention.get(el, 0.999)
                permeate_composition[el] = val * (1-ret) * 1e3
                concentrate_composition[el] = val * (1-(R/100)*(1-ret)) / (1-(R/100)) * 1e3
            permeate = self.pp.add_solution_simple(permeate_composition, 'mol')
            concentrate = self.pp.add_solution_simple(concentrate_composition, 'mol')
            return concentrate.copy(), permeate.copy()

        qualities = {}
        for s, df in self.stage_results.items():
            qualities[s] = {'Cf_e': [], 'Cc_e': [], 'Cp_e': []}
            for index, stage_row in df.iterrows():
                if index == 0 and s == 0:
                    R = stage_row['R_e']
                    Cf_e = self.influent.copy()
                    qualities[s]['Cf_e'].append(Cf_e)
                elif index == 0 and s > 0:
                    R = stage_row['R_e']
                    Cf_e = qualities[s-1]['Cc_e'][-1]
                    qualities[s]['Cf_e'].append(Cf_e)
                else:
                    R = stage_row['R_e']
                    Cf_e = qualities[s]['Cc_e'][-1]                    
                    qualities[s]['Cf_e'].append(Cf_e)
       
                Cc_e, Cp_e = solve_qualities(Cf_e, R)
                qualities[s]['Cc_e'].append(Cc_e)
                qualities[s]['Cp_e'].append(Cp_e)

            for key, ls in qualities[s].items():
                self.stage_results[s][f"π_{key}"] = pd.Series([l.osmotic_pressure for l in ls])
                self.stage_results[s][key] = pd.Series([l.total('Ca', 'mg') for l in ls])

            self.stage_results[s][f"π_fc_e"] = (self.stage_results[s]["π_Cf_e"] + self.stage_results[s]["π_Cc_e"])/2
            self.stage_results[s] = self.stage_results[s].round(2)
        
        self.qualities = qualities
        self.stack = pd.concat(self.stage_results.values())        

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

    @property
    def stream_species(self):
        species = {}
        for stage, streams in self.qualities.items():
            species[stage] = {}
            for stream, sols in streams.items():
                species[stage][stream] = [s.species for s in sols]
        return species

    @property
    def stream_elements(self):
        species = {}
        for stage, streams in self.qualities.items():
            species[stage] = {}
            for stream, sols in streams.items():
                species[stage][stream] = [s.elements for s in sols]
        return species

    def generate_chart_data(self, col1, col2):
        datasets = []
        for s, df in self.stage_results.items():
            data = dict(zip(df[col1], df[col2]))
            dataset = {
                "label": f"Stage {s+1}",
                "data": data
            }
            datasets.append(dataset)

        return datasets
    
    @property
    def overview(self):
        control_volums = {}
        for s, data in self.stage_results.items():
            control_volums[s] = {
                "Qf": self.stack_inflow if s == 0 else data.iloc[0]['Qf_e'],
                "Pf": data.iloc[0]['Pf_e'],
                "EGVf": self.qualities[s]['Cf_e'][0].sc20 / 10,
                "Qc": data.iloc[-1]['Qc_e'] * self.stage_config[s],
                "Pc": data.iloc[-1]['Pc_e'],
                "EGVc": self.qualities[s]['Cc_e'][-1].sc20 / 10,
                "Qp": data['Qp_e'].sum() * self.stage_config[s],
                "Pp": 0,
                "EGVp": self.qualities[s]['Cp_e'][-1].sc20 / 10
            }
        return control_volums

    @property
    def d_influent(self):        
        return self.qualities[0]['Cf_e'][0]
    
    @property
    def d_concentrate(self):        
        s = max(self.qualities.keys())
        return self.qualities[s]['Cc_e'][-1]
    
    @property
    def d_permeate(self):
        permeate_mixture = {}
        for s in self.stage_results.keys():
            p_sols = self.qualities[s]['Cp_e']
            p_flows = self.stage_results[s]['Qp_e'].tolist()
            p_total = sum(p_flows)

            mixture = {sol:flow/p_total for sol, flow in zip(p_sols, p_flows)}
            int_permeate = self.pp.mix_solutions(mixture)
            permeate_mixture[int_permeate] = p_total
        return self.pp.mix_solutions(permeate_mixture)



    def design(self):
        print("Designin a Membrane")
        #use test pressure to start iteration
        P_f_test = self.membrane_config['test_conditions']['P_feed'] 
        self.solve_staging(P_f_test)
        self.solve_staging_qualities()
        
        d = {
            "MEMBRANE_DB": list(MEMBRANES_DATABASE.keys()),
            "keys": self.stack.columns.tolist(),
            "data": self.stack.to_dict(orient='records'),
            "overview": self.overview,
            "results": {
                "Qf": self.stack_inflow,
                "Cf": self.stack.iloc[0]["Cf_e"],
                "Qc": self.stage_results[list(self.stage_results.keys())[-1]]["Qc_e"].sum(),
                "Cc": 0, #use pp.mix_solutions to mix all outgoing concentrate streams of the latest stage with their weight,
                "Qp": self.stack["Qp"].sum(),
                "Cp": 0, #use pp.mix_solutions to mix all outgoing permeate streams with their weight,
                "recovery": self.recovery,
                "flux_avg": self.stack['J_e'].mean()
                },
            'keys2': self.stage_results[0].columns.tolist(),
            'stage_results': pd.concat([df for df in self.stage_results.values()]).to_dict(orient='records'),
            'stage_species': self.stream_species,
            'stage_elements': self.stream_elements,
            'charts': {
                "recovery": self.generate_chart_data('element', 'R_e'),
                "flux_rec": self.generate_chart_data('R_e','J_e'),
                "head_loss": self.generate_chart_data('element','dP_e'),
                "stage_flows": self.generate_chart_data('element','Qf_e'),
                "stage_conc": self.generate_chart_data('element','Cf_e'),
                "osmotic_avg": self.generate_chart_data('element','π_fc_e'),
            },
            'influent': {
                'pH': self.d_influent.pH,
                'egv': self.d_influent.sc20/10,
                'na': self.d_influent.total('Na', 'mg'),
                'cl': self.d_influent.total('Cl', 'mg'),
                'ca': self.d_influent.total('Ca','mg'),
                'mg': self.d_influent.total('Mg','mg'),
            },
            'effluent': {
                'pH': self.d_permeate.pH,
                'egv': self.d_permeate.sc20/10,
                'na': self.d_permeate.total('Na', 'mg'),
                'cl': self.d_permeate.total('Cl', 'mg'),
                'ca': self.d_permeate.total('Ca','mg'),
                'mg': self.d_permeate.total('Mg','mg'),
            },
            'concentrate': {
                'pH': self.d_concentrate.pH,
                'egv': self.d_concentrate.sc20/10,
                'na': self.d_concentrate.total('Na', 'mg'),
                'cl': self.d_concentrate.total('Cl', 'mg'),
                'ca': self.d_concentrate.total('Ca','mg'),
                'mg': self.d_concentrate.total('Mg','mg'),
            },        
        }
        return d