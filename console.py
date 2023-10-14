#!/usr/bin/python3

"""Module that defines main logic of the command interpreter."""

from ast import literal_eval
import cmd
from models.base_model import BaseModel
from models import storage
import re
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """Class that represents the
    HBNB command line interpreter."""
    prompt = '(hbnb) '

    __available_models = {
        'BaseModel': BaseModel,
        'User': User,
        'State': State,
        'City': City,
        'Amenity': Amenity,
        'Place': Place,
        'Review': Review
    }

    def onecmd(self, line):
        args = line.split('.')
        if len(args) > 1:
            self.do_class_method(args[0] if args[0] else "", args[1])
            return

        return super().onecmd(line)

    def do_class_method(self, class_name, args):
        """
        a special internal method that executes
        some special commands
        """
        methods_dict = {
            "all": self.do_all,
            "count": self.do_count,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "update": self.do_update
        }

        method, line = extract_method_line(class_name, args)
        if isinstance(method, dict):
            update_dict = method
            _id = line
            for key, item in update_dict.items():
                methods_dict['update'](
                    f'{class_name} {_id} {key} {item}')
            return

        methods_dict[method](line)

    def emptyline(self):
        pass

    def do_EOF(self, line):
        """Exits the program when ctrl-D is pressed."""
        return True

    def do_quit(self, line):
        """
        Quit command to exit the program.
        Ex: $ quit
        """
        return True

    def do_count(self, line):
        """
        Prints the number of instance of a class
        Ex: $ count BaseModel
        """
        args = line.split()
        if not validate_args(args, HBNBCommand.__available_models):
            return

        _, saved_keys = get_saved_objs()
        count = len([x for x in saved_keys if
                    str(x).__contains__(args[0])])
        print(count)

    def do_create(self, line):
        """
        Creates a new instance of BaseModel,
        saves it (to the JSON file) and prints the id.
        Ex: $ create BaseModel
        """
        args = line.split()
        if not validate_args(args, HBNBCommand.__available_models):
            return

        new_instance = HBNBCommand.__available_models[line]()
        new_instance.save()
        print(new_instance.id)

    def do_show(self, line):
        """
        Prints the string representation of an
        instance based on the class name and id.
        Ex: $ show BaseModel 1234-1234-1234
        """
        args = line.split()
        saved_objects, saved_keys = get_saved_objs()
        if not validate_args(
                args,
                HBNBCommand.__available_models,
                saved_keys,
                check_id=True
        ):
            return

        instance_key = f'{args[0]}.{args[1]}'
        print(saved_objects[instance_key])

    def do_destroy(self, line):
        """
        Deletes an instance based on the class name and id
        (save the change into the JSON file).
        Ex: $ destroy BaseModel 1234-1234-1234
        """
        args = line.split()
        saved_objects, saved_keys = get_saved_objs()
        if not validate_args(
                args, HBNBCommand.__available_models,
                saved_keys, check_id=True
        ):
            return

        instance_key = f'{args[0]}.{args[1]}'
        del saved_objects[instance_key]
        storage.save()

    def do_all(self, line):
        """
        Prints all string representation of all
        instances based or not on the class name.
        Ex: $ all BaseModel or $ all
        """
        args = line.split() if line is not None else None
        saved_objects, saved_keys = get_saved_objs()
        if (args and
                args[0] not in
                HBNBCommand.__available_models.keys()):
            print("** class doesn't exist **")
            return

        objects_list = []
        if args:
            objects_list = [str(saved_objects[key])
                            for key in saved_keys if
                            str(key).__contains__(args[0])]
        else:
            objects_list = [str(saved_objects[key])
                            for key in saved_keys]

        print(objects_list)

    def do_update(self, line):
        """
        Updates an instance based on the
        class name and id by adding or updating attribute
        (save the change into the JSON file).
        Ex: $ update User 1234-1234-1234 name "John"
        """
        args = line.split()[:4]
        saved_objects, saved_keys = get_saved_objs()
        if not validate_args(
                args,
                HBNBCommand.__available_models,
                saved_keys,
                check_id=True,
                check_attrs=True
        ):
            return

        instance_key = f'{args[0]}.{args[1]}'

        args_no_quotes = remove_excess_quotes(args[3])
        saved_objects[instance_key].__dict__[args[2]] = args_no_quotes
        storage.save()


def remove_excess_quotes(line):
    """Removes any excessive quotes in a string input"""
    line_no_quotes = re.sub(r'\"|\'', "", line)
    try:
        if line_no_quotes.isdigit():
            line_no_quotes = int(line_no_quotes)
        elif float(line_no_quotes):
            line_no_quotes = float(line_no_quotes)
    except ValueError:
        pass
    return line_no_quotes


def extract_method_line(class_name, args):
    """Extracts the command to invoke
    and its passed line of arguments"""
    args = args[:-1]
    method, params = args.split('(')

    # check if input is a dictionary for update method
    index = params.find('{')
    update_dict = None
    if index != -1:
        update_dict = literal_eval(params[index:])

    params = str(params).split(", ")
    params = list(map(remove_excess_quotes, params))
    if update_dict is not None:
        return update_dict, params[0]
    params = " ".join(params)
    line = f'{class_name} {params}'
    return method, line


def get_saved_objs():
    """Returns all the previously
    saved objects and their keys"""
    saved_objects = storage.all()
    saved_keys = saved_objects.keys()
    return (saved_objects, saved_keys)


def validate_args(
    args,
    models,
    saved_keys=None,
    check_id=False,
    check_attrs=False
):
    """validates the arguments passed to each command"""
    if not args:
        print("** class name missing **")
        return False
    if args[0] not in models:
        print("** class doesn't exist **")
        return False

    if check_id:
        instance_key = f'{args[0]}.{args[1]}'
        if len(args) < 2 or not args[1]:
            print("** instance id missing **")
            return False
        if instance_key not in saved_keys:
            print("** no instance found **")
            return False
    if check_attrs:
        if len(args) < 3 or not args[2]:
            print("** attribute name missing **")
            return False
        if len(args) < 4 or not args[3]:
            print("** value missing **")
            return False
    return True


if __name__ == '__main__':
    HBNBCommand().cmdloop()
