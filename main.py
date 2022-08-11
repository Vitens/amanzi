from amanzi.core import Project

project = Project('projectB.slm')

print(project.scenarios[1].flows)

