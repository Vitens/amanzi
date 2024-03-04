import cProfile
from amanzi.core import Project

demo = Project('/Users/Abel/Vitens/Projecten/amanzi/amanzi/tests/RO_demo.json')

def profile():
    demo.scenarios[0].solver.solve()

cProfile.run('profile()', 'membrane.prof')