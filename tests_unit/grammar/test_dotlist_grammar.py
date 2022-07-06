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

    def test_from_dotlist_invalid_twoequal(self):
        source = "some_string=some_value=3"
        self._test_error(source, errors.dotlist_entry_multiple_equal_signs_error(source))
