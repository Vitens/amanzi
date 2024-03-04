from .model import Model

class Output(Model):

    @property
    def equations(self):
        return []
    
    @property
    def quality_table(self):
        ## return table of quality
        print(self.solution.elements)

        parameters = [
        {'name': 'pH', 'll': 6.5, 'lt': 7.7, 'ut': 8.3, 'ul': 9.5, 'value': lambda s: s.pH, 'units': '-'},
        {'name': 'EGV 20°C', 'ut': 80, 'ul': 130, 'value': lambda s: s.sc20/10, 'units': 'mS/m'},
        {'name': 'Zuurstof', 'lt': 4, 'll': 2, 'value': lambda s: s.total('Oxg')*32 + s.total('O2') * 32, 'units': 'mg/l'},
        {'name': 'Hardheid', 'ut': 1.43, 'ul': 2, 'll': 1, 'value': lambda s: s.hardness, 'units': 'mmol/l'},
        {'name': 'TACC90', 'ut': 0.4, 'ul': 0.6, 'value': lambda s: s.ccpp90, 'units': 'mmol/l'},
        {'name': 'AggCO2', 'ul': 2.2, 'ut': 2.2, 'units': 'mg/l', 'value': lambda s: -1 * min(0, s.ccpp()) * 44.01},
        {'name': 'Fe', 'ut': 0.05, 'ul': 0.1, 'value': lambda s: s.total('Fe')*55.84, 'units': 'mg/l'},
        {'name': 'Mn', 'ut': 0.01, 'ul': 0.05, 'value': lambda s: s.total('Mn', 'mg'), 'units': 'mg/l'},
        {'name': 'NH4', 'ut': 0.05, 'ul': 0.20, 'value': lambda s: s.total('[N-3]', 'mmol')*18, 'units': 'mg/l'},
        {'name': 'Na', 'ul': 100, 'value': lambda s: s.total('Na')*22.99, 'units': 'mg/l'},
        {'name': 'Cl', 'ut': 100, 'ul': 150, 'value': lambda s: s.total('Cl')*35.45, 'units': 'mg/l'},
        ]
    
        output = []
        for p in parameters:
            p['value'] = p['value'](self.solution)
    
        return parameters
        




    
    # @property
    # def mass(self):
    #     inflow = sum([c.flow for c in self.upstream_connections['product']])
    #     return -self.solution.total('Na') * inflow
