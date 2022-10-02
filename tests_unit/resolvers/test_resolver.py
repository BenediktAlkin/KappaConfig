import unittest

from kappaconfig.functional.load import from_string
from kappaconfig.resolvers.resolver import Resolver


class TestResolver(unittest.TestCase):
    def test_resolve_with_nonstring_keys(self):
        source = """
        5: intkey
        true: boolkey
        3.2: floatkey 
        """
        resolver = Resolver()
        actual = resolver.resolve(from_string(source))
        self.assertEqual({
            5: "intkey",
            True: "boolkey",
            3.2: "floatkey",
        }, actual)
