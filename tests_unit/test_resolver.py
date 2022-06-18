import unittest

from kappaconfig.entities.wrappers import KCDict, KCList, KCScalar
from kappaconfig.resolvers.resolver import Resolver
import kappaconfig.errors as errors
from kappaconfig.functional.load import from_string

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

    def test_resolve_invalid_resolver_key(self):
        expected = errors.invalid_resolver_key("asdf", [], "", None)
        with self.assertRaises(type(expected)) as ex:
            Resolver().resolve(from_string("${asdf:qwer}"))
        self.assertEqual(expected.args[0], str(ex.exception))

    def test_resolve_invalid_resolver_key_multiple_valid_keys(self):
        expected = errors.invalid_resolver_key("asdf", ["q", "b", None], "", None)
        with self.assertRaises(type(expected)) as ex:
            Resolver(
                scalar_resolvers=dict(q=None, b=None),
                default_scalar_resolver=dict()
            ).resolve(from_string("${asdf:qwer}"))
        self.assertEqual(expected.args[0], str(ex.exception))
