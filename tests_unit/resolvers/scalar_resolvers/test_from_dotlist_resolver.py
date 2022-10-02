import unittest

import kappaconfig.errors as errors
from kappaconfig.functional.load import from_string
from kappaconfig.resolvers.resolver import Resolver
from kappaconfig.resolvers.scalar_resolvers.from_dotlist_resolver import FromDotlistResolver
from tests_unit.util.trace import simulated_trace


class TestFromDotlistResolver(unittest.TestCase):
    @staticmethod
    def _resolve(source):
        resolver = Resolver(
            scalar_resolvers=dict(
                from_dotlist=FromDotlistResolver()
            ),
        )
        return resolver.resolve(from_string(source))

    def _resolve_and_assert(self, source, expected):
        actual = self._resolve(source)
        self.assertEqual(expected, actual)

    def test_simple(self):
        input_ = """
        somekey: ${from_dotlist:value=3}
        """
        expected = dict(somekey=dict(value=3))
        self._resolve_and_assert(input_, expected)

    def test_multiple(self):
        input_ = """
        somekey: ${from_dotlist:value=3 some.obj=2 some.key=value}
        """
        expected = dict(
            somekey=dict(
                value=3,
                some=dict(
                    obj=2,
                    key="value",
                ),
            ),
        )
        self._resolve_and_assert(input_, expected)

    def test_excess_spaces(self):
        source = """
        somekey: ${from_dotlist:value=3  other=2}
        """
        expected = errors.dotlist_resolver_empty_entry("value=3  other=2", simulated_trace("somekey"))
        with self.assertRaises(type(expected)) as ex:
            self._resolve(source)
        self.assertEqual(expected.args[0], str(ex.exception))
