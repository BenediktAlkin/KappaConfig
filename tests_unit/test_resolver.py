import unittest

from kappaconfig.entities.wrappers import KCDict, KCList, KCScalar
from kappaconfig.resolvers.resolver import Resolver

class TestResolver(unittest.TestCase):
    def test_resolve_scalar_root(self):
        self.assertEqual(5, Resolver().resolve(KCScalar(5)))

    def test_resolve_list_root(self):
        actual = Resolver().resolve(KCList(KCScalar(5), KCScalar(6)))
        self.assertTrue(isinstance(actual, list))
        self.assertEqual([5, 6], actual)

    def test_resolve_dict_root(self):
        actual = Resolver().resolve(KCDict(some=KCScalar("value")))
        self.assertTrue(isinstance(actual, dict))
        self.assertEqual("value", actual["some"])
