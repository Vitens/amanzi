class Splitter:    
    @property
    def equations(self):
        equations = []
        # output_1 is equal to split * input
        equations.append([[c.eq(self.split) for c in self.anchors_connections['left']]+[c.eq(-1) for c in self.anchors_connections['right']], 0])
        # output_2 is equal to split * (1-input)
        equations.append([[c.eq(1-self.split) for c in self.anchors_connections['left']]+[c.eq(-1) for c in self.anchors_connections['bottom']], 0])
        return equations
