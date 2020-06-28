from member import Member, MemberClassMap
from constants import *
from repo.family_repo import FamilyRepo
from family_tree_exceptions import *
from family import Family
from relationships import RelationShipClassMap


class FamilyTree(object):

    @staticmethod
    def initialise_family_tree(members, sex):
        for member in members:
            member_cls = MemberClassMap.get(sex)
            new_member = member_cls(member)
            result = FamilyRepo().add_family_member(new_member)
            if not result:
                raise MemberAlreadyExists(name=new_member.name)

    @staticmethod
    def set_husband_wife(husband_wife_list):
        for husband, wife in husband_wife_list:
            husband_obj = FamilyRepo().get_member(husband)
            wife_obj = FamilyRepo().get_member(wife)
            if not husband_obj or not wife_obj:
                raise MemberNotFound()

            family_obj = Family(husband, wife)
            FamilyRepo().add_family(family_obj)
            husband_obj.set_family(family_obj.id)
            wife_obj.set_family(family_obj.id)

    @staticmethod
    def set_parent_children(parent_child):
        for parent in parent_child.keys():
            parent_obj = FamilyRepo().get_member(parent)
            if not parent_obj:
                raise MemberNotFound()

            if not parent_obj.family_id:
                raise SpouseNotExist()

            family_obj = FamilyRepo().get_family(parent_obj.family_id)
            husband, wife = family_obj.husband, family_obj.wife

            for child in parent_child[parent]:
                child_obj = FamilyRepo().get_member(child)
                child_obj.mother = wife
                child_obj.father = husband
                if child_obj.sex == Sex.Female:
                    family_obj.daughters.append(child_obj.name)
                else:
                    family_obj.sons.append(child_obj.name)

    @staticmethod
    def get_relationship(name, relationship):
        member = FamilyRepo().get_member(name)
        if not member:
            raise MemberNotFound()

        relationship_cls = RelationShipClassMap.get(relationship)
        if not relationship_cls:
            raise UnknownRelationship()

        return relationship_cls(member).get_relations()

