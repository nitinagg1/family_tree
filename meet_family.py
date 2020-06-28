from member import Member, MemberClassMap
from constants import *
from repo.family_repo import FamilyRepo
from family_tree_exceptions import *
from family import Family
from relationships import RelationShipClassMap


male_members = ["shan", "chit", "vich", "ish", "aras", "vyan", "jaya", "vritha", "arit", "ahit", "asva", "vyas",
                "yodhan", "laki", "vasa", "kriya"]
female_members = ["anga", "amba", "lika", "chitra", "satya", "dritha", "tritha", "vila", "chika", "jnki",
                  "satvy", "krpi", "atya", "lavnya", "krithi"]

husband_wife = [["shan", "anga"],
                ["chit", "amba"],
                ["vich", "lika"],
                ["aras", "chitra"],
                ["vyan", "satya"],
                ["jaya", "dritha"],
                ["arit", "jnki"],
                ["asva", "satvy"],
                ["vyas", "krpi"]
                ]

parent_childs = { "anga": ["chit", "ish", "vich", "aras", "satya"],
                "amba": ["dritha", "tritha", "vritha"],
                "vich": ["vila", "chika"],
                "chitra": ["jnki", "ahit"],
                "satya": ["asva", "vyas", "atya"],
                "dritha": ["yodhan"],
                "jnki": ["laki", "lavnya"],
                "satvy": ["vasa"],
                "krpi": ["kriya", "krithi"]
                }


class MeetFamily(object):


    @staticmethod
    def initialise_family_tree():
        MeetFamily.add_members(male_members, Gender.Male)
        MeetFamily.add_members(female_members, Gender.Female)
        MeetFamily.set_husband_wife(husband_wife)
        MeetFamily.set_parent_children(parent_childs)

    @staticmethod
    def add_members(members, gender):
        for member in members:
            member_cls = MemberClassMap.get(gender.value.lower())
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
    def set_parent_children(parent_children):
        for parent in parent_children.keys():
            parent_obj = FamilyRepo().get_member(parent)
            if not parent_obj:
                raise MemberNotFound()

            if not parent_obj.family_id:
                raise SpouseNotExist()

            family_obj = FamilyRepo().get_family(parent_obj.family_id)
            husband, wife = family_obj.husband, family_obj.wife

            for child in parent_children[parent]:
                child_obj = FamilyRepo().get_member(child)
                child_obj.mother = wife
                child_obj.father = husband
                child_obj.get_added_to_family(family_obj)

    @staticmethod
    def get_relationship(*args):
        name = args[0]
        relationship = args[1]
        member = FamilyRepo().get_member(name)
        if not member:
            raise MemberNotFound()

        relationship_cls = RelationShipClassMap.get(relationship)
        if not relationship_cls:
            raise UnknownRelationship()

        return relationship_cls(member).get_relations()

    @staticmethod
    def add_child(*args):
        member_cls = MemberClassMap.get(args[2])
        child = member_cls(args[1])
        parent_obj = FamilyRepo().get_member(args[0])
        if not parent_obj:
            raise MemberNotFound()
        parent_obj.add_child(child)
        return ["CHILD_ADDITION_SUCCEEDED"]


class CommandParser(object):

    CMD_METHOD_MAPPING = {
        'add_child': MeetFamily.add_child,
        'get_relationship': MeetFamily.get_relationship
    }

    def process_commands(self, command):
        command = command.lower().split(' ')
        command_name = command[0]
        method = self.CMD_METHOD_MAPPING.get(command_name)
        if method:
            try:
                response = method(*command[1:])
                if not response:
                    print("NONE")
                else:
                    print(" ".join(response).title())
            except FamilyTreeException as fe:
                print(fe.get_error_message())
        else:
            print('command not Found')

