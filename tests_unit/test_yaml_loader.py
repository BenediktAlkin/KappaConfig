import unittest
import kappaconfig as kc

class TestYamlLoader(unittest.TestCase):
    def test_basic_load(self):
        expected = dict(
            some_string="some_value",
            some_int=5,
            some_double=5.,
            some_list=["a", "b", "c", 5],
            some_dict=dict(
                some_nested_dict=dict(
                    some_nested_dict_value=5
                )
            ),
        )
        actual = kc.YamlLoader.from_uri("res/basic.yaml")
        self.assertEqual(expected, actual)