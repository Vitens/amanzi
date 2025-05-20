import inspect
import json

from amanzi import models
from amanzi.core import Project, Database
from amanzi.models.parametric import ParametricModel
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class AmanziAPI():
  def __init__(self):
    """AmanziAPI provides the server-side API endpoints for the Amanzi web interface.
    
    The API handles:
    - Getting model parameters
    - Running scenario simulations
    - Generating reports
    - Performing design optimizations
    - Retrieving key performance figures

    The API can either be called as a Flask application or through a lambda function (AWS).
    """

    pass

  def parameters(self):
    parameters = {}

    for n,obj in inspect.getmembers(models, inspect.isclass):
        logger.debug(f"Found class: {n}")
        if issubclass(obj, ParametricModel) and n != 'Model':
            params = obj({}, None).input_parameters
            parameters[n.lower()] = [p | {'name': n, 'type': type(p['default']).__name__} for n,p in params.items()]

    return json.dumps(parameters)
  
  def solve(self, data, scenario):
    if isinstance(data, str):
      data = json.loads(data)
    p = Project(data)
    p.scenarios[int(scenario)].run_scenario()
    ## get output model
    s = p.scenarios[int(scenario)]

    quantity_summary = s.solvers['quantity'].summary()

    quantity = {
        'abstraction': quantity_summary['total_production'],
        'distribution': quantity_summary['total_distribution'],
    }

    energy_summary = s.solvers['energy'].summary()

    energy = {
        'total_consumption': energy_summary['total_consumption'],
        'specific_consumption': energy_summary['specific_consumption'],
        'specific_consumption_production': energy_summary['specific_consumption_production'],
        'specific_consumption_distribution': energy_summary['specific_consumption_distribution']
    }

    resp = {
            'connections': {c.cid : {'flow': c.quantity.flow, 'booster': c.hydraulics.booster, 'booster_head': c.hydraulics.booster_head, 'efficiency': c.hydraulics.efficiency, 'headloss': c.hydraulics.headloss} for c in s.connections.values()},
            'hydraulics': {m.uid: m.hydraulics.toDict() for m in s.models.values()},
            'metrics': {
                'energy': s.solvers['energy'].summary()['metrics'],
                'quantity': s.solvers['quantity'].summary()['metrics'],
                'quality': s.solvers['quality'].summary()['metrics'],
                'sustainability': s.solvers['sustainability'].summary()['metrics']
            },
            }

    return json.dumps(resp)
  
  def report(self, data):
    if isinstance(data, str):
      data = json.loads(data)
    p = Project(data)
    return json.dumps(p.report())

  def design(self, data, scenario, model):
    if isinstance(data, str):
      data = json.loads(data)
    p = Project(data)
    s = p.scenarios[int(scenario)]
    s.run_scenario(until=model)

    response = {
        'hydraulics': {
            'connections': {c.cid : {'flow': c.quantity.flow, 'booster': c.hydraulics.booster, 'booster_head': c.hydraulics.booster_head, 'efficiency': c.hydraulics.efficiency, 'headloss': c.hydraulics.headloss} for c in s.connections.values()},
            'models': {m.uid: m.hydraulics.toDict() for m in s.models.values()},
        }
    }

    response.update(s.models[model].run_design())

    return json.dumps(response)

  def keyfigures(self):
    # load csv as array
    db = Database()
    return json.dumps({'rows':db.rows})