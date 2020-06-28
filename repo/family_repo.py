from utility.singleton import Singleton


class FamilyRepo(metaclass=Singleton):

    def __init__(self):
        self.family_members = dict()
        self.families = dict()

    def add_family_member(self, member_obj):
        if member_obj.name in self.family_members:
            return False

        self.family_members[member_obj.name] = member_obj
        return True

    def add_family(self, family_obj):
        if family_obj.id in self.families:
            return False

        self.families[family_obj.id] = family_obj
        return True

    def get_member(self, name):
        return self.family_members.get(name)

    def get_family(self, id):
        return self.families.get(id)