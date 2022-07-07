import unittest
from kappaconfig.functional.merge import merge
import kappaconfig.errors as errors
from kappaconfig.entities.wrappers import KCScalar

class TestUtil(unittest.TestCase):
    def test_dict(self):
        base = dict(
            some_key=5,
            other_key=6
        )
        to_merge = dict(other_key=10)
        expected = dict(
            some_key=5,
            other_key=10,
        )
        actual = merge(base, to_merge)
        self.assertEqual(expected, actual)

    def test_none(self):
        base = None
        to_merge = 5
        expected = 5
        actual = merge(base, to_merge)
        self.assertEqual(expected, actual)

    def test_kcscalar_none(self):
        base = KCScalar(None)
        to_merge = 5
        expected = 5
        actual = merge(base, to_merge)
        self.assertEqual(expected, actual)

    def test_nested_dict(self):
        base = dict(obj=dict(prop=5), other=3)
        to_merge = dict(obj=dict(prop=10), very_other=7)
        expected = dict(obj=dict(prop=10), other=3, very_other=7)
        actual = merge(base, to_merge)
        self.assertEqual(expected, actual)

    def test_scalar_root(self):
        base = 5
        to_merge = 10
        expected = 10
        actual = merge(base, to_merge)
        self.assertEqual(expected, actual)

    def test_returns_copy(self):
        base = dict(
            some_key=5,
            other_key=6
        )
        to_merge = dict(other_key=10)
        expected = dict(
            some_key=5,
            other_key=6,
        )
        _ = merge(base, to_merge)
        self.assertEqual(expected, base)

    def test_root_lists(self):
        base = [5, 6]
        to_merge = [7, 8]
        expected = [7, 8]
        actual = merge(base, to_merge)
        self.assertEqual(expected, actual)

    def test_nested_list(self):
        base = dict(some_list=[1, 2, dict(some=5)])
        to_merge = dict(some_list=[5, 6, dict(other=10)])
        expected = dict(some_list=[5, 6, dict(some=5, other=10)])
        actual = merge(base, to_merge)
        self.assertEqual(expected, actual)

    def test_nested_dict_combine(self):
        base = dict(some=dict(other=3, some=dict(prop=12)))
        to_merge = dict(other_root="asdf", some=dict(some=5))
        expected = dict(some=dict(other=3, some=5), other_root="asdf")
        actual = merge(base, to_merge)
        self.assertEqual(expected, actual)

    def test_merge_larger_list(self):
        base = dict(some_list=[1])
        to_merge = dict(some_list=[5, 6, "asdf"])
        expected = dict(some_list=[5, 6, "asdf"])
        actual = merge(base, to_merge)
        self.assertEqual(expected, actual)

    def test_incompatible_dict(self):
        base = dict(a=5)
        to_merge = [6]
        expected = errors.incompatible_type(dict, list)
        with self.assertRaises(type(expected)) as ex:
            _ = merge(base, to_merge)
        self.assertEqual(expected.args[0], str(ex.exception))

    def test_incompatible_list(self):
        base = [6]
        to_merge = dict(a=5)
        expected = errors.incompatible_type(list, dict)
        with self.assertRaises(type(expected)) as ex:
            _ = merge(base, to_merge)
        self.assertEqual(expected.args[0], str(ex.exception))

    def test_list_merge_missing_strategy(self):
        base = dict(a=[1])
        to_merge = dict(a=[5])
        expected = dict(a=[5])
        actual = merge(base, to_merge)
        self.assertEqual(expected, actual)

    def test_list_merge_missing_strategy2(self):
        base = dict(a=[1])
        to_merge = dict(a=[7, 6])
        expected = dict(a=[7, 6])
        actual = merge(base, to_merge)
        self.assertEqual(expected, actual)

    def test_list_merge_invalid_strategy(self):
        base = dict(a=[1])
        to_merge = {"a.strat": [5]}
        expected = errors.list_merge_invalid_resolving_strategy("a.strat")
        with self.assertRaises(type(expected)) as ex:
            merge(base, to_merge)
        self.assertEqual(expected.args[0], str(ex.exception))
