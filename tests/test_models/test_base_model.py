#!/usr/bin/python3

"""A unit test module that tests the BaseModel class"""

from datetime import datetime
from io import StringIO
from models.base_model import BaseModel
import unittest
from unittest.mock import patch


class TestBaseModel(unittest.TestCase):
    """
    a class that implements functions that run test cases
    over the BaseModel class
    """

    def test_instance(self):
        obj = BaseModel()
        # Test obj type
        self.assertTrue(isinstance(obj, BaseModel))

        # Test __str__ output
        res = f'[{type(obj).__name__}] ({obj.id}) {obj.__dict__}'
        with patch('sys.stdout', new=StringIO()) as str_out:
            print(obj)
            self.assertEqual(str_out.getvalue(), res)

    def test_attrs(self):
        """Test assigned id"""
        new = BaseModel()
        time_now = datetime.now()

        # Test ID
        self.assertIsNotNone(new.id)
        self.assertTrue(isinstance(new.id, str))

        # Test Created_at
        self.assertIsNotNone(new.created_at)
        self.assertTrue(isinstance(new.created_at, datetime))

        # Test Updated_at
        self.assertIsNotNone(new.updated_at)
        self.assertTrue(isinstance(new.updated_at, datetime))
