from abc import ABC, abstractmethod
from repo.family_repo import FamilyRepo
from family_tree_exceptions import *


class Relationships(ABC):

    def __init__(self, member_obj):
        self.member_obj = member_obj

    def get_brothers(self):
        pass

    @staticmethod
    def get_family_obj(family_id):
        if not family_id:
            raise FamilyNotFound()
        return FamilyRepo().get_family(family_id)

    @abstractmethod
    def get_relations(self):
        pass


class Son(Relationships):

    def __init__(self, member_obj):
        super(Son, self).__init__(member_obj)

    def get_relations(self):
        return self.member_obj.get_sons()


class Daughter(Relationships):

    def __init__(self, member_obj):
        super(Daughter, self).__init__(member_obj)

    def get_relations(self):
        return self.member_obj.get_daughters()


class Siblings(Relationships):

    def __init__(self, member_obj):
        super(Siblings, self).__init__(member_obj)

    def get_relations(self):
        return self.member_obj.get_siblings()


class PaternalUncle(Relationships):

    def __init__(self, member_obj):
        super(PaternalUncle, self).__init__(member_obj)

    def get_relations(self):
        father_obj = self.member_obj.get_father_obj()
        return father_obj.get_brothers()


class PaternalAunt(Relationships):

    def __init__(self, member_obj):
        super(PaternalAunt, self).__init__(member_obj)

    def get_relations(self):
        father_obj = self.member_obj.get_father_obj()
        return father_obj.get_sisters()


class MaternalUncle(Relationships):

    def __init__(self, member_obj):
        super(MaternalUncle, self).__init__(member_obj)

    def get_relations(self):
        mother_obj = self.member_obj.get_mother_obj()
        return mother_obj.get_brothers()


class MaternalAunt(Relationships):

    def __init__(self, member_obj):
        super(MaternalAunt, self).__init__(member_obj)

    def get_relations(self):
        mother_obj = self.member_obj.get_mother_obj()
        return mother_obj.get_sisters()


class SisterInLaw(Relationships):

    def __init__(self, member_obj):
        super(SisterInLaw, self).__init__(member_obj)

    def get_spouse_sisters(self):
        in_laws = []
        try:
            spouse_obj = self.member_obj.get_spouse_obj()
            in_laws += spouse_obj.get_sisters()

        except SpouseNotExist as e:
            pass

        return in_laws

    def get_spouse_of_brothers(self):
        in_laws = []
        brothers = self.member_obj.get_brothers()
        for brother in brothers:
            try:
                brother_obj = FamilyRepo().get_member(brother)
                spouse = brother_obj.get_spouse_name()
                in_laws.append(spouse)
            except SpouseNotExist:
                pass

        return in_laws

    def get_relations(self):
        return self.get_spouse_of_brothers() + self.get_spouse_sisters()


class BrotherInLaw(Relationships):

    def __init__(self, member_obj):
        super(BrotherInLaw, self).__init__(member_obj)

    def get_spouse_brothers(self):
        in_laws = []
        spouse_obj = self.member_obj.get_spouse_obj()
        try:
            in_laws += spouse_obj.get_brothers()
        except SpouseNotExist:
            pass

        return in_laws

    def get_spouse_of_sisters(self):
        in_laws = []
        sisters = self.member_obj.get_sisters()
        for sister in sisters:
            try:
                sister_obj = FamilyRepo().get_member(sister)
                spouse = sister_obj.get_spouse_name()
                in_laws.append(spouse)
            except SpouseNotExist:
                pass

        return in_laws

    def get_relations(self):
        return self.get_spouse_brothers() + self.get_spouse_of_sisters()


RelationShipClassMap = {
    'son': Son,
    'daughter': Daughter,
    'siblings': Siblings,
    'paternal-uncle': PaternalUncle,
    'maternal-uncle': MaternalUncle,
    'paternal-aunt': PaternalAunt,
    'maternal-aunt': MaternalAunt,
    'sister-in-law': SisterInLaw,
    'brother-in-law': BrotherInLaw
}

