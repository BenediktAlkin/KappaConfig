import unittest

from kappaconfig.functional.load import from_string
from kappaconfig.resolvers.resolver import Resolver
from kappaconfig.resolvers.processors.remove_vars_post_processor import RemoveVarsPostProcessor
from kappaconfig.resolvers.scalar_resolvers.interpolation_resolver import InterpolationResolver

class TestRemoveVarsPostProcessor(unittest.TestCase):
    def resolve_and_assert(self, yaml_str, expected):
        kc_obj = from_string(yaml_str)
        resolver = Resolver(
            post_processors=[RemoveVarsPostProcessor()],
            default_scalar_resolver=InterpolationResolver(),
        )
        actual = resolver.resolve(kc_obj)
        self.assertEqual(expected, actual)

    def test_simple(self):
        yaml_str = """
        vars:
          x: 5
        value: ${vars.x}
        """
        expected = dict(value=5)
        self.resolve_and_assert(yaml_str, expected)