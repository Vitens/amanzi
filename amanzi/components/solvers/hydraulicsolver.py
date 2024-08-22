import logging
from .solver import Solver

class HydraulicSolver(Solver):
    """
    A class to solve all hydraulic equations in a scenario.

    The solver works by first tranversing from leaf nodes to starting nodes, assigning head_in and head_out values to each node based on the minimal required head and total headloss.
    Then, the solver tranverses from starting nodes to leaf nodes, propagating head_in and head_out values for pressurized nodes, and assigning booster heads and pump efficiency to connections.
    """

    def solve(self, until=None):
      
      start_nodes = [m for m in self.scenario.models.values() if not m.upstream_connections.get('product')]
      leaf_nodes = [m for m in self.scenario.models.values() if not m.downstream_connections.get('product')]

      for leaf in leaf_nodes:
        self._walk_backwards(leaf)
      
      for start in start_nodes:
        self._walk_forward(start, 0.55) # pump efficiency of 55% for now
      
      # assign average efficiency to models
      for m in self.scenario.models.values():
        # efficiency is weighted average of all upstream connections
        for c in m.upstream_connections.get('product', []):
          m.hydraulics.efficiency += c.hydraulics.efficiency * c.quantity.flow / m.quantity.inflow.product

    def _walk_backwards(self, from_node):
      """
        Walks backwards from a given node, assigning head_in and head_out values to each node
        It is required to walk backwards before walking forwards to ensure that the head_in and head_out values are correct for pressure nodes
      """
      # get node info
      info = self.hydraulic_info(from_node)

      if info['pressurized']:
        # get maximum head required by downstream nodes
        if from_node.downstream_connections.get('product'):
          head_out_required = max([c.to_model.hydraulics.head_in for c in from_node.downstream_connections.get('product', [])])
        else:
          head_out_required = 0

        # assign highest required head to node
        from_node.hydraulics.head_out = max(from_node.hydraulics.head_out, head_out_required)

        # check for integrated booster
        if info['integrated_booster']:
          from_node.hydraulics.head_in = info['minimal_head'] # assign minimal required head to node
        else:
          # calculate head in based on head out and total headloss
          from_node.hydraulics.head_in = max(from_node.hydraulics.head_out + info['total_headloss'], info['minimal_head'])
      # if node is not pressurized
      else:
        from_node.hydraulics.head_in = info['minimal_head'] # assign minimal required head to node
        from_node.hydraulics.head_out = info['minimal_head'] - info['total_headloss'] # calculate head out based on head in and total headloss

      # walk backwards to upstream nodes
      for c in from_node.upstream_connections.get('product', []):
        self._walk_backwards(c.from_model)
      

    def _walk_forward(self, from_node, pump_efficiency):
      """ Walks forward from starting nodes to leaf nodes. Propagate head_in and head_out for pressurized nodes, and assign booster and pump efficiency to connections """

      info = self.hydraulic_info(from_node)

      # if pressurized, set h_in with highest head_out of upstream nodes
      if info['pressurized']:
        # if upstream nodes, get highest head_out and assign it to head_in if higher than current head_in
        if from_node.upstream_connections.get('product'):
          from_node.hydraulics.head_in = max([c.from_model.hydraulics.head_out for c in from_node.upstream_connections.get('product', [])] + [from_node.hydraulics.head_in])

          # if integrated booster, assign booster head
          if info['integrated_booster']:
            # calculate booster head based on head_in, head_out and total headloss
            from_node.hydraulics.booster_head = from_node.hydraulics.head_out - from_node.hydraulics.head_in + info['total_headloss']
            # check for negative booster head
            if from_node.hydraulics.booster_head < 0:
              from_node.hydraulics.booster_head = 0 # set booster head to 0 if negative
              logging.warning(f'Negative integrated booster head at {from_node.name}')
              # set head out as head in - total headloss
              from_node.hydraulics.head_out = from_node.hydraulics.head_in - info['total_headloss']
            else:
              pump_efficiency = 0.75

            # set pump efficiency to 75% for integrated booster
          else:
            # calculate head_out based on head_in and total headloss
            from_node.hydraulics.head_out = from_node.hydraulics.head_in - info['total_headloss']

      for c in from_node.downstream_connections.get('product', []):
        # assign booster to connection if head_out is lower than head_in
        if from_node.hydraulics.head_out < c.to_model.hydraulics.head_in:
          pump_efficiency = 0.75
          c.hydraulics.booster = True
          c.hydraulics.booster_head = c.to_model.hydraulics.head_in - from_node.hydraulics.head_out
        
        if from_node.hydraulics.head_out > c.to_model.hydraulics.head_in:
          c.hydraulics.headloss = from_node.hydraulics.head_out - c.to_model.hydraulics.head_in
        
        # assign pump efficiency to connection
        c.hydraulics.efficiency = pump_efficiency
        # walk forward to downstream node
        self._walk_forward(c.to_model, pump_efficiency)

    @staticmethod
    def hydraulic_info(model):
      return {
        'pressurized': model.get_output('pressurized', True),
        'integrated_booster': model.get_output('integrated_booster', False),
        'inlet_elevation': model.parameters.get('inlet_elevation', 0),
        'outlet_elevation': model.get_output('outlet_elevation', 0),
        'minimal_head': model.get_output('minimal_head', 0),
        'total_headloss': model.get_output('total_headloss', 0)
      }


    def print_debug(self):
      print("====================================")
      s = self.scenario

      print(f'{"Model":<20} \t {"Hin"} \t {"Ho"} \t {"Hb"}')
      for _,m in s.models.items():
        print(f'{m.name:<20} \t {m.hydraulics.head_in} \t {m.hydraulics.head_out} \t {m.hydraulics.booster_head}')

    
    def summary(self):

      return {
        'total_boosters': len([c for c in self.scenario.connections.values() if c.hydraulics.booster]),
        'total_headloss': sum([c.hydraulics.headloss for c in self.scenario.connections.values()]),
      }