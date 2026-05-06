class Balance:
    @property
    def equations(self):
        # all ingoing streams must match all outgoing streams
        # return [[[c.eq(1) for c in self.connections['product']] + [c.eq(-1) for c in self.connections['product']], 0]]
        equations = []

        # all ingoing streams must match all outgoing streams

        # upstream equals downstream
        if 'product' in self.upstream_connections:
            eq1 = [c.eq(1) for c in self.upstream_connections['product']]
            eq2 = [c.eq(-1) for c in self.downstream_connections['product']]
        elif 'waste' in self.upstream_connections:
            eq1 = [c.eq(1) for c in self.upstream_connections['waste']]
            eq2 = [c.eq(-1) for c in self.downstream_connections['waste']]

        equations.append([ eq1 + eq2, 0])
        
        return equations