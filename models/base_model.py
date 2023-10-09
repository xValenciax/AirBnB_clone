#!usr/bin/python3

"""Module that defines BaseModel class"""

from uuid import uuid4
from datetime import datetime


class BaseModel:
    """
    represents the base for all other
    coming models to inherit from
    """

    def __init__(self):
        """
        initializes a new instance of BaseModel
        with some instance attributes
        """
        self.id = str(uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def __str__(self):
        """returns a string representation of the current instance"""
        return f'[{type(self).__name__}] ({self.id}) {self.__dict__}'

    def save(self):
        """
        updates the public instance attribute updated_at
        with the current datetime
        """
        self.updated_at = datetime.now()

    def to_dict(self):
        """
        returns a dictionary containing all
        keys/values of __dict__ of the instance
        """
        instance_dict = self.__dict__
        instance_dict['__class__'] = type(self).__name__
        instance_dict['created_at'] = self.created_at.isoformat()
        instance_dict['updated_at'] = self.updated_at.isoformat()

        return instance_dict
