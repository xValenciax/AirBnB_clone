#!/usr/bin/python3
"""Defines the FileStorage class."""

import json
from models.base_model import BaseModel


class FileStorage:
    """Represent an abstracted storage engine.

    Attributes:
        __file_path (str): The name of the file to save objects to.
        __objects (dict): A dictionary of instantiated objects.
    """
    __file_path = "storage.json"
    __objects = {}

    def all(self):
        """Return the dictionary __objects."""
        return FileStorage.__objects

    def new(self, obj):
        """Set in __objects obj with key <obj_class_name>.id"""
        obj_class_name = obj.__class__.__name__
        FileStorage.__objects[f"{obj_class_name}.{obj.id}"] = obj

    def save(self):
        """Serialize __objects to the JSON file __file_path."""
        saved_objs_dict = FileStorage.__objects
        objs_dict = {obj: saved_objs_dict[obj].to_dict()
                     for obj in saved_objs_dict.keys()}

        with open(FileStorage.__file_path, "w") as f:
            json.dump(objs_dict, f)

    def reload(self):
        """Deserialize the JSON file __file_path to __objects, if it exists."""
        available_models = {'BaseModel': BaseModel, 'User': None, 'State': None,
                            'City': None, 'Amenity': None, 'Place': None, 'Review': None}

        try:
            with open(FileStorage.__file_path, 'r') as f:
                print("okay")
                obj_dict = json.load(f)
                for o in obj_dict.values():
                    cls_name = o["__class__"]
                    del o["__class__"]
                    self.new(available_models[cls_name](**o))
        except (FileNotFoundError, FileExistsError):
            return
