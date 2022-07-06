import unittest
import kappaconfig.functional.dotlist as dotlist
from kappaconfig.entities.wrappers import KCDict, KCList, KCScalar
import kappaconfig.errors as errors

class TestDotlist(unittest.TestCase):
    def test_to_dotlist(self):
        source = dict(
            some_string="some_value",
            some_list=["a", "b", "c", 5],
            some_dict=dict(
                some_nested_dict=dict(
                    some_nested_dict_value=5
                )
            ),
        )
        expected = [
            "some_string=some_value",
            "some_list[0]=a",
            "some_list[1]=b",
            "some_list[2]=c",
            "some_list[3]=5",
            "some_dict.some_nested_dict.some_nested_dict_value=5",
        ]
        actual = dotlist.to_dotlist(source)
        self.assertEqual(expected, actual)

    def test_from_dotlist(self):
        source = [
            "some_string=some_value",
            "some_list[0]=a",
            "some_list[1]=b",
            "some_list[2]=c",
            "some_list[3]=5",
            "some_dict.some_nested_dict.some_nested_dict_value=5",
        ]
        expected = KCDict(
            some_string=KCScalar("some_value"),
            some_list=KCList(KCScalar("a"), KCScalar("b"), KCScalar("c"), KCScalar(5)),
            some_dict=KCDict(
                some_nested_dict=KCDict(
                    some_nested_dict_value=KCScalar(5)
                )
            ),
        )

        actual = dotlist.from_dotlist(source)
        self.assertEqual(expected, actual)

    def test_from_dotlist_ignore_invalid(self):
        source = [
            "some_string=some_value",
            "--invalid"
        ]
        expected = KCDict(some_string=KCScalar("some_value"))
        actual = dotlist.from_dotlist(source, ignore_invalid_entries=True)
        self.assertEqual(expected, actual)

    def test_from_dotlist_invalid_noequal(self):
        source = [
            "some_string=some_value",
            "--invalid"
        ]
        expected = errors.dotlist_entry_requires_equal_sign_error("--invalid")
        with self.assertRaises(type(expected)) as ex:
            dotlist.from_dotlist(source)
        self.assertEqual(expected.args[0], str(ex.exception))

    def test_from_dotlist_invalid_twoequal(self):
        source = [
            "some_string=some_value=3",
        ]
        expected = errors.dotlist_entry_multiple_equal_signs_error("some_string=some_value=3")
        with self.assertRaises(type(expected)) as ex:
            dotlist.from_dotlist(source)
        self.assertEqual(expected.args[0], str(ex.exception))

    def test_from_dotlist_invalid_accessor_character(self):
        source = [
            "some_string#=some_value",
        ]
        expected = errors.dict_accessor_has_to_be_identifier_error("some_string#", "some_string#")
        with self.assertRaises(type(expected)) as ex:
            dotlist.from_dotlist(source)
        self.assertEqual(expected.args[0], str(ex.exception))

    def test_from_dotlist_invalid_accessor_space(self):
        source = [
            "some string=some_value",
        ]
        expected = errors.dict_accessor_has_to_be_identifier_error("some string", "some string")
        with self.assertRaises(type(expected)) as ex:
            dotlist.from_dotlist(source)
        self.assertEqual(expected.args[0], str(ex.exception))