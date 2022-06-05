import unittest
import kappaconfig.functional.dotlist as dotlist

class TestDotlist(unittest.TestCase):
    def test_to_dotlist(self):
        input_ = dict(
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
        actual = dotlist.to_dotlist(input_)
        self.assertEqual(expected, actual)

    def test_from_dotlist(self):
        input_ = [
            "some_string=some_value",
            "some_list[0]=a",
            "some_list[1]=b",
            "some_list[2]=c",
            "some_list[3]=5",
            "some_dict.some_nested_dict.some_nested_dict_value=5",
        ]
        expected = dict(
            some_string="some_value",
            some_list=["a", "b", "c", 5],
            some_dict=dict(
                some_nested_dict=dict(
                    some_nested_dict_value=5
                )
            ),
        )

        actual = dotlist.from_dotlist(input_)
        self.assertEqual(expected, actual)