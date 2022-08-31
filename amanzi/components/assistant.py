class Assistant:
    def __init__(self, project):
        self.project = project
        # self.parse_metadata(project)
        
    def parse_metadata(self, instance):
        metadata = getattr(instance, "config")["metadata"]
        for key, meta in metadata.items():
            setattr(instance, key, meta)


    
        