import importlib.resources
from .output import Output
from dataclasses import dataclass
from collections import OrderedDict
import ast
import math
import yaml

class ParametricModel():

  def __init__(self, config, **kwargs):

    self.config = config.get('configuration', {})
    # list of input parameters
    self.input_parameters = OrderedDict()
    # list of output parameters
    self.output_parameters = OrderedDict()

    # parse the yaml files
    for filename in self.parametric_model:
      try:
        self.parse_yaml(filename)
      except Exception as e:
        raise Exception(f"Error parsing {filename}.yml: {e}")

    
    # set parameters
    self.parameters = self.config.get('parameters', {})
    # set unknown parameters to default values
    for name, param in self.input_parameters.items():
      self.parameters[name] = param.get('default', None) if name not in self.parameters else self.parameters[name]


  def parse_yaml(self, filename):
    with importlib.resources.open_text('amanzi.parametric', filename + '.yml') as file:
      model = yaml.safe_load(file)

      self.process_parameters(model, filename)
      self.process_outputs(model, filename)

  def process_parameters(self, model, filename):
    for name, section, category, param, _ in self._flatten(model.get('parameters', {})):
      if name in self.input_parameters:
        # merge parameters
        self.input_parameters[name].update(param)
      else:
        self.input_parameters[name] = param
      
      # set the section, category, and namespace
      self.input_parameters[name].update({
        'section': section,
        'category': category,
        'namespace': filename
      })

  def process_outputs(self, model, filename):
    for name, section, category, param, parent in self._flatten(model.get('outputs', {})):
      if name in self.output_parameters:
        self.output_parameters[name].update(filename, param)
      else:
        if parent:
          parent = self.output_parameters[parent]
        self.output_parameters[name] = Output(name, section, category, filename, param, parent)
    
    
  @staticmethod
  def _flatten(parameters):
    flattened = []
    for category, sections in parameters.items():
      for section, values in sections.items():
        for name, param in values.items():
          flattened.append((name, section, category, param, None))
          if 'parameters' in param:
            for iname, innerparam in param['parameters'].items():
              flattened.append((iname, section, category, innerparam, name))
    return flattened
  
  @property
  # default methods
  def methods(self):
    return {
      'test': lambda x: x**2,
    }
  
  def get_output(self, name, default=None):
    if name in self.parameters:
      return self.parameters[name]

    if name not in self.output_parameters:
      return default

    output = self.output_parameters.get(name)
    ctx = self.context

    if 'nominal_capacity' in self.parameters:
      ctx = ctx | {'capacity': self.parameters['nominal_capacity']}

    try:
      result = output.calculate(ctx)
    except:
      raise Exception(f"Error calculating {name} for {self.name}")

    return result

  
  @property
  # calculation context for parameters
  def context(self):
    return self.parameters | self.methods | {'quantity': self.quantity, 'quality': self.quality, 'hydraulics': self.hydraulics, 'energy': self.energy, 'db': self.database, 'chemicals': self.chemicals} | self.output_parameters

  def generate_tables(self):

    tables = []

    for c,summarize,precision in [['design',None,0], ['hydraulic',None,0], ['energy','kWh/m3',3], ['sustainability', 'gCO2-eq/m3', 2], ['chemicals', None, 0]]:
      outputs = [o for o in self.output_parameters.values() if o.category == c]

      sections = []
      # find sections
      for o in outputs:
        if not any(s['name'] == o.section for s in sections):
          section = o.section
          sections.append({'name': section, 'namespace': o.namespace, 'precision': precision, 'uom': summarize})
      
      values = {o.name: {} for o in outputs}
      invalid = {o.name: {} for o in outputs}

      for capacity in ['minimal_capacity', 'maximal_capacity', 'nominal_capacity']:
        # reset outputs
        for o in outputs:
          o.reset()
        


        label = capacity[:3]
        capacity = self.parameters.get(capacity, None)

        if capacity is not None and capacity <= 0:
          # skip if capacity is -1
          continue
        
        # calculate outputs
        for o in outputs:
          values[o.name][label] = o.calculate(self.context | {'capacity': capacity})
          invalid[o.name][label+'_invalid'] = int(not o.validate(self.context | {'capacity': capacity}))
        
          if summarize and o.uom == summarize and not o.hidden(self.context) and o.parent is None:
            # find relevant section
            section = next((s for s in sections if s['name'] == o.section), None)
            section[label] = section.get(label, 0) + values[o.name][label]

      totals = {'uom': summarize}
      if summarize:
        # calculate totals from sections
        for s in sections:
          for label in ['min', 'max', 'nom']:
            totals[label] = totals.get(label, 0) + s.get(label, 0)

      tables.append({
        'name': c,
        'outputs':
          [{'name': o.name,
          'uom': o.uom,
          'indent': True if o.parent else False,
          'namespace': o.namespace,
          'section': o.section,
          'precision': o.precision,
          } | values[o.name] | invalid[o.name]
          for o in outputs if not o.hidden(self.context)],
        'sections': sections,
        'totals': totals if summarize else None
    })
    return tables