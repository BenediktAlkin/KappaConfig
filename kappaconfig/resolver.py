from .entities.kc_dict import KCDict
from .entities.kc_list import KCList
from .entities.kc_scalar import KCScalar
from .grammar.tree_parser import TreeParser
from .grammar.tree_nodes import RootNode, FixedNode, InterpolatedNode
from .functional.util import string_to_accessors, select

class Resolver:
    def __init__(self):
        self.resolvers = {}


    def resolve(self, node, root_node=None):
        if root_node is None:
            root_node = node

        if isinstance(node, KCDict):
            return {key: self.resolve(value, root_node=root_node) for key, value in self.dict.items()}
        elif isinstance(node, KCList):
            return [self.resolve(item, root_node=root_node) for item in self.list]
        else:
            # node is a KCScalar
            if not isinstance(node.value, str):
                return self.value

            # resolve interpolations/grammar
            tree = TreeParser.parse(self.value)
            self.resolve_grammar(tree, data_root_node=root_node)

            return self.value

    def resolve_grammar(self, grammar_node, data_root_node):
        if isinstance(grammar_node, RootNode):
            return self.resolve_grammar_children(grammar_node, data_root_node=data_root_node)
        elif isinstance(grammar_node, FixedNode):
            return grammar_node.value
        elif isinstance(grammar_node, InterpolatedNode):
            resolved = self.resolve_grammar_children(grammar_node, data_root_node=data_root_node)
            if grammar_node.resolver_key is None:
                # interpolation
                accessors = string_to_accessors(resolved)
                return select(root_node=root_node, accessors=accessors)
            else:
                # custom resolver
                resolver = self.resolvers[grammar_node.resolver_key]
                return resolver
                # TODO
                raise NotImplementedError

    def resolve_grammar_children(self, grammar_node, data_root_node):
        if len(grammar_node.children) == 1:
            # keep datatype of single child
            return GrammarResolver.resolve(grammar_node.children[0], data_root_node)
        else:
            # concat as string
            return "".join(map(lambda child: self.resolve_grammar(child, data_root_node), grammar_node.children))