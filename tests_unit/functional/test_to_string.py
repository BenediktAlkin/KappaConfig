import unittest

from kappaconfig.functional.to_string import accessors_to_string, trace_to_full_accessor


class TestToString(unittest.TestCase):
    def test_accessors_to_string(self):
        accessors = ["some", "asd", 1, 3, "q", 3]
        expected = "some.asd[1][3].q[3]"
        actual = accessors_to_string(accessors)
        self.assertEqual(expected, actual)

    def test_trace_to_full_accessor_empty(self):
        self.assertEqual("", trace_to_full_accessor([]))

    def test_trace_to_full_accessor(self):
        trace_accessors = ["root", 5, "asdf", 3]
        trace = list(map(lambda ta: (None, ta), trace_accessors))
        self.assertEqual("[5].asdf[3]", trace_to_full_accessor(trace))
