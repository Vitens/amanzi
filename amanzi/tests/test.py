import pprint as pp
from amanzi.core import Project

p = Project('/Users/Abel/Downloads/demo-complete.json')

s  = p.scenarios[0]

import time
st = time.time()
p.report()
et = time.time()