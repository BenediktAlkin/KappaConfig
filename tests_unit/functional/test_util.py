import unittest
import kappaconfig.functional.util as util
import kappaconfig.errors as msg

class TestUtil(unittest.TestCase):
    def test_accessors_to_string(self):
        accessors = ["some", "asd", 1, 3, "q", 3]
        expected = "some.asd[1][3].q[3]"
        actual = util.accessors_to_string(accessors)
        self.assertEqual(expected, actual)

    def test_string_to_accessors(self):
        accessor_string = "some.asd[1][3].q[3]"
        expected = ["some", "asd", 1, 3, "q", 3]
        actual = util.string_to_accessors(accessor_string)
        self.assertEqual(expected, actual)

    def test_string_to_accessors_missing_closing_bracket(self):
        accessor_string = "some.asd[1"
        expected = msg.missing_closing_bracket_error("[1")
        with self.assertRaises(type(expected)) as ex:
            util.string_to_accessors(accessor_string)
        self.assertEqual(expected.args[0], str(ex.exception))

    def test_merge_primitive(self):
        base = dict(
            some_key=5,
            other_key=6
        )
        to_merge = dict(other_key=10)
        expected = dict(
            some_key=5,
            other_key=10,
        )
        actual = util.merge(base, to_merge)
        self.assertEqual(expected, actual)