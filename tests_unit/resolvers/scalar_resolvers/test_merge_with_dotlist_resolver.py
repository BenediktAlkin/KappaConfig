import unittest

from kappaconfig.functional.load import from_string
from kappaconfig.resolvers.resolver import Resolver
from kappaconfig.resolvers.scalar_resolvers.from_dotlist_resolver import FromDotlistResolver
from kappaconfig.resolvers.scalar_resolvers.merge_with_dotlist_resolver import MergeWithDotlistResolver


class TestMergeWithDotlistResolver(unittest.TestCase):
    @staticmethod
    def _resolve(source):
        resolver = Resolver(
            scalar_resolvers=dict(
                from_dotlist=FromDotlistResolver(),
                merge_with_dotlist=MergeWithDotlistResolver(),
            ),
        )
        return resolver.resolve(from_string(source))

    def _resolve_and_assert(self, source, expected):
        actual = self._resolve(source)
        self.assertEqual(expected, actual)

    def test_simple(self):
        source = """
        somekey: ${merge_with_dotlist:value=5:${from_dotlist:value=3 other=4}}
        """
        expected = dict(
            somekey=dict(
                value=5,
                other=4,
            ),
        )
        self._resolve_and_assert(source, expected)

    def test_multiple(self):
        source = """
        somekey: ${merge_with_dotlist:value=5 asdf=True obj.key=value:${from_dotlist:value=3 other=4}}
        """
        expected = dict(
            somekey=dict(
                asdf=True,
                value=5,
                other=4,
                obj=dict(key="value"),
            ),
        )
        self._resolve_and_assert(source, expected)
