import unittest

from kappaconfig.entities.kc_dict import KCDict
from kappaconfig.entities.kc_list import KCList
from kappaconfig.entities.kc_scalar import KCScalar

class TestResolve(unittest.TestCase):
    def test_to_primitive_scalar_root(self):
        self.assertEqual(5, KCScalar(5).resolve())

    def test_to_primitive_list_root(self):
        actual = KCList(KCScalar(5), KCScalar(6)).resolve()
        self.assertTrue(isinstance(actual, list))
        self.assertEqual([5, 6], actual)

    def test_to_primitive_dict_root(self):
        actual = KCDict(some=KCScalar("value")).resolve()
        self.assertTrue(isinstance(actual, dict))
        self.assertEqual("value", actual["some"])
