

class Family(object):
    FAMILY_ID = '{husband}$${wife}'

    def __init__(self, husband, wife):
        self.id = self.FAMILY_ID.format(husband=husband, wife=wife)
        self.husband = husband
        self.wife = wife
        self.sons = []
        self.daughters = []

    def get_sons(self):
        return self.sons

    def get_daughters(self):
        return self.daughters

    def get_children(self):
        return self.sons + self.daughters