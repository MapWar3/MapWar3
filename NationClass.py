class Nation:  # To initialize, type: x = Nation()
    def __init__(self, production=0, technology=0, trade=0, resources=0, overspent=0, name='', leader=''):
        self.Production = production # Now you can say something like Bob.production
        self.Technology = technology
        self.Trade = trade
        self.Resources = resources
        self.Overspent = overspent
        self.NationName = name
        self.LeaderName = leader
    def resourcecompute(self):
        self.Resources += int(round(BR + self.Production + self.Technology*TEM + self.Trade*TRM - self.Resources**RDE*RDC - self.Overspent*OPM, 0))
    def resourceprint(self):
        pass # Osmotischen will work on this later.