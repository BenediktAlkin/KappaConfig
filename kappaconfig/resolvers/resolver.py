from ..entities.wrappers import KCDict, KCList, KCScalar, KCObject
from ..functional.parse_grammar import parse_grammar
from ..entities.grammar_tree_nodes import RootNode, FixedNode, InterpolatedNode
from copy import deepcopy

class Resolver:
    def __init__(
            self, collection_resolvers=None,
            scalar_resolvers=None, default_scalar_resolver=None,
            post_processors=None):
        self.collection_resolvers = collection_resolvers or []
        self.scalar_resolvers = scalar_resolvers or {}
        if default_scalar_resolver is not None:
            self.scalar_resolvers[None] = default_scalar_resolver
        self.post_processors = post_processors or []


    def resolve(self, node, root_node=None):
        node = deepcopy(node)
        result = {}
        root_node_to_pass = node if root_node is None else root_node
        wrapped_node = KCDict(root=node)
        self._resolve_collection(node, root_node=root_node_to_pass, result=result, trace=[(wrapped_node, "root")])
        processed_result = result["root"]
        # only postprocess from root call (e.g. template resolver also calls resolve but with a root_node parameter)
        if root_node is None:
            post_processed = self.post_process(processed_result)
        else:
            post_processed = processed_result
        return post_processed


    def _resolve_collection(self, node, root_node, result, trace):
        parent, parent_accessor = trace[-1]
        if isinstance(node, KCDict):
            if isinstance(parent_accessor, int):
                result.append({})
            else:
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
            if isinstance(parent_accessor, int):
                result[parent_accessor].append([])
            else:
                result[parent_accessor] = []
            # preorder
            for resolver in self.collection_resolvers:
                resolver.preorder_resolve(node, root_node=root_node, result=result, trace=trace, root_resolver=self)
                # preorder is allowed to change the current node
                node = parent[parent_accessor]

            # traverse
            for i, subnode in enumerate(node.list):
                trace.append((node, i))
                self._resolve_collection(subnode, root_node=root_node, result=result[parent_accessor], trace=trace)
                trace.pop()

            # postorder
            for resolver in self.collection_resolvers:
                resolver.postorder_resolve(node, root_node=root_node, result=result, trace=trace, root_resolver=self)
        elif isinstance(node, KCScalar):
            # preorder
            for resolver in self.collection_resolvers:
                resolver.preorder_resolve(node, root_node=root_node, result=result, trace=trace, root_resolver=self)
                # preorder is allowed to change the current node
                node = parent[parent_accessor]

            if not isinstance(node.value, str):
                resolve_result = node.value
            else:
                resolve_result = self.resolve_scalar(node.value, root_node=root_node)

            # resolved value might be a KCObject (e.g. when loading a nested yaml)
            if isinstance(resolve_result, KCObject):
                parent[parent_accessor] = resolve_result
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

            # postorder
            for resolver in self.collection_resolvers:
                resolver.postorder_resolve(node, root_node=root_node, result=result, trace=trace, root_resolver=self)
        else:
            from ..errors import unexpected_type_error
            raise unexpected_type_error([KCDict, KCList, KCScalar], node)

    def resolve_scalar(self, value, root_node):
        grammar_tree = parse_grammar(value)
        resolved_scalar = self._resolve_scalar(grammar_tree, root_node=root_node)
        return resolved_scalar

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
            if grammar_node.resolver_key not in self.scalar_resolvers:
                from ..errors import invalid_resolver_key
                raise invalid_resolver_key(grammar_node.resolver_key, list(self.scalar_resolvers.keys()))
            scalar_resolver = self.scalar_resolvers[grammar_node.resolver_key]
            resolved_scalar = scalar_resolver.resolve(resolve_result, root_node=root_node)
            return resolved_scalar
        else:
            from ..errors import unexpected_type_error
            raise unexpected_type_error([RootNode, FixedNode, InterpolatedNode], grammar_node)

    @staticmethod
    def _merge_scalar_resolve_results(resolve_results):
        if len(resolve_results) == 1:
            # keep datatype of single result
            return resolve_results[0]
        else:
            # concat as string
            return "".join(map(str, resolve_results))

    def post_process(self, node):
        wrapped = dict(root=node)
        self._post_process(wrapped, trace=[])
        if "root" not in wrapped:
            from ..errors import empty_result
            raise empty_result()
        return wrapped["root"]

    def _post_process(self, node, trace):
        for post_processor in self.post_processors:
            post_processor.preorder_process(node, trace=trace)
        if isinstance(node, dict):
            for key in node.keys():
                trace.append((node, key))
                self._post_process(node[key], trace=trace)
                trace.pop()
        elif isinstance(node, list):
            for i, item in enumerate(node):
                trace.append((node, i))
                self._post_process(item, trace=trace)