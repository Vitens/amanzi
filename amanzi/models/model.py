from ..components import Connection

class Model:
    def __init__(self, config):
        self.uid = config['uid']
        self.type = config["type"]
        self.name = self.type.capitalize()
        self.connections = {'top': [], 'bottom': [], 'left': [], 'right': []}

    # def connect(self, from_anchor, to_model, to_anchor):
    #     new_connection = Connection(self, to_model)
    #     self.connections.setdefault(from_anchor, []).append(new_connection)
    #     to_model.connections.setdefault(to_anchor, []).append(new_connection)        
    
    # def get_conn(self, anchor):
    #     self.connections.get(anchor, [])

    @property
    def equations(self):
        return []

    # @property
    # def cost(self):
    #     return 250_000 # €

    # @property
    # def emission(self):
    #     return 500_000 # CO2eq

    # @property    
    # def energy(self):
    #     return 350_000 # kWh