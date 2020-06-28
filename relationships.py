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
        family_id = self.member_obj.get_family_id()
        family_obj = self.get_family_obj(family_id)
        return family_obj.get_sons()


class Daughter(Relationships):

    def __init__(self, member_obj):
        super(Daughter, self).__init__(member_obj)

    def get_relations(self):
        family_id = self.member_obj.get_family_id()
        family_obj = self.get_family_obj(family_id)
        return family_obj.get_daughters()


class Siblings(Relationships):

    def __init__(self, member_obj):
        super(Siblings, self).__init__(member_obj)

    def get_relations(self):
        family_id = self.member_obj.get_parent_family_id()
        family_obj = self.get_family_obj(family_id)
        children = family_obj.children()
        children.remove(self.member_obj.name)
        return children


class PaternalFamily(Relationships):

    def __init__(self, member_obj):
        super(PaternalFamily, self).__init__(member_obj)

    def get_paternal_family(self):
        father_obj = self.member_obj.get_father_obj()
        grandfather_obj = self.father_obj.get_father_obj()
        family_obj = FamilyRepo().get_family(grandfather_obj.family_id)
        return family_obj, father_obj.name


class PaternalUncle(PaternalFamily):

    def __init__(self, member_obj):
        super(PaternalUncle, self).__init__(member_obj)

    def get_relations(self):
        family_obj, father = self.get_paternal_family()
        uncles = family_obj.get_sons(father)
        return uncles


class PaternalAunt(PaternalFamily):

    def __init__(self, member_obj):
        super(PaternalUncle, self).__init__(member_obj)

    def get_relations(self):
        family_obj, father = self.get_paternal_family()
        aunts = family_obj.get_daughters()
        return aunts


class MaternalFamily(Relationships):

    def __init__(self, member_obj):
        super(MaternalFamily, self).__init__(member_obj)

    def get_maternal_family(self):
        mother_obj = self.member_obj.get_mother_obj()
        grandfather_obj = self.mother_obj.get_father_obj()
        family_obj = FamilyRepo().get_family(grandfather_obj.family_id)
        return family_obj, mother_obj.name


class MaternalUncle(MaternalFamily):

    def __init__(self, member_obj):
        super(MaternalUncle, self).__init__(member_obj)

    def get_relations(self):
        family_obj, mother = self.get_maternal_family()
        uncles = family_obj.get_sons()
        return uncles


class MaternalAunt(MaternalFamily):

    def __init__(self, member_obj):
        super(MaternalAunt, self).__init__(member_obj)

    def get_relations(self):
        family_obj, mother = self.get_maternal_family()
        aunts = family_obj.get_daughters()
        aunts.remove(mother)
        return aunts


class SisterInLaw(Relationships):

    def __init__(self, member_obj):
        super(SisterInLaw, self).__init__(member_obj)

    def get_spouse_sisters(self):
        in_laws = []
        try:
            spouse = self.member_obj.get_spouse()
            spouse_obj = FamilyRepo().get_member(spouse)
            in_laws = []
            try:
                family_id = spouse_obj.get_parent_family_id()
                family_obj = self.get_family_obj(family_id)
                in_laws += family_obj.get_daughters()
                try:
                    in_laws.remove(spouse_obj.name)
                except:
                    pass
            except FamilyNotFound as e:
                pass

        except SpouseNotExist as e:
            pass

        return in_laws

    def get_spouse_of_brothers(self):
        in_laws = []
        family_id = self.member_obj.get_parent_family_id()
        family_obj = FamilyRepo().get_family(family_id)
        brothers = family_obj.get_sons()
        try:
            brothers.remove(self.member_obj.name)
        except:
            pass
        for brother in brothers:
            try:
                brother_obj = FamilyRepo().get_member(brother)
                spouse = brother_obj.get_spouse()
                in_laws.append(spouse)
            except SpouseNotExist as e:
                pass

        return in_laws

    def get_relations(self):
        return self.get_spouse_of_brothers() + self.get_spouse_sisters()

class BrotherInLaw(Relationships):

    def __init__(self, member_obj):
        super(BrotherInLaw, self).__init__(member_obj)

    def get_spouse_brothers(self):
        in_laws = []
        try:
            spouse = self.member_obj.get_spouse()
            spouse_obj = FamilyRepo().get_member(spouse)
            in_laws = []
            try:
                family_id = spouse_obj.get_parent_family_id()
                family_obj = self.get_family_obj(family_id)
                in_laws += family_obj.get_sons()
                try:
                    in_laws.remove(spouse_obj.name)
                except:
                    pass
            except FamilyNotFound as e:
                pass
        except SpouseNotExist as e:
            pass

        return in_laws

    def get_spouse_of_sisters(self):
        in_laws = []
        family_id = self.member_obj.get_parent_family_id()
        family_obj = FamilyRepo().get_family(family_id)
        brothers = family_obj.get_sons()
        try:
            brothers.remove(self.member_obj.name)
        except:
            pass
        for brother in brothers:
            try:
                brother_obj = FamilyRepo().get_member(brother)
                spouse = brother_obj.get_spouse()
                in_laws.append(spouse)
            except SpouseNotExist as e:
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

