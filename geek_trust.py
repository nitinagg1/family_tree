import sys
from meet_family import MeetFamily, CommandParser
from constants import *


def main():

    meet_family = MeetFamily()
    meet_family.initialise_family_tree()
    ## init family tree

    input_file = sys.argv[1]
    command_parser = CommandParser()
    with open(input_file, "r") as f:
        commands = f.readlines()
        for command in commands:
            command_parser.process_commands(command.strip())

if __name__ == "__main__":
    main()