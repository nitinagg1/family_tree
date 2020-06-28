from repo.family_repo import FamilyRepo
from family_tree_exceptions import *


class Member(object):

    def __init__(self, name, sex, mother=None, father=None):
        self.name = name
        self.sex = sex
        self.mother = mother
        self.father = father
        self.family_id = None

    def set_family(self, family_id):
        self.family_id = family_id

    def get_family_id(self):
        return self.family_id

    def get_father(self):
        return self.father

    def get_mother(self):
        return self.mother

    def get_parental_grand_father(self):
        return self.get_father_obj().father

    def get_maternal_grand_father(self):
        return self.get_mother_obj().father

    def get_father_obj(self):
        father_obj = FamilyRepo().get_member(self.father)
        if not father_obj:
            raise MemberNotFound()
        return father_obj

    def get_mother_obj(self):
        mother_obj = FamilyRepo().get_member(self.mother)
        if not mother_obj:
            raise MemberNotFound()
        return mother_obj

    def get_parent_family_id(self):
        family_id = self.get_father_obj().family_id
        return family_id

    def get_brothers(self):
        family_obj = self.get_parent_family_obj()
        brothers = family_obj.get_sons()
        try:
            brothers.remove(self.name)
        except:
            pass
        return brothers

    def get_sisters(self):
        family_obj = self.get_parent_family_obj()
        sisters = family_obj.get_daughters()
        try:
            sisters.remove(self.name)
        except:
            pass
        return sisters

    def get_siblings(self):
        return self.get_brothers() + self.get_sisters()

    def get_sons(self):
        if not self.family_id:
            raise FamilyNotFound()
        family_obj = FamilyRepo().get_family(self.family_id)
        return family_obj.get_sons()

    def get_daughters(self):
        if not self.family_id:
            raise FamilyNotFound()
        family_obj = FamilyRepo().get_family(self.family_id)
        return family_obj.get_sons()

    def get_spouse(self):
        if not self.family_id:
            raise SpouseNotExist()
        spouse_name = self.family_id.replace(self.name, '').replace('$$', '')
        return spouse_name
