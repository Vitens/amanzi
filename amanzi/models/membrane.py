from .model import Model
from .submodels.splitter import Splitter
import pandas as pd
from scipy.optimize import minimize, minimize_scalar
import numpy as np
import json
from phreeqpython import PhreeqPython, Solution
from ..assets.membranes import MEMBRANE_DB

KP = 0.99 #Hydraunotics constant for permeate flux (p. 258 from https://www.researchgate.net/publication/351606477)

class Membrane(Model, Splitter):
    def __init__(self, config, pp):
        super().__init__(config, pp)
        self.configuration = config.get('configuration', {}) 
        self.split = self.configuration.get('recovery', 0.8)
        self.capacity = self.configuration.get('capacity', 300)

        self.membrane = self.configuration.get('membrane', 'ESPA2-LD')
        self.membrane_config = MEMBRANE_DB[self.membrane]
        self.retention = self.membrane_config.get('retention', {'Na': 0.996, 'Cl': 0.996, 'Mg': 0.999, 'Ca': 0.999})
        self.membrane_surface = self.membrane_config.get('A_e', 40)
        self.optiflux = self.configuration.get('optiflux', False)

        # self.modules = self.configuration.get('modules', 6)
        self.stacks = self.configuration.get('stacks', 3)
        self.stages = self.configuration.get('stages', 3)
        # self.vessel_config = list(self.configuration['vessels'].values())
        
        self.stack = None
        # self.concentrate = None
        self.stage_results = {}      
        self.ready = False    

        self.qualities = {}
        
        self.spacer_height = 0.86e-3 # m
        self.element_length = 1 # m
        self.rho = 1000 # kg/m3
        self.porosity = 0.85 # RO-porosity = 0.8-0.85 (Vrouwenvelder, 2009)
        print("OPTIFLUX =", self.optiflux)
        

    @property
    def vessel_config(self):
        if self.optiflux:
            return [x*2 for x in list(self.configuration['vessels'].values())]
        else:
            return list(self.configuration['vessels'].values())

    @property
    def modules(self):
        modules = self.configuration.get('modules', 6)/2 if self.optiflux else self.configuration.get('modules', 6)
        return int(modules)


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
    


    def init_stack(self, Pf):
        for stage in range(self.stages):
            df = pd.DataFrame(index=range(self.modules))
            df['stage'] = stage

            vessels = self.vessel_config[stage]
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
                df.at[0, "Qf_e"] = (prev_df.iloc[-1]["Qc_e"] * self.vessel_config[stage-1]) / vessels
                df.at[0, 'v_e'] = self.velocity(df.at[0, "Qf_e"])
                df.at[0, 'dP_e'] = self.head_loss(df.at[0, 'v_e'])
                df.at[0, "Pf_e"] = prev_df.iloc[-1]["Pc_e"]
                df.at[0, "Pc_e"] = df.at[0, "Pf_e"] - df.at[0, "dP_e"]               
                df.at[0, "NDP_e"] = prev_df.iloc[-1]["NDP_e"] - prev_df.iloc[-1]["dP_e"]
                df.at[0, "Qp_e"] = df.at[0, "NDP_e"] * self.membrane_surface * self.k_w() / 1000
                df.at[0, "Qc_e"] = df.at[0, "Qf_e"] - df.at[0, "Qp_e"]
                df.at[0, "R_e"] = (df.at[0, "Qp_e"] / df.at[0, "Qf_e"])*100
                df.at[0, "J_e"] = df.at[0, "Qp_e"]*1000/self.membrane_surface  
                # df.at[0, 'v_e'] = self.velocity(df.at[0, "Qf_e"])

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
                # df.at[i, 'v_e'] = self.velocity(df.at[i, "Qf_e"])


            df["Qp"] = df["Qp_e"] * vessels
            df.index.name = 'element'
            df.reset_index(inplace=True)
            df = df.round(2)
            df['stage'] = df['stage'] + 1
            df['element'] = df['element'] + 1
            self.stage_results[stage] = df

        self.stack = pd.concat(self.stage_results.values())
        # return self.stack

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
        def solve_qualities(influent, R):
            permeate_composition = {}
            concentrate_composition = {}
            for el, val in influent.species.items():
                ret = self.retention.get(el, 0.999)
                permeate_composition[el] = val * (1-ret) * 1e3
                concentrate_composition[el] = val * (1-(R/100)*(1-ret)) / (1-(R/100)) * 1e3
            permeate = self.pp.add_solution_simple(permeate_composition, 'mol')
            concentrate = self.pp.add_solution_simple(concentrate_composition, 'mol')
            return concentrate.copy(), permeate.copy()

        qualities = {}
        for s, df in self.stage_results.items():
            qualities[s] = {'influent': [], 'concentrate': [], 'permeate': []}
            for index, stage_row in df.iterrows():
                if index == 0 and s == 0:
                    # R = stage_row['R_e']
                    Cf_e = self.influent.copy()
                    qualities[s]['influent'].append(Cf_e)
                elif index == 0 and s > 0:
                    # R = stage_row['R_e']
                    Cf_e = qualities[s-1]['concentrate'][-1]
                    qualities[s]['influent'].append(Cf_e)
                else:
                    Cf_e = qualities[s]['concentrate'][-1]                    
                    qualities[s]['influent'].append(Cf_e)
       
                R = stage_row['R_e']
                conc, perm = solve_qualities(Cf_e, R)
                qualities[s]['concentrate'].append(conc)
                qualities[s]['permeate'].append(perm)

            for key, ls in qualities[s].items():
                self.stage_results[s][f"π_{key}"] = pd.Series([l.osmotic_pressure for l in ls])
                # self.stage_results[s][key] = pd.Series([l.total('Ca', 'mg') for l in ls])

            self.stage_results[s][f"π_mean"] = (self.stage_results[s]["π_influent"] + self.stage_results[s]["π_concentrate"])/2
            # self.stage_results[s][f"Beta"] = self.stage_results[s]["π_concentrate"] / self.stage_results[s]["π_influent"]
            # self.stage_results[s][f"Beta_mean"] = self.stage_results[s]["π_mean"] / self.stage_results[s]["Q"]
            self.stage_results[s]["Qfc_e"] = (self.stage_results[s]["Qc_e"] + self.stage_results[s]["Qf_e"])/2
            self.stage_results[s]["Beta"] = KP * np.exp( self.stage_results[s]["Qp_e"] / self.stage_results[s]["Qfc_e"])
            self.stage_results[s] = self.stage_results[s].round(2)
        
        self.qualities = qualities
        self.stack = pd.concat(self.stage_results.values())   
        self.ready = True     

    @property
    def emitter_solutions(self):
        return {'waste': self.concentrate}

    def run_model(self, type, total_inflow, solution):
        specsheet_pressure = self.membrane_config['test_conditions']['P_feed'] #use test pressure to start iteration
        self.solve_staging(specsheet_pressure)
        self.solve_staging_qualities()

        return self.permeate
    
    @property
    def concentrate(self):
        return self.get_solution('concentrate') if len(self.qualities) else None

    @property
    def permeate(self):
        return self.get_solution('permeate') if len(self.qualities) else None

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

    # def generate_chart_data(self, *cols):
    #     datasets = []
    #     for s, df in self.stage_results.items():
    #         data = {}
    #         for col in cols:
    #             data[col] = df[col].tolist()
    #         dataset = {
    #             "label": f"Stage {s+1}",
    #             "data": data
    #         }
    #         datasets.append(dataset)
    #     return datasets
      
    # @property
    # def stack_quantities(self):
    #     d = {
    #         "influent": self.stack_inflow,
    #         "concentrate": self.stack.iloc[-1]["Qc_e"] * self.vessel_config[-1],
    #         "permeate": sum([data['Qp'] for s, data in self.stage_quantities.items()])
    #     }
    #     return d

    @property
    def stack_quantities(self):
        qp = sum([data['Qp'] for s, data in self.stage_quantities.items()])
        d = {
            "Qf": self.stack_inflow,
            "Qc": self.stack.iloc[-1]['Qc_e'] * self.vessel_config[-1],
            "Qp": qp,
            "Pf": self.stack.iloc[0]['Pf_e'],
            "Pc": self.stack.iloc[-1]['Pc_e'],
            "Pp": 0,
            "dP_mean": self.stack['dP_e'].mean(),
            "dP_max": self.stack['dP_e'].max(),            
            "recovery": 100 * qp/self.stack_inflow,
            "flux_mean": self.stack['J_e'].mean(),
            "flux_max": self.stack['J_e'].max()                
        }
        return d
    
    @property
    def stage_quantities(self):
        d = {}
        qp_summed = 0
        for s, data in self.stage_results.items():
            qf = self.stack_inflow if s == 0 else data.iloc[0]['Qf_e'] * self.vessel_config[s]
            qp = (data['Qp_e'] * self.vessel_config[s]).sum()
            qp_summed += qp
            # print(s, qp_summed)
            d[s] = {
                "Qf": qf,
                "Qc": data.iloc[-1]['Qc_e'] * self.vessel_config[s],
                "Qp": qp,
                "Pf": data.iloc[0]['Pf_e'],
                "Pc": data.iloc[-1]['Pc_e'],
                "Pp": 0,
                "dP_mean": data['dP_e'].mean(),
                "dP_max": data['dP_e'].max(),
                "recovery": round(100 * qp/qf, 0),
                "flux_mean": data['J_e'].mean(),
                "flux_max": data['J_e'].max(),
            }
        return d 
    
    def get_solution(self, stream, stage=None, module=None):
        """
        Get the solution-elements for any stream.
        If no stage or module is specified, the solution for the entire stack is returned.
        """
        if stage and not module:
            return self.stage_solutions[stage][stream]
        elif stage and module:
            return self.module_solutions[stage][stream][module]
        elif not stage and module:
            raise Exception("Module solution requested without stage specification.")
        else:
            return self.stack_solutions[stream]     

    def _serialize_solution(self, data):
        if isinstance(data, dict):
            new_dict = {}
            for key, value in data.items():
                new_value = self._serialize_solution(value)
                new_dict[key] = new_value
            return new_dict
        elif isinstance(data, list):
            return [self._solution_elements(sol) for sol in data]        
        elif isinstance(data, Solution):
            return self._solution_elements(data)
        else:
            return data
        
    def _solution_elements(self, solution):
        elements = {}
        for element, mass_fraction in solution.elements.items():
            # Extract the element name by ignoring the parenthesis part enables correct handling of redox states
            element_name = element.split('(')[0]
            try:
                elements[element_name] = round(solution.total(element_name, 'mg'), 1)
            except:
                # print("Membrane failed to process element:", element_name)
                pass
                # elements[element_name] = elements.get(element_name, 0) + mass_fraction * 1e3 #convert to mmol.
                # elements[element_name] = round(elements[element_name], 2)

        # add misc parameters
        elements['Hardheid'] = round(solution.hardness, 2)
        elements['pH'] = round(solution.pH, 2)
        elements['EGV'] = round(solution.sc20/10, 2)
        elements['TDS'] = round(solution.tds, 2)

        return elements
    
    @property
    def stack_solutions(self):
        # aggregate solutions based on scope (overview, stages, or modules)
        d = {}
        d['influent'] = self.qualities[0]['influent'][0]      
        d['concentrate'] = self.qualities[self.stages-1]['concentrate'][-1]
        permeate_mixture = {}
        for s in self.stage_results.keys():
            p_sols = self.qualities[s]['permeate']
            p_flows = self.stage_results[s]['Qp_e'].tolist()
            p_total = sum(p_flows)

            mixture = {sol:flow/p_total for sol, flow in zip(p_sols, p_flows)}
            int_permeate = self.pp.mix_solutions(mixture)
            permeate_mixture[int_permeate] = p_total
        d['permeate'] = self.pp.mix_solutions(permeate_mixture)
        return d
    
    @property
    def stage_solutions(self):
        # aggregate solutions based on scope (overview, stages or modules)
        d = {}
        for stage, streamsol in self.qualities.items():
            d[stage] = {}
            d[stage]['influent'] = streamsol['influent'][0]
            d[stage]['concentrate'] = streamsol['concentrate'][-1]
            p_sols = streamsol['permeate']
            p_flows = self.stage_results[stage]['Qp_e'].tolist()
            mixture = {sol:flow/sum(p_flows) for sol, flow in zip(p_sols, p_flows)}
            d[stage]['permeate'] = self.pp.mix_solutions(mixture)
        return d
    
    @property
    def module_solutions(self):
        solutions = {}
        for s, streamdata in self.qualities.items():
            solutions[s] = {}
            for stream, sols in streamdata.items():
                solutions[s][stream] = sols    
        return solutions

    @property
    def stack_inflow(self):
        return self.capacity / self.split 

    @property
    def mass_balance_inflow(self):
        total_inflow = self.inflows['product'] * 1e6 / (365*24) # convert Mm3/year to m3/h
        return total_inflow / self.stacks
    
    @property
    def recovery(self):
        return 100 * self.stack_quantities['Qp'] / self.stack_quantities['Qf']

    @property
    def summary_table(self):
        #Combine stage & stack data
        data = self.stage_quantities.copy()
        data['total'] = self.stack_quantities.copy()
        df = pd.DataFrame(data).round(1)

        #Format data to table-dict
        df['Eenheid'] = ['m3/h','m3/h','m3/h','bar','bar','bar','bar','bar', '%', 'l/m2h', 'l/m2h']
        df.reset_index(inplace=True)
        
        cols = ['']
        stage_names = [f"Stage {s+1}" for s in range(self.stages)]
        cols.extend(stage_names)
        cols.extend(['Stack Total','Eenheid'])
        df.columns = cols

        #Add membrane-specific thresholds
        # qf_max = self.membrane_config['Qf_max']
        # qc_min = self.membrane_config['Qc_min']
        # nominal = round(self.membrane_config['nominal_flow']/24,1)
        # p_max = self.membrane_config['P_max']
        # dp_max = self.membrane_config['dP_max']
        # df['Limiet'] = [f"< {qf_max}", f"> {qc_min}", f"< {nominal}", f"< {p_max}", '-','-',f"< {dp_max}", f"< {dp_max}", '-', '-','-']
                    
        return df.to_dict(orient='records')
    
    def design(self):
        print("Designing a Membrane")
        self.run_model(None, None, None)
        
        d = {
            #parameters
            "recovery" : self.recovery,
            "membranes": list(MEMBRANE_DB.keys()),
            'table': self.stack.to_dict(orient='records'),
            "summary_table": self.summary_table,
            
            #solutions per scope-level
            "stack_solutions": self._serialize_solution(self.stack_solutions),
            "stage_solutions": self._serialize_solution(self.stage_solutions),
            "module_solutions": self._serialize_solution(self.module_solutions),

            #quantities per scope-level (flow & pressure)
            "stack_quantities": self.stack_quantities,
            "stage_quantities": self.stage_quantities,


            'charts': {
                # "pressure": self.pressure_chart('element', 'Pf_e', 'Pc_e', 'Pp_e'),
                "recovery": self.generate_chart_data('element', 'R_e'),
                "flux": self.generate_chart_data('element','J_e'),
                "flux_rec": self.generate_chart_data('R_e','J_e'),
                "feed_pressure": self.generate_chart_data('element','Pf_e'),
                "head_loss": self.generate_chart_data('element','dP_e'),
                "stage_flows": self.generate_chart_data('element','Qf_e'),
                "osmotic_avg": self.generate_chart_data('element','π_mean'),
                "beta": self.generate_chart_data('element','Beta'),
            },   
        }
        return d