from cadet import Cadet

import subprocess
import os

from pathlib import Path 
# python numeric library
import numpy as np

# pandas is python library for data analysis
import pandas as pd

# addict is a library that makes it easier to create nested dictionaries
from addict import Dict

import tempfile
tempfile.tempdir = os.path.join(Path.home())
import platform
from pathlib import Path
from cadet import Cadet

#"Change path directions for Freundlichen Binary"

cadet_bin_path = Path(r'C:\Users\ZickermannN\AppData\Local\anaconda3\pkgs\cadet-4.4.0-hdf1ca3b_1\bin')
if platform.system() == 'Windows':   
    cadet_path = cadet_bin_path / "cadet-cli.exe"  #"D:/Program Files (x86)/Freundlich_isotherm/Pre_build_binaries/bin/cadet-cli.exe", "D:/Program Files (x86)/cadet/bin/cadet-cli.exe"
    lwe_path = cadet_bin_path / "createLWE.exe"   #"D:/Program Files (x86)/Freundlich_isotherm/Pre_build_binaries/bin/createLWE.exe"
   
   
else:
    cadet_path = cadet_bin_path / "cadet-cli"
    lwe_path = cadet_bin_path / "createLWE"

if cadet_path.exists() and lwe_path.exists():
    Cadet.cadet_path = cadet_path.as_posix()
    print("All good")
elif cadet_path.exists() and not lwe_path.exists():
    print("CADET was found but createLWE.exe was not found. Please make sure that none of the files have been moved.")
else:
    print("CADET could not be found. Please check the bin path")
#Cadet.cadet_path= 'C:\Users\ZickermannN\AppData\Local\anaconda3\pkgs\cadet-4.3.0-hbe8a693_3\bin\cadet-cli.exe'
#Cadet.lwe_path = 'C:\Users\ZickermannN\AppData\Local\anaconda3\pkgs\cadet-4.3.0-hbe8a693_3\bin\createlwe.exe'

class CADETMODEL():
    def __init__(self):
        self.model = None
        self.root = None
        self.filename = None

    def get_cadet_template(self,n_units=3, split_components_data=False):
        cadet_template = Cadet()
        
        cadet_template.root.input.model.nunits = n_units
        
        # Store solution
        cadet_template.root.input['return'].split_components_data = False #getestet für n_comp ist True and false gleich
        cadet_template.root.input['return'].split_ports_data = 0
        cadet_template.root.input['return'].write_solution_last = True
        cadet_template.root.input['return'].unit_000.write_solution_inlet = 1 #1
        cadet_template.root.input['return'].unit_000.write_solution_outlet = 1
        cadet_template.root.input['return'].unit_000.write_solution_bulk = 1 #1
        cadet_template.root.input['return'].unit_000.write_solution_particle = 1 #1
        cadet_template.root.input['return'].unit_000.write_solution_solid = 1
        cadet_template.root.input['return'].unit_000.write_solution_flux = 1 #1
        cadet_template.root.input['return'].unit_000.write_solution_volume = 1
        cadet_template.root.input['return'].unit_000.write_coordinates = 1
        cadet_template.root.input['return'].unit_000.write_sens_outlet = 1
        
        for unit in range(n_units):
            cadet_template.root.input['return']['unit_{0:03d}'.format(unit)] = cadet_template.root.input['return'].unit_000
            
        # Tolerances for the time integrator                           # Settings that worked previously:   
        cadet_template.root.input.solver.time_integrator.abstol = 1e-7 # previous 1e-6  ; 1e-11
        cadet_template.root.input.solver.time_integrator.algtol = 1e-11# previous 1e-10 ; 1e-14 
        cadet_template.root.input.solver.time_integrator.reltol = 1e-7 # previous 1e-6  ; 1e-11
        cadet_template.root.input.solver.time_integrator.init_step_size = 1e-10 #vpreviously 1e-6 ; 1e-10
        cadet_template.root.input.solver.time_integrator.max_steps = 1000000
        
        # Solver settings
        cadet_template.root.input.model.solver.gs_type = 1
        cadet_template.root.input.model.solver.max_krylov = 0
        cadet_template.root.input.model.solver.max_restarts = 10
        cadet_template.root.input.model.solver.schur_safety = 1e-8

        # Run the simulation on single thread
        cadet_template.root.input.solver.nthreads = 5
        
        return cadet_template 

    def set_discretization(self,model, n_bound=None, n_col=100):
        columns = {'GENERAL_RATE_MODEL', 'LUMPED_RATE_MODEL_WITH_PORES', 'LUMPED_RATE_MODEL_WITHOUT_PORES'}
        
        
        for unit_name, unit in model.root.input.model.items():
            if 'unit_' in unit_name and unit.unit_type in columns:
                unit.discretization.ncol = n_col
                unit.discretization.npar = 5 # discretization resolution of the particle
                
                if n_bound is None:
                    n_bound = unit.ncomp*[0]
                unit.discretization.nbound = n_bound
                
                unit.discretization.par_disc_type = 'EQUIDISTANT_PAR'
                unit.discretization.use_analytic_jacobian = 1
                unit.discretization.reconstruction = 'WENO'
                unit.discretization.gs_type = 1
                unit.discretization.max_krylov = 0
                unit.discretization.max_restarts = 10
                unit.discretization.schur_safety = 1.0e-8

                unit.discretization.weno.boundary_model = 0
                unit.discretization.weno.weno_eps = 1e-10
                unit.discretization.weno.weno_order = 1 

    def run_simulation(self,cadet, file_name=None):
        f = next(tempfile._get_candidate_names())
        file = os.path.join(tempfile.tempdir, f + '.h5')
        
        cadet.filename = file

        # save the simulation
        cadet.save()

        # run the simulation
        data = cadet.run()

        if data.returncode == 0:
            print("Simulation completed successfully")
            cadet.load()   
        else:
            print(data)
            raise Exception("Simulation failed")

        if file_name is not None:
            cadet.filename = file_name

            # save the simulation
            cadet.save()
        else:
            os.remove(file)
                
        return cadet
    
    def create_column_bB_GRM_AFR(self, t_in_seconds, c_feed,  resolution, volume_flow_rate, height, crosssection, filmdiffusion,freundlich_k, freundlich_n ):
        
        t_in_minutes = t_in_seconds / 60
        t_in_hours = t_in_minutes / 60
        
        n_comp = len(c_feed)                               
        n_col=100
        n_bound=[1]
        n_partype=1
        velocity = volume_flow_rate / crosssection
        print(velocity)
        model = self.get_cadet_template()
        
        
        #########################################  INLET  ###########################################################
        model.root.input.model.unit_000.unit_type = 'INLET'
        model.root.input.model.unit_000.ncomp = n_comp                     
        model.root.input.model.unit_000.inlet_type = 'PIECEWISE_CUBIC_POLY'
        
        model.root.input.model.unit_000.sec_000.const_coeff = c_feed               # mol/m^3

        ####################################  Column  ################################################################
        model.root.input.model.unit_001.unit_type = 'LUMPED_RATE_MODEL_WITHOUT_PORES'        
        model.root.input.model.unit_001.ncomp = n_comp               
        model.root.input.model.unit_001.col_length = height                           # m      Pit: 2.1
        model.root.input.model.unit_001.total_porosity = 0.45                       #        Pit: 0.45       
        model.root.input.model.unit_001.cross_section_area = crosssection                # m^2    Pit: 0.046
        model.root.input.model.unit_001.velocity = velocity                        # m/s  Pit: 2.28e-3      #3.25e-3
        model.root.input.model.unit_001.col_dispersion = n_comp*[0]                # m^2/s  Aumeier:
        model.root.input.model.unit_001.init_c = n_comp * [0]                      # mol/m^3 
        model.root.input.model.unit_001.init_q = n_comp *[0]                       
        
        
        ##################################Particles###################################################################
        
        model.root.input.model.unit_001.film_diffusion =[filmdiffusion]                          # m/s
        model.root.input.model.unit_001.film_diffusion_multiplex = 0  
        model.root.input.model.unit_001.par_porosity = 0.5                           # Pitt: 0.49
        model.root.input.model.unit_001.par_radius = 5.5e-4                          # [5.5e-4,4.5e-4,3.5e-4,2.5e-4,1.5e-4]  # m   beachte RADIUS!!!!! Pitt d=1.1mm --> 0,55mm

        
        
        ###################################  Adsorption  ###############################################################
        adsorption_parameters = Dict()
        adsorption_parameters.is_kinetic = 1
        adsorption_parameters.FLDF_KKIN = [filmdiffusion]                  
        adsorption_parameters.FLDF_KF = [freundlich_k]             
        adsorption_parameters.FLDF_N = [freundlich_n] 
        model.root.input.model.unit_001.adsorption_model = 'FREUNDLICH_LDF'         
        model.root.input.model.unit_001.adsorption = adsorption_parameters    
        
        
        model.root.input.model.unit_001.reaction_model_particles = 'MASS_ACTION_LAW'
        model.root.input.model.unit_001.reaction_particle.MAL_KFWD_liquid = [0.00739]
   

        model.root.input.model.unit_001.reaction_particle.MAL_KBWD_liquid = 0

   
        model.root.input.model.unit_001.reaction_particle.MAL_STOICHIOMETRY_liquid = [-1]    

        ###################################  Discretization  #############################################################
        
        self.set_discretization(model, n_bound)
        
        model.root.input.model.unit_001.discretization.ncol = n_col          
        model.root.input.model.unit_001.discretization.nbound = n_bound  
        model.root.input.model.unit_001.discretization.npartype = n_partype
        model.root.input.model.unit_001.discretization.par_geom = 'SPHERE'           

        ###########################################  Outlet  ######################################################
        model.root.input.model.unit_002.unit_type = 'OUTLET'
        model.root.input.model.unit_002.ncomp = n_comp

        
        ######################################  Sections and Switches  ############################################
        model.root.input.solver.sections.nsec = 1                         
        model.root.input.solver.sections.section_times = [0.0, t_in_seconds]  
        model.root.input.solver.sections.section_continuity = [0]          

        model.root.input.model.connections.nswitches = 1                  
        model.root.input.model.connections.switch_000.section = 0         
        model.root.input.model.connections.switch_000.connections = [
            
            0, 1, -1, -1, volume_flow_rate,                                               
            1, 2, -1, -1, volume_flow_rate]
        

                #unit_from, unit_to, component_from, component_to, volumetric flow rate
                #unit_000, unit_001, all components, all components, Q
                #unit_001, unit_002, all components, all components, Q
                #-1 = all components from origin and destination unit are connected
                
                
        #######################################  Simulator Settings  ################################################
        
        
        model.root.input.solver.user_solution_times = np.linspace(0, t_in_seconds, resolution)
        
        return model  

    def create_and_run_model(self, t_in_seconds, c_feed,  resolution, volume_flow_rate, height, crosssection, filmdiffusion,freundlich_k, freundlich_n):
        model = self.create_column_bB_GRM_AFR(t_in_seconds, c_feed,  resolution, volume_flow_rate, height, crosssection, filmdiffusion,freundlich_k, freundlich_n)
        print("Simulation started")
        model = self.run_simulation(model)
        return model
        
