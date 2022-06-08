import unittest
from kappaconfig.functional.parse_grammar import parse_grammar
from kappaconfig.entities.grammar_tree_nodes import InterpolatedNode, FixedNode
import kappaconfig.errors as errors

class TestParseGrammar(unittest.TestCase):
    def test_single_interpolation(self):
        tree = parse_grammar("${obj.key}")
        self.assertEqual(1, len(tree.children))
        interp_node = tree.children[0]
        self.assertTrue(isinstance(interp_node, InterpolatedNode))
        self.assertIsNone(interp_node.resolver_key)
        self.assertEqual(1, len(interp_node.children))
        fixed_node = interp_node.children[0]
        self.assertTrue(isinstance(fixed_node, FixedNode))
        self.assertEqual("obj.key", fixed_node.value)

    def test_single_resolver(self):
        tree = parse_grammar("${eval:obj.key}")
        self.assertEqual(1, len(tree.children))
        interp_node = tree.children[0]
        self.assertTrue(isinstance(interp_node, InterpolatedNode))
        self.assertEqual(1, len(interp_node.children))
        self.assertEqual("eval", interp_node.resolver_key)
        fixed_node = interp_node.children[0]
        self.assertTrue(isinstance(fixed_node, FixedNode))
        self.assertEqual("obj.key", fixed_node.value)

    def test_nested(self):
        tree = parse_grammar("${eval:${obj.key}/5}")

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
        tree = parse_grammar("start${obj.key}${eval:vars.variable}end")

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

    def test_empty_resolver_value(self):
        expected = errors.empty_resolver_value_error("yaml:")
        with self.assertRaises(type(expected)) as ex:
            parse_grammar("${yaml:}")
        self.assertEqual(expected.args[0], str(ex.exception))

        expected = errors.empty_resolver_value_error("")
        with self.assertRaises(type(expected)) as ex:
            parse_grammar("${}")
        self.assertEqual(expected.args[0], str(ex.exception))

    def test_parse_resolver_key_and_args_missing_closing_par(self):
        expected = errors.missing_closing_parentheses_at_last_position("select()a")
        with self.assertRaises(type(expected)) as ex:
            parse_grammar("${select()a:asdf}")
        self.assertEqual(expected.args[0], str(ex.exception))

        expected = errors.missing_closing_parentheses_at_last_position("select(")
        with self.assertRaises(type(expected)) as ex:
            parse_grammar("${select(:asdf}")
        self.assertEqual(expected.args[0], str(ex.exception))

    def test_parse_resolver_key_and_args(self):
        tree = parse_grammar("${select(some_key):asdf}")
        self.assertEqual(1, len(tree.children))
        node = tree.children[0]
        self.assertTrue(isinstance(node, InterpolatedNode))
        self.assertEqual("select", node.resolver_key)
        self.assertEqual(1, len(node.args))
        self.assertEqual("some_key", node.args[0])

    def test_parse_resolver_key_and_args_multiple(self):
        tree = parse_grammar("${select(some_key, other, 5):asdf}")
        self.assertEqual(1, len(tree.children))
        node = tree.children[0]
        self.assertTrue(isinstance(node, InterpolatedNode))
        self.assertEqual("select", node.resolver_key)
        self.assertEqual(3, len(node.args))
        self.assertEqual("some_key", node.args[0])
        self.assertEqual("other", node.args[1])
        self.assertEqual(5, node.args[2])