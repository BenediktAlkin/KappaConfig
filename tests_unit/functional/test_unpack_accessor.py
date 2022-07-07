import unittest
from kappaconfig.functional.load import from_string
from kappaconfig.functional.unpack_accessors import unpack_accessors
from kappaconfig.functional.convert import to_primitive
import kappaconfig.errors as errors

class TestUnpackAccessor(unittest.TestCase):
    def _unpack_and_assert_equal(self, source, expected):
        expected = to_primitive(from_string(expected))
        actual = to_primitive(unpack_accessors(from_string(source)))
        self.assertEqual(expected, actual)

    def _unpack_and_assert_fails(self, source, expected):
        with self.assertRaises(type(expected)) as ex:
            unpack_accessors(from_string(source))
        self.assertEqual(expected.args[0], str(ex.exception))

    def test_root(self):
        source = "some.obj.value: 5"
        expected = """
        some:
          obj:
            value: 5
        """
        self._unpack_and_assert_equal(source, expected)

    def test_nested(self):
        source = """
        some:
          obj.value: 5
          other:
            nested.arr[0].value: 3
        """
        expected = """
        some:
          obj:
            value: 5
          other:
            nested:
              arr:
                - value: 3
        """
        self._unpack_and_assert_equal(source, expected)


    def test_non_sequential_list(self):
        source = """
        a.[5]: 5
        """
        expected = errors.dotlist_requires_sequential_insert_error()
        self._unpack_and_assert_fails(source, expected)

    def test_invalid_unpack(self):
        source = """
        obj: 5
        obj.val: 3
        """
        expected = errors.invalid_unpack_operation("obj.val", "obj")
        self._unpack_and_assert_fails(source, expected)
