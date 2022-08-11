from amanzi.core import Project

project = Project('inputs/projectC.slm')


print(" ")
print(f"✅ Project processed!")
print(" ")
print("Summary")
print("_________")
print(f"Name: {project.project_name}")
print(f"Author: {project.author}")
print(f"Description: {project.description}")
print(f"Version: {project.version}")
print(f"UI Version: {project.ui_version}")

print(" ")
print("Scenarios")
print("_________")
for scenario in project.scenarios.values():
    print(f"Name: {scenario.name}")
    print(f"Description: {scenario.description}")
    print(f"Version: {scenario.scenario_version}")
    print(" ")

model_uid = '3'



print("self.waste", project.scenarios[1].waste)
print("self.inflow", project.scenarios[1].inflow)
print("self.outflow", project.scenarios[1].outflow)

print("self.waste", project.scenarios[2].waste)
print("self.inflow", project.scenarios[2].inflow)
print("self.outflow", project.scenarios[2].outflow)
# print(project.scenarios[1].waste)
# print(project.scenarios[1].models[model_uid].upstream_connections)
# print(project.scenarios[1].models[model_uid].inflow)
# print(project.scenarios[1].models[model_uid].downstream_connections)
# print(project.scenarios[1].models[model_uid].outflow)