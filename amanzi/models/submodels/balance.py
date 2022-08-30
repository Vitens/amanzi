class Balance:
    @property
    def equations(self):
        # all ingoing streams must match all outgoing streams
        return [[[c.eq(1) for c in self.connections['left']]+[c.eq(-1) for c in self.connections['right']], 0]]