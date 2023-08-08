import unittest

from kappaconfig.functional.load import from_string
from kappaconfig.resolvers.resolver import Resolver
from kappaconfig.resolvers.scalar_resolvers.env_resolver import EnvResolver
import os


class TestEnvResolver(unittest.TestCase):
    def _resolve_and_assert(self, input_, key, expected):
        os.environ[key] = expected
        resolver = Resolver(
            scalar_resolvers=dict(
                env=EnvResolver()
            ),
        )
        actual = resolver.resolve(from_string(input_))
        self.assertEqual(expected, actual["somekey"])

    def test_simple(self):
        src = """
        somekey: ${env:test_simple_key}
        """
        expected = "test_simple_value"
        self._resolve_and_assert(src, "test_simple_key", expected)
