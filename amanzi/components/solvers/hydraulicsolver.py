import pprint
from dataclasses import dataclass
import numpy as np
from amanzi.models.model import Model
from amanzi.components.connection import Connection
import phreeqpython as pp
import logging


class HydraulicSolver:

    def __init__(self, scenario):

      self.scenario = scenario
      self.max_iterations = 100
      self.precision = 0.0001
      self.data = {}
      self.stop_at_model = None
      self.interrupted = False
      self.amanzi_connections = []
      self.amanzi_models = []
 

    def solve(self) -> list: 
      
      #print(self.scenario.config['models'])
      # for model in self.scenario.models.values():
      #    #self.amanzi_models.append(Model(model,pp))
      #    print(vars(model))
      #    #print(model.uid)
      
      # for _,c in self.scenario.connections.items():
      #    #self.amanzi_connections.append(Connection(c))
      #    print(vars(c))

      models = {model.uid: model for model in self.scenario.models.values()}
      connections2 = {connection.id: connection for _,connection in self.scenario.connections.items()}
      # print(models)
      # print(connections2)

      start_nodes = [conn for conn  in connections2.values() if not models[conn.from_uid].upstream_connections and conn.type == 'product']
      leaf_nodes = [conn for conn in connections2.values() if not models[conn.to_uid].downstream_connections and conn.type == 'product']

      for i in models.values():
        for j in self.scenario.config['models']:
          if i.uid == j['uid']:
            i.info = j['configuration']['parameters']
        #print(i.info)
    #models
      def walk_backwards(from_node):
          current_model = models[from_node.to_uid]
          upstream_model= models[from_node.from_uid]          

          if 'integral_pump' in upstream_model.info:
              upstream_model.info['inlet_elevation'] = upstream_model.info['pump_z']
              upstream_model.info['outlet_elevation'] =  current_model.info['inlet_elevation']
              upstream_model.info['pump_head'] = current_model.info['inlet_elevation'] - upstream_model.info['inlet_elevation']  + upstream_model.info['influent_pressure_loss']
          # catches all pressurized models and sources (Winning)
          elif upstream_model.info.get('pressurized',False) or not upstream_model.upstream_connections:
              # assign highest required inlet_elevation to upstream model
              upstream_model.info['inlet_elevation'] = max(current_model.info['inlet_elevation'] + upstream_model.info['influent_pressure_loss'], upstream_model.info.get('inlet_elevation', 0))
              upstream_model.info['outlet_elevation']= upstream_model.info['inlet_elevation'] - upstream_model.info.get('influent_pressure_loss', 0)

          else:
              upstream_model.info['outlet_elevation']= upstream_model.info['inlet_elevation'] - upstream_model.info.get('influent_pressure_loss', 0)
              required_head = current_model.info['inlet_elevation']
              if 'outlet_elevation' in upstream_model.info and required_head > upstream_model.info['outlet_elevation']:
                  from_node.booster = True
                  from_node.booster_head = required_head - upstream_model.info['outlet_elevation']
          upstream_connection = [c for c in connections2.values() if c.to_uid == from_node.from_uid]

          

          for c in upstream_connection:
              walk_backwards(c)



      def walk_forward(from_node, pump_efficiency):
        current_model = models[from_node.from_uid]
        downstream_model= models[from_node.to_uid]

        h_loss = current_model.info['outlet_elevation'] - downstream_model.info['inlet_elevation']

        if downstream_model.info.get('pressurized',False) and h_loss > 0 and not 'integral_pump' in downstream_model.info:
          downstream_model.info['inlet_elevation'] += h_loss
          downstream_model.info['outlet_elevation'] += h_loss
        elif downstream_model.info.get('pressurized',False) and h_loss > 0 and 'integral_pump' in downstream_model.info:
          downstream_model.info['inlet_elevation'] += h_loss
        elif h_loss > 0:
          from_node.h_loss = h_loss

        if 'integral_pump' in current_model.info:
          current_model.info['pump_head'] = downstream_model.info['inlet_elevation'] - current_model.info['inlet_elevation']  + current_model.info['influent_pressure_loss']
          from_node.efficiency = 0.75

        from_node.efficiency = pump_efficiency if from_node.booster == False else 0.75

        downstream_connection = [c for c in connections2.values() if c.from_uid == from_node.to_uid]
        for c in downstream_connection:
          walk_forward(c, pump_efficiency)


      pump_efficiency = 0.55

      for leaf in leaf_nodes:
        walk_backwards(leaf)

      for node in start_nodes:
        walk_forward(node, pump_efficiency)

