from .solver import Solver

class ChemicalSolver(Solver):

  def solve(self, until=None):

    models = self.scenario.models if not until else {until: self.scenario.models[until]}

    for m in models.values():
      outputs = [o for o in m.output_parameters.values() if o.category == 'chemicals' and o.uom == 'gAS/m3' and not o.hidden(m.context) and o.parent is None]

      for o in outputs:
        m.chemicals[o.name] = o.calculate(m.context)
      
      print(m.chemicals)




  def summary(self):
    pass