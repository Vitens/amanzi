import pprint as pp
from amanzi.core import Project

p = Project('/Users/Abel/Downloads/demo123.json')

s  = p.scenarios[0]

s.run_scenario(until='cfzrwi')