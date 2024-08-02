import pprint
from dataclasses import dataclass
import numpy as np

@dataclass
class HydraulicSolver:
    """
    A class to solve all linear equations in a process.

    ...

    Attributes
    ----------
    scenario : dict
        config of a scenario containing all models and connections

    Methods
    -------
    solve():
        Solve the linear matrix equation.
    """

    scenario: dict

    def solve(self) -> list: 
  

      pump_minimal_sump_pressure = 1 # meters

      models = {
        'Winning': {
          'delta_h': 10, # this includes drawdown, local losses and losses in transport pipeline, in meters (min. head required to reach ref. level of treatment plant)
          'efficiency': 0.55 # pump efficiency
        },
        'Splitter': {
          'delta_h': 0,
          'pressurized': True # if True, the model is pressurized
        },
        'Pressure1': {
          'delta_h': 5, # meters
          'pressurized': True # if True, the model is pressurized
        },
        'Pressure2': {
          'delta_h': 50, # meters
          'pressurized': True, # if True, the model is pressurized
          'integral_pump': True, # if True, pump is integral to the model
          'pump_z': 1 # elevation of pump inlet above ground level, should have at least 1 meter of sump head
        },
        'Cascade': {
          # h_in is user input and consists of z_in + delta_p_inlet
          'h_in': 9, # meters (head at the inlet of the cascade, including inlet losses!)
          'delta_h':2 # meters (head at the outlet of the cascade)
        },
        'SandFilter': {
          'h_in': 7,
          'delta_h': 6
        },
        'Tower': {
          'h_in': 12, # meters (head at the inlet of the tower, including inlet losses!)
          'delta_h': 10 # meters (head at the outlet of the tower)
        },
        'Reservoir': {
          'h_in': 5,
          'delta_h': 2 # represents mean reservoir level
        },
        'Output': {
          'h_in': 35 # customer pressure demand
        }
      }
      connections = [
        {'src': 'Winning', 'tgt': 'Splitter', 'flow': 100},
        {'src': 'Splitter', 'tgt': 'Pressure1', 'flow': 50},
        {'src': 'Pressure1', 'tgt': 'Pressure2', 'flow': 50},
        {'src': 'Pressure2', 'tgt': 'Reservoir', 'flow': 50},
        {'src': 'Reservoir', 'tgt': 'Output', 'flow': 100},
        {'src': 'Splitter', 'tgt': 'Cascade', 'flow': 50},
        {'src': 'Cascade', 'tgt': 'SandFilter', 'flow': 50},
        {'src': 'SandFilter', 'tgt': 'Tower', 'flow': 50},
        {'src': 'Tower', 'tgt': 'Reservoir', 'flow': 50}
      ]
      amanzi_connections = [
        

      ]
      class Connection:
          def __init__(self, id, config, models):
              self.name = 'From_'+str(config['src']) + '_to_' + str(config['tgt'])
              self.id = id
              self.from_uid = config['src']
              #self.from_model = models[config['src']]
              #self.from_anchor = config['srcAnchor']
              self.booster = False
              self.booster_head = 0
              
              self.to_uid = config['tgt']
              self.to_model = models[config['tgt']]
              self.iteration = 0
              self.flow = 0
              self.solution = False
              self.h_loss = 0
              self.efficiency = 0
          def __repr__(self):
              return f'<Connection {self.name}>'



      class Model():
        def __init__(self, name, info):
          self.uid = name
          self.info = info
        
        def __repr__(self):
          return f'<Model {self.uid}>'

        @property
        def downstream_models(self):
          return [models[c['tgt']] for c in connections if c['src'] == self.uid]
        
        @property
        def upstream_models(self):
          return [models[c['src']] for c in connections if c['tgt'] == self.uid]





      models = {uid: Model(uid, info) for uid, info in models.items()}
      connections2 = {Connection(i, config, models) for i, config in enumerate(connections)}


      start_nodes = [conn for conn  in connections2 if not models[conn.from_uid].upstream_models]
      leaf_nodes = [conn for conn in connections2 if not models[conn.to_uid].downstream_models]


      def walk_backwards(from_node):
          current_model = models[from_node.to_uid]
          upstream_model= models[from_node.from_uid]

          if 'integral_pump' in upstream_model.info:
              upstream_model.info['h_in'] = upstream_model.info['pump_z']
              upstream_model.info['h_out'] =  current_model.info['h_in']
              upstream_model.info['pump_head'] = current_model.info['h_in'] - upstream_model.info['h_in']  + upstream_model.info['delta_h']

          elif 'pressurized' in upstream_model.info or not upstream_model.upstream_models:
              # assign highest required h_in to upstream model
              upstream_model.info['h_in'] = max(current_model.info['h_in'] + upstream_model.info['delta_h'], upstream_model.info.get('h_in', 0))
              upstream_model.info['h_out']= upstream_model.info['h_in'] - upstream_model.info.get('delta_h', 0)

          else:
              upstream_model.info['h_out']= upstream_model.info['h_in'] - upstream_model.info.get('delta_h', 0)
              required_head = current_model.info['h_in']
              if 'h_out' in upstream_model.info and required_head > upstream_model.info['h_out']:
                  # assign booster to connection
                  print('This is called')
                  from_node.booster = True
                  from_node.booster_head = required_head - upstream_model.info['h_out']
          upstream_connection = [c for c in connections2 if c.to_uid == from_node.from_uid]

          

          for c in upstream_connection:
              walk_backwards(c)



      def walk_forward(from_node, pump_efficiency):
        current_model = models[from_node.from_uid]
        downstream_model= models[from_node.to_uid]

        h_loss = current_model.info['h_out'] - downstream_model.info['h_in']

        if downstream_model.info.get('pressurized',False) and h_loss > 0 and not 'integral_pump' in downstream_model.info:
          downstream_model.info['h_in'] += h_loss
          downstream_model.info['h_out'] += h_loss
        elif downstream_model.info.get('pressurized',False) and h_loss > 0 and 'integral_pump' in downstream_model.info:
          downstream_model.info['h_in'] += h_loss
        elif h_loss > 0:
          from_node.h_loss = h_loss

        if 'integral_pump' in current_model.info:
          current_model.info['pump_head'] = downstream_model.info['h_in'] - current_model.info['h_in']  + current_model.info['delta_h']
          from_node.efficiency = 0.75

        from_node.efficiency = pump_efficiency if from_node.booster == False else 0.75

        downstream_connection = [c for c in connections2 if c.from_uid == from_node.to_uid]
        for c in downstream_connection:
          walk_forward(c, pump_efficiency)




      for leaf in leaf_nodes:
        walk_backwards(leaf)

      for node in start_nodes:
        walk_forward(node, models[node.from_uid].info['efficiency'])

      for connection in connections2:
          pprint.pprint(vars(connection))

      #vars(connection))
      print('---')

      for m in models:
        print(m, models[m].info)