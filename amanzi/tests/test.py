import pprint as pp
from amanzi.core import Project

p = Project('/Users/Abel/Downloads/ro.json')

s  = p.scenarios[0]

s.run_scenario()