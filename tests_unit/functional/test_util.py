import unittest

import kappaconfig.errors as errors
from kappaconfig.functional.util import select
from tests_unit.util.trace import simulated_trace


class TestUtil(unittest.TestCase):
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
        expected = errors.invalid_accessor_error(["invalid"], simulated_trace())
        with self.assertRaises(type(expected)) as ex:
            select(root_node, ["invalid"])
        self.assertEqual(expected.args[0], str(ex.exception))

        expected = errors.invalid_accessor_error(["some_node", "invalid"], simulated_trace())
        with self.assertRaises(type(expected)) as ex:
            select(root_node, ["some_node", "invalid", 5])
        self.assertEqual(expected.args[0], str(ex.exception))

        expected = errors.invalid_accessor_error(["some_nested_node", "some_list", 23], simulated_trace())
        with self.assertRaises(type(expected)) as ex:
            select(root_node, ["some_nested_node", "some_list", 23])
        self.assertEqual(expected.args[0], str(ex.exception))
