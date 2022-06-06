import unittest
from kappaconfig.grammar.tree_parser import TreeParser
from kappaconfig.entities.grammar_tree_nodes import InterpolatedNode, FixedNode

class TestTreeParser(unittest.TestCase):
    def test_single_interpolation(self):
        tree = TreeParser.parse("${obj.key}")
        self.assertEqual(1, len(tree.children))
        interp_node = tree.children[0]
        self.assertTrue(isinstance(interp_node, InterpolatedNode))
        self.assertIsNone(interp_node.resolver_key)
        self.assertEqual(1, len(interp_node.children))
        fixed_node = interp_node.children[0]
        self.assertTrue(isinstance(fixed_node, FixedNode))
        self.assertEqual("obj.key", fixed_node.value)

    def test_single_resolver(self):
        tree = TreeParser.parse("${eval:obj.key}")
        self.assertEqual(1, len(tree.children))
        interp_node = tree.children[0]
        self.assertTrue(isinstance(interp_node, InterpolatedNode))
        self.assertEqual(1, len(interp_node.children))
        self.assertEqual("eval", interp_node.resolver_key)
        fixed_node = interp_node.children[0]
        self.assertTrue(isinstance(fixed_node, FixedNode))
        self.assertEqual("obj.key", fixed_node.value)

    def test_nested(self):
        tree = TreeParser.parse("${eval:${obj.key}/5}")

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
        tree = TreeParser.parse("start${obj.key}${eval:vars.variable}end")

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