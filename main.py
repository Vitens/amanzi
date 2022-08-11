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