from ..components import Connection

class Model:
    def __init__(self, config):
        self.uid = config['uid']
        self.type = config["type"]
        self.name = self.type.capitalize()
        self.connections = {}

    @property
    def upstream_connections(self):
        upstream = []
        upstream.extend(self.connections.get("left", []))
        upstream.extend(self.connections.get("top", []))

        return upstream
    
    @property
    def downstream_connections(self):
        downstream = []
        downstream.extend(self.connections.get("right", []))
        downstream.extend(self.connections.get("bottom", []))

        return downstream

    @property
    def inflow(self):
        return sum([conn.flow for conn in self.upstream_connections])

    @property
    def outflow(self):
        """all outgoing flows, including waste flows"""
        return sum([conn.flow for conn in self.downstream_connections])

    # @property
    # def waste_flow(self):
    #     for conn in self.connections.values():
    #         if isinstance(conn.to_model, Output)


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