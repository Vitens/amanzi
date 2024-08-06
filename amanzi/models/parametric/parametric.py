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
      self.parse_yaml(filename)
    
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
    for name, section, category, param in self._flatten(model.get('parameters', {})):
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
    for name, section, category, param in self._flatten(model.get('outputs', {})):
      self.output_parameters[name] = Output(name, section, category, filename, param)
      if 'parameters' in param:
        for iname, inneroutput in param['parameters'].items():
          self.output_parameters[iname] = Output(iname, section, category, filename, inneroutput, True)
    
  @staticmethod
  def _flatten(parameters):
    return [
      (name, section, category, param)
      for category, sections in parameters.items()
      for section, values in sections.items()
      for name, param in values.items()
    ]
  
  @property
  # default methods
  def methods(self):
    return {
      'test': lambda x: x**2,
    }

  
  @property
  # calculation context for parameters
  def context(self):
    return self.parameters | self.methods | {'quantity': self.quantity, 'quality': self.quality} | self.output_parameters
  

  def generate_tables(self):

    outputs = [o for o in self.output_parameters.values() if o.category == 'design']

    sections = []
    section = ""
    for o in outputs:
      if o.section != section:
        section = o.section
        sections.append({'name': section, 'namespace': o.namespace})
    
    values = {o.name: {} for o in outputs}
    invalid = {o.name: {} for o in outputs}

    for capacity in ['minimal_capacity', 'nominal_capacity', 'maximal_capacity']:
      # reset outputs
      for o in outputs:
        o.reset()

      label = capacity[:3]
      capacity = self.parameters.get(capacity, 0)
      
      # calculate outputs
      for o in outputs:
        values[o.name][label] = o.calculate(self.context | {'capacity': capacity})
        invalid[o.name][label+'_invalid'] = int(not o.validate(self.context | {'capacity': capacity}))

    return {
      'outputs':
        [{'name': o.name,
        'uom': o.uom,
        'indent': o.indent,
        'namespace': o.namespace,
        'section': o.section,
        'precision': o.precision,
        } | values[o.name] | invalid[o.name]
        for o in outputs if not o.hidden(self.context)],
      'sections': sections
    }