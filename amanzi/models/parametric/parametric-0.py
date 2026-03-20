import importlib.resources
from dataclasses import dataclass
from collections import OrderedDict
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
                if name in self.input_parameters:
                  # merge parameters
                  self.input_parameters[name].update(param)

                else:
                  # create new parameter
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

  @property
  def values(self):
    return {
      'product_flow': self.inflows.get('product', 0)
    }
  
  def load_defaults(self):
    defaults = {}
    for name, param in self.input_parameters.items():
      defaults[name] = param.get('default', 0)
    return defaults

  def calculate_outputs(self):

    inputs = self.config['configuration'].get('parameters', {})
    defaults = self.load_defaults()
    defaults.update(inputs)
    inputs = defaults

    outputs = self.output_parameters

    # calculate results for minimal, nominal, and maximal capacity
    for capacity in ['minimal_capacity', 'nominal_capacity', 'maximal_capacity']:
      values = {}
      label = capacity[:3]
      inputs['capacity'] = inputs.get(capacity, 0)

      for output in outputs:
        for o in output.get('inner',[]) + [output]:
          name = o['name']
          if 'if' in o and not eval(o['if'], inputs | values):
              o['hidden'] = True
              continue
          
          try:
              equation_result = eval(o["equation"], self.methods, inputs | values | self.values)
              o[label] = equation_result

              values[name] = equation_result

              if 'validation' in o and not eval(o['validation'], inputs | values):
                o[label + '_invalid'] = True

          except:
            print(values)
            print('Error in equation for output {}'.format(name))
            raise
    

    return outputs

  def generate_tables(self):
    tables = []

    # solve model
    outputs = self.calculate_outputs()

    # generate design
    # filter for design outputs
    tables = []

    for c,summation,precision in [['design', None, 0], ['energy', 'kWh/m3', 3]]:

      design = [o for o in outputs if o['category'] == c]

      sections = []
      section = {}

      for output in design:
          if output['section'] != section.get('name',''):
              if section.get('name', ''):
                  sections.append(section)
              section = {
                  'name': output['section'],
                  'parameters': [],
                  'precision': precision,
              }
              if summation:
                # add summation fields
                section.update({'nom': 0, 'min': 0, 'max': 0, 'uom': summation})

          if not output.get('hidden', False):
            section['parameters'].append(output)
            # apply namespace to section for i18n
            section['namespace'] = output['namespace']

            if summation and output['uom'] == summation:
              section['nom'] += output['nom']
              section['min'] += output['min']
              section['max'] += output['max']

      sections.append(section)


      table = {
        'name': c,
        'sections': sections
      }
      if summation:
        table['totals'] = {
          'nom': sum([s.get('nom',0) for s in sections]),
          'min': sum([s.get('min',0) for s in sections]),
          'max': sum([s.get('max',0) for s in sections]),
          'uom': summation
        }

      tables.append(table)

    return tables






              
