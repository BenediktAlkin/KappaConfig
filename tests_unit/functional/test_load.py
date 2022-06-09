import sys
import unittest
import kappaconfig.functional.load as load
from kappaconfig.resolvers.resolver import Resolver
from kappaconfig.functional.util import merge

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
        sys.argv = sys.argv[:1] + ["some.object.key=value", "some.alist=[1,2,asdf]"]
        expected = dict(
            some=dict(
                object=dict(key="value"),
                alist=[1, 2, "asdf"],
            ),
        )
        actual = Resolver().resolve(load.from_cli())
        self.assertEqual(expected, actual)

    def test_from_cli_merge(self):
        # remove any potential arguments (from other tests or unittest runner)
        sys.argv = sys.argv[:1] + ["some.object.key=value", "other=5", "some.alist=[1,2,asdf]"]
        yaml = """
        some:
          list:
            - will_be_overwritten
          other: 23
        """
        expected = dict(
            some=dict(
                object=dict(key="value"),
                alist=[1, 2, "asdf"],
            ),
            other=5,
        )
        cli = load.from_cli()
        merged = merge(load.from_string(yaml), cli)
        actual = Resolver().resolve(merged)
        self.assertEqual(expected, actual)