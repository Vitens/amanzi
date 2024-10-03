import pprint as pp
from amanzi.core import Project

p = Project('/Users/Abel/Downloads/vacuum.json')

s  = p.scenarios[0]

pp.pprint(s.models['0mcq94'].parameters)
