from abc import abstractmethod, ABC

from repo.family_repo import FamilyRepo
from family_tree_exceptions import *
from constants import *


class Member(ABC):

    def __init__(self, name, gender, mother=None, father=None):
        self.name = name
        self.gender = gender
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

    def get_spouse_name(self):
        if not self.family_id:
            raise SpouseNotExist()
        spouse_name = self.family_id.replace(self.name, '').replace('$$', '')
        return spouse_name

    def get_spouse_obj(self):
        spouse_name = self.get_spouse_name()
        spouse_obj = FamilyRepo().get_member(spouse_name)
        return spouse_obj

    def get_parent_family_id(self):
        family_id = self.get_father_obj().family_id
        return family_id

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

    @abstractmethod
    def get_brothers(self):
        pass

    @abstractmethod
    def get_sisters(self):
        pass

    def get_siblings(self):
        return self.get_brothers() + self.get_sisters()


class FemaleMember(Member):

    def __init__(self, name, mother=None, father=None):
        super(FemaleMember, self).__init__(name, Gender.Female, mother, father)

    def get_brothers(self):
        father_obj = self.get_father_obj()
        brothers = father_obj.get_sons()
        return brothers

    def get_sisters(self):
        father_obj = self.get_father_obj()
        sisters = father_obj.get_daughters()
        sisters.remove(self.name)
        return sisters


class MaleMember(Member):

    def __init__(self, name, mother=None, father=None):
        super(MaleMember, self).__init__(name, Gender.Male, mother, father)

    def get_brothers(self):
        father_obj = self.get_father_obj()
        brothers = father_obj.get_sons()
        brothers.remove(self.name)
        return brothers

    def get_sisters(self):
        father_obj = self.get_father_obj()
        sisters = father_obj.get_daughters()
        return sisters


MemberClassMap = {
    Gender.Male: MaleMember,
    Gender.Female: FemaleMember
}