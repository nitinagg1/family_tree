import sys
from family_tree import FamilyTree
from constants import *

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

parent_child = { "anga": ["chit", "ish", "vich", "aras", "satya"],
                "amba": ["dritha", "tritha", "vritha"],
                "vich": ["vila", "chika"],
                "chitra": ["jnki", "ahit"],
                "satya": ["asva", "vyas", "atya"],
                "dritha": ["yodhan"],
                "jnki": ["laki", "lavnya"],
                "satvy": ["vasa"],
                "krpi": ["kriya", "krithi"]
                }


def main():

    family_tree = FamilyTree()

    ## init family tree
    family_tree.initialise_family_tree(male_members, Gender.Male)
    family_tree.initialise_family_tree(female_members, Gender.Female)
    family_tree.set_husband_wife(husband_wife)
    family_tree.set_parent_children(parent_child)

    print (family_tree.get_relationship("atya", "Sister-In-Law".lower()))


if __name__ == "__main__":
    main()