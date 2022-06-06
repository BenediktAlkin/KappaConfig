from ..entities.wrappers import KCDict, KCList, KCScalar, KCObject
from ..functional.parse_grammar import parse_grammar
from ..entities.grammar_tree_nodes import RootNode, FixedNode, InterpolatedNode
from ..functional.util import string_to_accessors, select

class Resolver:
    def __init__(self, *collection_resolvers, default_scalar_resolver=None, **scalar_resolvers):
        self.collection_resolvers = list(collection_resolvers)
        self.scalar_resolvers = scalar_resolvers
        if default_scalar_resolver is not None:
            self.scalar_resolvers[None] = default_scalar_resolver


    def resolve(self, node, root_node=None):
        result = {}
        if root_node is None:
            root_node = node
        wrapped_node = KCDict(root=node)
        self._resolve_collection(node, root_node=root_node, result=result, trace=[(wrapped_node, "root")])
        return result["root"]


    def _resolve_collection(self, node, root_node, result, trace):
        if isinstance(node, KCDict):
            parent, parent_accessor = trace[-1]
            result[parent_accessor] = {}
            # preorder
            for resolver in self.collection_resolvers:
                resolver.preorder_resolve(node, root_node=root_node, result=result, trace=trace, root_resolver=self)
                # preorder is allowed to change the current node
                node = parent[parent_accessor]

            # traverse
            for accessor, subnode in node.dict.items():
                trace.append((node, accessor))
                self._resolve_collection(subnode, root_node=root_node, result=result[parent_accessor], trace=trace)
                trace.pop()

            # postorder
            for resolver in self.collection_resolvers:
                resolver.postorder_resolve(node, root_node=root_node, result=result, trace=trace, root_resolver=self)
        elif isinstance(node, KCList):
            parent, parent_accessor = trace[-1]
            result[parent_accessor] = []
            # preorder
            for resolver in self.collection_resolvers:
                resolver.preorder_resolve(node, root_node=root_node, result=result, trace=trace, root_resolver=self)
                # preorder is allowed to change the current node
                node = parent[parent_accessor]

            # traverse
            for i, subnode in enumerate(node.list):
                trace.append((subnode, i))
                self._resolve_collection(subnode, root_node=root_node, result=result[parent_accessor], trace=trace)
                trace.pop()

            # postorder
            for resolver in self.collection_resolvers:
                resolver.postorder_resolve(node, root_node=root_node, result=result, trace=trace, root_resolver=self)
        elif isinstance(node, KCScalar):
            if not (isinstance(result, list) or isinstance(result, dict)):
                raise TypeError
            if not isinstance(node.value, str):
                resolve_result = node.value
            else:
                resolve_result = self.resolve_scalar(node.value, root_node=root_node)

            # resolved value might be a KCObject (e.g. when loading a nested yaml)
            if isinstance(resolve_result, KCObject):
                parent, accessor = trace.pop()
                trace.append((resolve_result, accessor))
                self._resolve_collection(resolve_result, root_node=root_node, result=result, trace=trace)
            else:
                # set value
                parent_accessor = trace[-1][1]
                if isinstance(parent_accessor, int):
                    if len(result) != parent_accessor:
                        raise IndexError
                    result.append(resolve_result)
                else:
                    result[parent_accessor] = resolve_result
        else:
            raise TypeError

    def resolve_scalar(self, value, root_node):
        grammar_tree = parse_grammar(value)
        return self._resolve_scalar(grammar_tree, root_node=root_node)

    def _resolve_scalar(self, grammar_node, root_node):
        if isinstance(grammar_node, RootNode):
            resolve_results = [self._resolve_scalar(child, root_node=root_node) for child in grammar_node.children]
            return self._merge_scalar_resolve_results(resolve_results)
        elif isinstance(grammar_node, FixedNode):
            return grammar_node.value
        elif isinstance(grammar_node, InterpolatedNode):
            # resolve children
            resolve_results = [self._resolve_scalar(child, root_node=root_node) for child in grammar_node.children]
            resolve_result = self._merge_scalar_resolve_results(resolve_results)
            # resolve cur node
            scalar_resolver = self.scalar_resolvers[grammar_node.resolver_key]
            return scalar_resolver.resolve(resolve_result, root_node=root_node)
        else:
            raise TypeError

    @staticmethod
    def _merge_scalar_resolve_results(resolve_results):
        if len(resolve_results) == 1:
            # keep datatype of single result
            return resolve_results[0]
        else:
            # concat as string
            return "".join(map(str, resolve_results))