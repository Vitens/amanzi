from amanzi.core import Project

demo = Project('/Users/Abel/Downloads/rsf.json')

sc = demo.scenarios[0]  

sc.run_scenario()