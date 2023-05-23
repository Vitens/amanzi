class Balance:
    @property
    def equations(self):
        # all ingoing streams must match all outgoing streams
        # return [[[c.eq(1) for c in self.connections['product']] + [c.eq(-1) for c in self.connections['product']], 0]]
        equations = []
        # upstream equals downstream
        eq1 = [c.eq(self.minorloss_percentage) for c in self.upstream_connections['product']]
        eq2 = [c.eq(-1) for c in self.downstream_connections['product']]
        equations.append([ eq1 + eq2, self.minorloss])        
        
        return equations