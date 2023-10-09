#!/usr/bin/python3

"""A unit test module that tests the BaseModel class"""

from datetime import datetime
from io import StringIO
from models.base_model import BaseModel
from time import sleep
import unittest
from unittest.mock import patch
from uuid import uuid4


class TestBaseModel(unittest.TestCase):
    """
    a class that implements functions that run test cases
    over the BaseModel class
    """

    def test_instance(self):
        """Test Instance"""
        obj = BaseModel()

        # Test obj type
        self.assertTrue(isinstance(obj, BaseModel))

        # Test __str__ output
        res = f'[{type(obj).__name__}] ({obj.id}) {obj.__dict__}\n'
        with patch('sys.stdout', new=StringIO()) as str_out:
            print(obj)
            self.assertEqual(str_out.getvalue(), res)

    def test_attrs(self):
        """Test Assigned Attrs"""
        new = BaseModel()
        time_now = datetime.now().timestamp()

        # Test ID
        self.assertIsNotNone(new.id)
        self.assertTrue(isinstance(new.id, str))

        # Test Created_at
        self.assertIsNotNone(new.created_at)
        self.assertTrue(isinstance(new.created_at, datetime))
        self.assertAlmostEqual(new.created_at.timestamp(), time_now, delta=1)

        # Test Updated_at
        self.assertIsNotNone(new.updated_at)
        self.assertTrue(isinstance(new.updated_at, datetime))
        self.assertAlmostEqual(new.updated_at.timestamp(), time_now, delta=1)

        with self.assertRaises(TypeError):
            invalid_obj = BaseModel(1)

    def test_update_obj(self):
        """Test Updating Obj Attrs"""
        new = BaseModel()

        # Test Update ID
        old_ID = new.id
        new.id = uuid4()
        self.assertNotEqual(old_ID, new.id)

        # Test Update Created_at
        old_date = new.created_at
        new.created_at = datetime(2017, 9, 28, 21, 5, 54, 119427)
        self.assertNotEqual(old_date, new.created_at)

    def test_save_instance(self):
        """Test BaseModel Save Method"""
        new = BaseModel()

        old_date = new.updated_at

        new.my_name = "Selim"
        self.assertEqual(new.my_name, "Selim")

        sleep(0.05)
        new.save()

        self.assertNotEqual(old_date.timestamp(), new.updated_at.timestamp())

        with self.assertRaises(TypeError):
            new.save(2)

    def test_to_dict(self):
        """Test BaseModel to_dict Method"""
        new = BaseModel()

        res = new.__dict__
        model_dict = new.to_dict()

        self.assertDictEqual(model_dict, res)

        with self.assertRaises(TypeError):
            new.to_dict(2)
