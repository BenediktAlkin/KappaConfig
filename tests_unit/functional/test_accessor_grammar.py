import unittest
from kappaconfig.functional.accessor_grammar import parse_accessor
import kappaconfig.errors as errors

class TestAccessorGrammar(unittest.TestCase):
    def test_valid(self):
        self.assertEqual(["some", "accessor"], parse_accessor("some.accessor"))
        self.assertEqual(["some", 5], parse_accessor("some[5]"))
        self.assertEqual([5, "some"], parse_accessor("[5].some"))
        self.assertEqual(["some_prop", 5, "that5"], parse_accessor("some_prop[5].that5"))
        self.assertEqual(["some_prop", 5, 6, 7], parse_accessor("some_prop[5][6][7]"))

    def _test_error(self, source, expected):
        with self.assertRaises(type(expected)) as ex:
            parse_accessor(source)
        self.assertEqual(expected.args[0], str(ex.exception))

    def test_empty_accessor(self):
        source = ".asdf"
        self._test_error(source, errors.empty_accessor_error(source))

    def test_dict_accessor_starts_with_number(self):
        source = "asdf.5"
        self._test_error(source, errors.dict_accessor_has_to_start_with_letter_error(source, "5"))

    def test_dict_accessor_starts_with_underscore(self):
        source = "asdf._a"
        self._test_error(source, errors.dict_accessor_has_to_start_with_letter_error(source, "_a"))

    def test_dict_accessor_invalid_identifier(self):
        source = "asdf.a%"
        self._test_error(source, errors.dict_accessor_has_to_be_identifier_error(source, "a%"))

    def test_missing_closing_bracket(self):
        source = "some[5"
        self._test_error(source, errors.missing_closing_bracket_error(source, "[5"))

    def test_non_int_list_accessor(self):
        source = "some[a]"
        self._test_error(source, errors.list_accessor_has_to_be_int_error(source, "[a]"))

    def test_empty_list_accessor(self):
        source = "some[]"
        self._test_error(source, errors.list_accessor_has_to_be_int_error(source, "[]"))