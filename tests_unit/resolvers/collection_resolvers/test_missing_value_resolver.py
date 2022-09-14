import unittest

import kappaconfig.errors as errors
from kappaconfig.functional.load import from_string
from kappaconfig.resolvers.collection_resolvers.missing_value_resolver import MissingValueResolver
from kappaconfig.resolvers.resolver import Resolver
from tests_unit.util.trace import simulated_trace


class TestMissingValueResolver(unittest.TestCase):
    def _resolve_and_assert(self, input_, expected):
        resolver = Resolver(collection_resolvers=[MissingValueResolver()])
        with self.assertRaises(type(expected)) as ex:
            resolver.resolve(from_string(input_))
        self.assertEqual(expected.args[0], str(ex.exception))

    def test_simple(self):
        input_ = """
        some_obj: ???
        """
        expected = errors.missing_value_error(simulated_trace("some_obj"))
        self._resolve_and_assert(input_, expected)
