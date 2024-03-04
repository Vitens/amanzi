from .model import Model

class Output(Model):

    @property
    def equations(self):
        return []
    
    @property
    def quality_table(self):
        ## return table of quality

        parameters = [
        {'name': 'pH', 'll': 6.5, 'lt': 7.7, 'ut': 8.3, 'ul': 9.5, 'min': 6.5, 'max': 9.5, 'value': lambda s: s.pH, 'units': '-'},
        {'name': 'EGV 20°C', 'ut': 80, 'ul': 130, 'smin': 20, 'max': 130, 'rt': True, 'value': lambda s: s.sc20/10, 'units': 'mS/m'},
        {'name': 'Zuurstof', 'lt': 4, 'll': 2, 'min': 2, 'value': lambda s: s.total('Oxg')*32 + s.total('O2') * 32, 'units': 'mg/l'},
        {'name': 'Hardheid', 'ut': 1.43, 'ul': 2, 'll': 1, 'min': 1, 'value': lambda s: s.hardness, 'units': 'mmol/l'},
        {'name': 'TACC90', 'ut': 0.4, 'ul': 0.6, 'min': 0.2, 'max': 0.7, 'value': lambda s: s.ccpp90, 'units': 'mmol/l'},
        {'name': 'AggCO2', 'ul': 2.2, 'ut': 2.2, 'units': 'mg/l', 'value': lambda s: -1 * min(0, s.ccpp()) * 44.01},
        # {'name': 'Agressief CO2', 'ut': 2.2, 'smin': 0, 'smax': 2.5},
        # {'name': 'TOC', 'ut': 3, 'ul': 5, 'smin': 0, 'smax': 6},
        # {'name': 'Kleurintensiteit', 'ut': 10, 'ul': 20, 'min': 0, 'max': 25},
        {'name': 'Fe', 'ut': 0.05, 'ul': 0.1, 'min': 0, 'max': 0.15, 'value': lambda s: s.total('Fe')*55.84, 'units': 'mg/l'},
        {'name': 'Mn', 'ut': 0.01, 'ul': 0.05, 'min': 0, 'max': 0.06, 'value': lambda s: s.total('Mn', 'mg'), 'units': 'mg/l'},
        {'name': 'NH4', 'ut': 0.05, 'ul': 0.20, 'min': 0, 'max': 0.1, 'value': lambda s: s.total('[N-3]', 'mmol')*18, 'units': 'mg/l'}
        # {'name': 'E-coli', 'ul': 1.0, 'min': 0, 'max': 2},
        # {'name': 'Aeromonas 30°C', 'ut': 20, 'ul': 100, 'min': 0, 'max': 120},
        # {'name': 'Koloniegetal 22°C', 'ul': 100, 'min': 0, 'max': 150},
        # {'name': 'Na', 'ul': 100, 'min': 0, 'max': 120},
        # {'name': 'Cl', 'ut': 100, 'ul': 150, 'min': 0, 'max': 120},
        ]
    
        output = []
        for p in parameters:
            p['value'] = p['value'](self.solution)
    
        return parameters
        




    
    # @property
    # def mass(self):
    #     inflow = sum([c.flow for c in self.upstream_connections['product']])
    #     return -self.solution.total('Na') * inflow
