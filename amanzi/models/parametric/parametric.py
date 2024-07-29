import os
import importlib.resources
from collections import OrderedDict
import pprint
import math
import yaml

class ParametricModel():
  def __init__(self, config):

    self.input_parameters = OrderedDict()
    self.output_parameters = []

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
      for section, values in outputs.items():
            for name, output in values.items():
                output['name'] = name
                output['category'] = category
                output['section'] = section
                output['namespace'] = filename
                self.output_parameters.append(output)
                output['inner'] = []

                for iname, inneroutput in output.get('parameters', {}).items():
                    inneroutput['name'] = iname
                    inneroutput['category'] = None
                    inneroutput['parameter'] = name
                    self.output_parameters.append(inneroutput)
                    output['inner'].append(inneroutput)
                

  @property
  def methods(self):
     return {
        'math': math
     }

  def calculate_outputs(self):

    inputs = self.config['configuration'].get('parameters', {})

    outputs = self.output_parameters

    for capacity in ['minimal_capacity', 'nominal_capacity', 'maximal_capacity']:
      values = {}
      label = capacity[:3]
      inputs['capacity'] = inputs.get(capacity, 0)

      for output in outputs:
        name = output['name']
        if 'if' in output and not eval(output['if'], inputs | values):
            output['hidden'] = True
            continue
        
        try:
            equation_result = eval(output["equation"], self.methods, inputs | values)
            output[label] = equation_result

            values[name] = equation_result
        except:
          raise
    

    return outputs

  def generate_tables(self):
    tables = []

    # solve model
    outputs = self.calculate_outputs()

    # generate design
    # filter for design outputs
    design = [o for o in outputs if o['category'] == 'design']

    sections = []
    section = {}

    for output in design:
        if output['section'] != section.get('name',''):
            if section:
                sections.append(section)
            section = {
                'name': output['section'],
                'parameters': []
            }
        if not output.get('hidden', False):
          section['parameters'].append(output)
          # apply namespace to section for i18n
          section['namespace'] = output['namespace']


    sections.append(section)

    table = {
       'name': 'design_calculations',
       'sections': sections
    }

    return [table]






              
