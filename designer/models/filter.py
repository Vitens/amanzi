from .model import Model

class Filter(Model):
    def __init__(self, config, loss=0.1):
        super().__init__(config)
        self.loss = loss

    @property
    def equations(self):
        equations = []
        # output equal sum of inputs
        lc1 = [c.eq(1) for c in self.connections['left']]
        lc2 = [c.eq(-1) for c in self.connections['right']]
        equations.append([ lc1 + lc2, 0])
        
        # backwash in equals loss times sum of inputs
        lc3 = [c.eq(self.loss) for c in self.connections['left']]
        lc4 = [c.eq(-1) for c in self.connections.get("top",[])]        
        equations.append([lc3 + lc4, 0])
        
        # backwash out equals loss times sum of inputs
        lc5 = [c.eq(self.loss) for c in self.connections['left']]
        lc6 = [c.eq(-1) for c in self.connections.get("bottom",[])]
        equations.append([ lc5 + lc6, 0])
        
        return equations    
        
    
        