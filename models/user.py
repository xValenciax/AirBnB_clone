#!/usr/bin/python3

"""Defines the BaseModel class."""
from models.base_model import BaseModel


class User(BaseModel):
    """Represents HBNB user"""
    email = ""
    password = ""
    first_name = ""
    last_name = ""
