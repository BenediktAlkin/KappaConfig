import unittest

import kappaconfig.errors as errors
from kappaconfig.entities.grammar_tree_nodes import InterpolatedNode, FixedNode
from kappaconfig.grammar.scalar_grammar import parse_scalar, parse_resolver_args_and_value


class TestScalarGrammar(unittest.TestCase):
    def test_single_interpolation(self):
        tree = parse_scalar("${obj.key}")
        self.assertEqual(1, len(tree.children))
        interp_node = tree.children[0]
        self.assertTrue(isinstance(interp_node, InterpolatedNode))
        self.assertIsNone(interp_node.resolver_key)
        self.assertEqual(1, len(interp_node.children))
        fixed_node = interp_node.children[0]
        self.assertTrue(isinstance(fixed_node, FixedNode))
        self.assertEqual("obj.key", fixed_node.value)

    def test_single_resolver(self):
        tree = parse_scalar("${eval:obj.key}")
        self.assertEqual(1, len(tree.children))
        interp_node = tree.children[0]
        self.assertTrue(isinstance(interp_node, InterpolatedNode))
        self.assertEqual(1, len(interp_node.children))
        self.assertEqual("eval", interp_node.resolver_key)
        fixed_node = interp_node.children[0]
        self.assertTrue(isinstance(fixed_node, FixedNode))
        self.assertEqual("obj.key", fixed_node.value)

    def test_nested(self):
        tree = parse_scalar("${eval:${obj.key}/5}")

        # check ${eval:}
        self.assertEqual(1, len(tree.children))
        interp_node = tree.children[0]
        self.assertTrue(isinstance(interp_node, InterpolatedNode))
        self.assertEqual("eval", interp_node.resolver_key)
        self.assertEqual(2, len(interp_node.children))

        # check ${obj.key} node
        nested_interp_node = interp_node.children[0]
        self.assertTrue(isinstance(nested_interp_node, InterpolatedNode))
        self.assertEqual(1, len(nested_interp_node.children))
        fixed_node = nested_interp_node.children[0]
        self.assertTrue(isinstance(fixed_node, FixedNode))
        self.assertEqual("obj.key", fixed_node.value)

        # check /5 node
        fixed_node = interp_node.children[1]
        self.assertTrue(isinstance(fixed_node, FixedNode))
        self.assertEqual("/5", fixed_node.value)

    def test_mixed_root(self):
        tree = parse_scalar("start${obj.key}${eval:vars.variable}end")

        self.assertEqual(4, len(tree.children))
        self.assertTrue(isinstance(tree.children[0], FixedNode))
        self.assertEqual("start", tree.children[0].value)

        self.assertTrue(isinstance(tree.children[1], InterpolatedNode))
        self.assertEqual(1, len(tree.children[1].children))
        self.assertTrue(isinstance(tree.children[1].children[0], FixedNode))
        self.assertEqual("obj.key", tree.children[1].children[0].value)

        self.assertTrue(isinstance(tree.children[2], InterpolatedNode))
        self.assertEqual("eval", tree.children[2].resolver_key)
        self.assertEqual(1, len(tree.children[2].children))
        self.assertTrue(isinstance(tree.children[2].children[0], FixedNode))
        self.assertEqual("vars.variable", tree.children[2].children[0].value)

        self.assertTrue(isinstance(tree.children[3], FixedNode))
        self.assertEqual("end", tree.children[3].value)

    def test_empty_resolver_key(self):
        expected = errors.empty_resolver_key_error(":something")
        with self.assertRaises(type(expected)) as ex:
            parse_scalar("${:something}")
        self.assertEqual(expected.args[0], str(ex.exception))

    def test_empty_resolver_value(self):
        expected = errors.empty_resolver_value_error("yaml:")
        with self.assertRaises(type(expected)) as ex:
            parse_scalar("${yaml:}")
        self.assertEqual(expected.args[0], str(ex.exception))

        expected = errors.empty_resolver_value_error("")
        with self.assertRaises(type(expected)) as ex:
            parse_scalar("${}")
        self.assertEqual(expected.args[0], str(ex.exception))

    def test_parse_resolver_args_and_value_missing_scalar_resolver_value(self):
        expected = errors.missing_scalar_resolver_value("")
        with self.assertRaises(type(expected)) as ex:
            parse_resolver_args_and_value("")
        self.assertEqual(expected.args[0], str(ex.exception))

    def test_parse_resolver_args_and_value_missing_parameter(self):
        expected = errors.missing_parameter_error("only_value", n_args=1)
        with self.assertRaises(type(expected)) as ex:
            parse_resolver_args_and_value("only_value", n_args=1)
        self.assertEqual(expected.args[0], str(ex.exception))

        expected = errors.missing_parameter_error("param:value", n_args=2)
        with self.assertRaises(type(expected)) as ex:
            parse_resolver_args_and_value("param:value", n_args=2)
        self.assertEqual(expected.args[0], str(ex.exception))

    def test_parse_resolver_args_and_value(self):
        args, value = parse_resolver_args_and_value("param:value", n_args=1)
        self.assertEqual("value", value.value)
        self.assertEqual(1, len(args))
        self.assertEqual("param", args[0])

        args, value = parse_resolver_args_and_value("param1 : 5:value", n_args=2)
        self.assertEqual("value", value.value)
        self.assertEqual(2, len(args))
        self.assertEqual("param1", args[0])
        self.assertEqual(5, args[1])

        args, value = parse_resolver_args_and_value("param1:5:value")
        self.assertEqual("value", value.value)
        self.assertEqual(2, len(args))
        self.assertEqual("param1", args[0])
        self.assertEqual(5, args[1])
