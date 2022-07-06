import unittest
from kappaconfig.grammar.dotlist_grammar import parse_dotlist_entry
import kappaconfig.errors as errors


class TestDotlistGrammar(unittest.TestCase):
    def _test_error(self, source, expected):
        with self.assertRaises(type(expected)) as ex:
            parse_dotlist_entry(source)
        self.assertEqual(expected.args[0], str(ex.exception))


    def test_from_dotlist_invalid_noequal(self):
        source = "--invalid"
        self._test_error(source, errors.dotlist_entry_requires_equal_sign_error(source))

    def test_from_dotlist_twoequal(self):
        source = "some_string=some_value=3"
        actual_accessor, actual_value = parse_dotlist_entry(source)
        expected_accessor = ["some_string"]
        expected_value = "some_value=3"
        self.assertEqual(actual_accessor, expected_accessor)
        self.assertEqual(actual_value, expected_value)
