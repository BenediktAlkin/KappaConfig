import unittest
import kappaconfig.functional.load as load
from kappaconfig.resolver import Resolver

class TestLoad(unittest.TestCase):
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
        actual = Resolver().resolve(load.from_file_uri("res/basic.yaml"))
        self.assertEqual(expected, actual)