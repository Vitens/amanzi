class Connection:
    num = 0
    def __init__(self, fro, to):
        self.num = Connection.num
        Connection.num+=1
        self.to = to
        self.fro = fro

        # print(f"Going from {self.fro} <-> {self.to}")

    @property
    def name(self):
        return "{} -> {}".format(self.fro.uid, self.to.uid)
    
    def __repr__(self):
        return "<connection {} -> {} >".format(self.fro.uid, self.to.uid)
    
    def eq(self,factor):
        return [self, factor]