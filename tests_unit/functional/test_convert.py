import unittest
import kappaconfig.functional.convert as convert
import yaml


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
        self.assertEqual(5, converted[0])
        self.assertEqual(6, converted[1])

    def test_from_primitive_dict_root(self):
        primitive = yaml.safe_load("""
        some: value
        """)
        converted = convert.from_primitive(primitive)
        self.assertEqual("value", converted["some"])