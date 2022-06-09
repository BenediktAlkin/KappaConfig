import sys
import unittest
import kappaconfig.functional.load as load
from kappaconfig.resolvers.resolver import Resolver

class TestLoad(unittest.TestCase):
    @staticmethod
    def _basic_yaml_dict():
        return dict(
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

    def test_from_file_uri(self):
        expected = self._basic_yaml_dict()
        actual = Resolver().resolve(load.from_file_uri("tests_unit/res/basic.yaml"))
        self.assertEqual(expected, actual)

    def test_from_string(self):
        expected = self._basic_yaml_dict()
        with open("tests_unit/res/basic.yaml") as f:
            input_ = f.read()
        actual = Resolver().resolve(load.from_string(input_))
        self.assertEqual(expected, actual)

    def test_from_cli(self):
        # remove any potential arguments (from other tests or unittest runner)
        sys.argv = sys.argv[:1]
        sys.argv.append("some.object.key=value")
        expected = dict(some=dict(object=dict(key="value")))
        actual = Resolver().resolve(load.from_cli())
        self.assertEqual(expected, actual)