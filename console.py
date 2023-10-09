#!/usr/bin/python3

"""Module that defines main logic of the command interpreter"""

import cmd


class HBNBCommand(cmd.Cmd):
    """Class that represents the HBNB command line interpreter"""
    prompt = '(hbnb) '

    def do_EOF(self, line):
        return True

    def do_quit(self, line):
        """Quit command to exit the program"""
        return True


if __name__ == '__main__':
    HBNBCommand().cmdloop()
