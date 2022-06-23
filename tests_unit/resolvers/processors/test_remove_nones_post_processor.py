import unittest

from kappaconfig.functional.load import from_string
from kappaconfig.resolvers.resolver import Resolver
from kappaconfig.resolvers.processors.remove_nones_post_processor import RemoveNonesPostProcessor
import kappaconfig.errors as errors

class TestRemoveVarsPostProcessor(unittest.TestCase):
    def resolve_and_assert(self, yaml_str, expected):
        kc_obj = from_string(yaml_str)
        resolver = Resolver(post_processors=[RemoveNonesPostProcessor()])
        actual = resolver.resolve(kc_obj)
        self.assertEqual(expected, actual)

    def test_empty_scalar(self):
        yaml_str = """
        null
        """
        expected = errors.empty_result()
        with self.assertRaises(type(expected)) as ex:
            self.resolve_and_assert(yaml_str, expected)
        self.assertEqual(expected.args[0], str(ex.exception))

    def test_empty_dict(self):
        yaml_str = """
        value: null
        """
        expected = {}
        self.resolve_and_assert(yaml_str, expected)

    def test_empty_list(self):
        yaml_str = """
        - null
        """
        expected = []
        self.resolve_and_assert(yaml_str, expected)

    def test_simple(self):
        yaml_str = """
        some:
          value: null
          other: 5
          asdf:
          - 3
          - null
        """
        expected = dict(
            some=dict(
                other=5,
                asdf=[3],
            )
        )
        self.resolve_and_assert(yaml_str, expected)