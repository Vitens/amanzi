import os
import importlib.resources
from collections import OrderedDict
import yaml

class ParametricModel():
  def __init__(self, config):

    self.input_parameters = OrderedDict()
    self.output_parameters = OrderedDict()

    for filename in self.parametric_model:
      self.parse_yaml(filename)
    
  def parse_yaml(self, filename):
    with importlib.resources.open_text('amanzi.parametric', filename + '.yml') as file:
      model = yaml.safe_load(file)

      self.process_parameters(model, filename)
      self.process_outputs(model, filename)

  def process_parameters(self, model, filename):
    for category, params in model.get('parameters', {}).items():
      for section, values in params.items():
            for name, param in values.items():
                self.input_parameters[name] = param
                self.input_parameters[name]['section'] = section
                self.input_parameters[name]['category'] = category
                self.input_parameters[name]['namespace'] = filename

  def process_outputs(self, model, filename):
    for category, outputs in model.get('outputs', {}).items():
            for name, output in outputs.items():
                self.output_parameters[name] = output
                self.output_parameters[name]['category'] = category
                self.output_parameters[name]['namespace'] = filename