import unittest

import yaml

import kappaconfig.functional.convert as convert
from kappaconfig.entities.wrappers import KCScalar, KCList, KCDict


class TestConvert(unittest.TestCase):
    def test_from_primitive_scalar_root(self):
        primitive = yaml.safe_load("""
        5
        """)
        converted = convert.from_primitive(primitive)
        self.assertEqual(5, converted.value)

    def test_from_primitive_list_root(self):
        primitive = yaml.safe_load("""
        - 5
        - 6
        """)
        converted = convert.from_primitive(primitive)
        self.assertEqual(5, converted[0].value)
        self.assertEqual(6, converted[1].value)

    def test_from_primitive_dict_root(self):
        primitive = yaml.safe_load("""
        some: value
        """)
        converted = convert.from_primitive(primitive)
        self.assertEqual("value", converted["some"].value)

    def test_from_primitive_nonstring_keys(self):
        primitive = yaml.safe_load("""
        5: intkey
        true: boolkey
        3.2: floatkey 
        """)
        converted = convert.from_primitive(primitive)
        self.assertEqual("intkey", converted[5].value)
        self.assertEqual("boolkey", converted[True].value)
        self.assertEqual("floatkey", converted[3.2].value)

    def test_to_primitive_scalar_root(self):
        root_node = KCScalar(5)
        expected = 5
        actual = convert.to_primitive(root_node)
        self.assertEqual(expected, actual)

    def test_to_primitive_list_root(self):
        root_node = KCList(5, 6)
        expected = [5, 6]
        actual = convert.to_primitive(root_node)
        self.assertEqual(expected, actual)

    def test_to_primitive_dict_root(self):
        root_node = KCDict(some="value")
        expected = dict(some="value")
        actual = convert.to_primitive(root_node)
        self.assertEqual(expected, actual)
