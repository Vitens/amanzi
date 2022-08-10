class ProjectManager:
    def __init__(self, config):
        name = config["metadata"]["project_name"]
        print(f"Hi, I'm a Project Manager from {name}")