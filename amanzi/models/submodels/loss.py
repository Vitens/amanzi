class Loss:
    @property
    def equations(self):
        equations = []

        # upstream equals downstream
        eq1 = [c.eq(self.minorloss_percentage) for c in self.upstream_connections['product']]
        eq2 = [c.eq(-1) for c in self.downstream_connections['product']]
        equations.append([ eq1 + eq2, self.minorloss])
        
        # backwash in equals loss times sum of inputs
        eq3 = [c.eq(self.loss) for c in self.upstream_connections['product']]
        eq4 = [c.eq(-1) for c in self.upstream_connections.get('flush', [])]        
        equations.append([eq3 + eq4, 0])
        
        # backwash out equals loss times sum of inputs
        eq5 = [c.eq(self.loss) for c in self.upstream_connections['product']]
        eq6 = [c.eq(-1) for c in self.downstream_connections.get("waste",[])]
        equations.append([ eq5 + eq6, 0])
        
        return equations