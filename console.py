#!/usr/bin/python3

"""Module that defines main logic of the command interpreter."""

import cmd
import json
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage


class HBNBCommand(cmd.Cmd):
    """Class that represents the HBNB command line interpreter."""
    prompt = '(hbnb) '

    __available_models = {'BaseModel': BaseModel(), 'User': None, 'State': None,
                          'City': None, 'Amenity': None, 'Place': None, 'Review': None}

    __storage = FileStorage()
    __saved_objects = __storage.all()
    __saved_keys = __saved_objects.keys()

    def do_EOF(self, line):
        """Exits the program when ctrl-D is pressed."""
        return True

    def do_quit(self, line):
        """
        Quit command to exit the program.
        Ex: $ quit
        """
        return True

    def do_create(self, line):
        """
        Creates a new instance of BaseModel,
        saves it (to the JSON file) and prints the id.
        Ex: $ create BaseModel
        """
        args = line.split()
        if not args:
            print("** class name missing **")
            return
        if args[0] not in self.__available_models.keys():
            print("** class doesn't exist **")
            return

        new_instance = self.__available_models[line]
        new_instance.save()
        print(new_instance.id)

    def do_show(self, line):
        """
        Prints the string representation of an instance based on the class name and id.
        Ex: $ show BaseModel 1234-1234-1234
        """
        args = line.split()
        if not args:
            print("** class name missing **")
            return
        if args[0] not in self.__available_models.keys():
            print("** class doesn't exist **")
            return
        if len(args) < 2 or not args[1]:
            print("** instance id missing **")
            return

        instance_key = f'{args[0]}.{args[1]}'
        if instance_key not in self.__saved_keys:
            print("** no instance found **")
            return

        print(self.__saved_objects[instance_key])

    def do_destroy(self, line):
        """
        Deletes an instance based on the class name and id
        (save the change into the JSON file).
        Ex: $ destroy BaseModel 1234-1234-1234
        """
        args = line.split()
        if not args:
            print("** class name missing **")
            return
        if args[0] not in self.__available_models.keys():
            print("** class doesn't exist **")
            return
        if len(args) < 2 or not args[1]:
            print("** instance id missing **")
            return

        instance_key = f'{args[0]}.{args[1]}'
        if instance_key not in self.__saved_keys:
            print("** no instance found **")
            return

        del self.__saved_objects[instance_key]
        self.__storage.save()

    def do_all(self, line):
        """
        Prints all string representation of all instances based or not on the class name.
        Ex: $ all BaseModel or $ all
        """
        args = line.split() if line is not None else None
        if args and args[0] not in self.__available_models.keys():
            print("** class doesn't exist **")
            return
        objects_list = []
        if args:
            objects_list = [str(self.__saved_objects[key])
                            for key in self.__saved_keys if str(key).__contains__(args[0])]
        else:
            objects_list = [str(self.__saved_objects[key])
                            for key in self.__saved_keys]

        print(objects_list)

    def do_update(self, line):
        """
        Updates an instance based on the class name and id by adding or updating attribute
        (save the change into the JSON file).
        Ex: $ update BaseModel 1234-1234-1234
        """
        args = line.split()[:4]
        if not args:
            print("** class name missing **")
            return
        if args[0] not in self.__available_models.keys():
            print("** class doesn't exist **")
            return
        if len(args) < 2 or not args[1]:
            print("** instance id missing **")
            return

        instance_key = f'{args[0]}.{args[1]}'
        if instance_key not in self.__saved_keys:
            print("** no instance found **")
            return
        if len(args) < 3 or not args[2]:
            print("** attribute name missing **")
            return
        if len(args) < 4 or not args[3]:
            print("** value missing **")
            return

        try:
            if args[3].isdigit():
                args[3] = int(args[3])
            elif float(args[3]):
                args[3] = float(args[3])
            else:
                args[3] = str(args[3])
        except ValueError:
            pass

        self.__saved_objects[instance_key].__dict__[args[2]] = args[3]
        self.__saved_objects[instance_key].save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
