import unittest
import kappaconfig.functional.util as util
import kappaconfig.errors as errors

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
        expected = errors.missing_closing_bracket_error("[1")
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

    def test_merge_returns_copy(self):
        self.fail()

    def test_trace_to_full_accessor_empty(self):
        self.assertEqual("", util.trace_to_full_accessor([]))

    def test_trace_to_full_accessor(self):
        trace_accessors = ["root", 5, "asdf", 3]
        trace = list(map(lambda ta: (None, ta), trace_accessors))
        self.assertEqual("[5].asdf[3]", util.trace_to_full_accessor(trace))

    def test_invalid_select(self):
        root_node = dict(
            some_node=5,
            some_nested_node=dict(
                some_list=[
                    dict(some_obj=23),
                    25,
                ],
            ),
        )
        expected = errors.invalid_accessor_error("invalid", "invalid")
        with self.assertRaises(type(expected)) as ex:
            util.select(root_node, ["invalid"])
        self.assertEqual(expected.args[0], str(ex.exception))

        expected = errors.invalid_accessor_error("some_node.invalid", "some_node.invalid[5]")
        with self.assertRaises(type(expected)) as ex:
            util.select(root_node, ["some_node", "invalid", 5])
        self.assertEqual(expected.args[0], str(ex.exception))

        expected = errors.invalid_accessor_error("some_nested_node.some_list[23]", "some_nested_node.some_list[23]")
        with self.assertRaises(type(expected)) as ex:
            util.select(root_node, ["some_nested_node", "some_list", 23])
        self.assertEqual(expected.args[0], str(ex.exception))