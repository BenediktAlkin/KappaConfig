import unittest
import kappaconfig.functional.util as util

class TestUtil(unittest.TestCase):
    def test_string_to_accessors(self):
        accessor_string = "some.asd[1][3].q[3]"
        expected = ["some", "asd", 1, 3, "q", 3]
        actual = util.string_to_accessors(accessor_string)
        self.assertEqual(expected, actual)

    def test_string_to_accessors_no_closing_bracket(self):
        accessor_string = "some.asd[1"
        with self.assertRaises(ValueError) as ex:
            util.string_to_accessors(accessor_string)
            self.assertEqual("expected ']' at last position of accessor '[1'", str(ex.exception))