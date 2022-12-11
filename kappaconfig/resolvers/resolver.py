from copy import deepcopy

import yaml

from ..entities.grammar_tree_nodes import RootNode, FixedNode, InterpolatedNode
from ..entities.wrappers import KCDict, KCList, KCScalar, KCObject
from ..functional.convert import from_primitive, to_primitive
from ..grammar.scalar_grammar import parse_scalar


class Resolver:
    def __init__(
            self, collection_resolvers=None,
            scalar_resolvers=None, default_scalar_resolver=None,
            pre_processors=None, post_processors=None
    ):
        self.collection_resolvers = collection_resolvers or []
        self.scalar_resolvers = scalar_resolvers or {}
        if default_scalar_resolver is not None:
            self.scalar_resolvers[None] = default_scalar_resolver
        self.pre_processors = pre_processors or []
        self.post_processors = post_processors or []

    def resolve(self, node, root_node=None):
        node = deepcopy(node)
        if root_node is None:
            pre_processed = self.pre_process(node)
        else:
            pre_processed = node
        result = {}
        root_node_to_pass = pre_processed if root_node is None else root_node
        wrapped_node = KCDict(root=pre_processed)
        self._resolve_collection(
            pre_processed,
            root_node=root_node_to_pass,
            result=result,
            trace=[(wrapped_node, "root")],
        )
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
                if isinstance(result, list):
                    result.append({})
                else:
                    # dict with int index
                    result[parent_accessor] = {}
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
                result.append([])
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
                resolve_result = node.value
                # track resolved scalars to avoid endless loops in resolving (e.g. prop: ${prop})
                scalar_resolver_trace = []
                while True:
                    scalar_resolver_trace.append(resolve_result)
                    resolve_result = self.resolve_scalar(resolve_result, root_node=root_node, trace=trace)
                    if not isinstance(resolve_result, str) or not self._requires_resolve_scalar(resolve_result):
                        break
                    # check for recursive resolving
                    if resolve_result in scalar_resolver_trace:
                        from ..errors import recursive_resolving_error
                        raise recursive_resolving_error(trace)

            if isinstance(resolve_result, KCObject):
                # resolved value might be a KCObject (e.g. when loading a nested yaml with resolve_all=False)
                parent[parent_accessor] = resolve_result
                self._resolve_collection(resolve_result, root_node=root_node, result=result, trace=trace)
            elif isinstance(resolve_result, dict):
                # resolved value might be a dict (e.g. when loading a nested yaml with resolve_all=True)
                # wrap again into KCDict and process it (otherwise the node '${yaml:...}' node is not replaced
                # with the loaded dict -> ${select:key:${vars.params}} doesnt work)
                wrapped_resolve_result = from_primitive(resolve_result)
                parent[parent_accessor] = wrapped_resolve_result
                self._resolve_collection(wrapped_resolve_result, root_node=root_node, result=result, trace=trace)
            else:
                # set value
                if isinstance(parent_accessor, int) and isinstance(parent, KCList):
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

    @staticmethod
    def _requires_resolve_scalar(value):
        grammar_tree = parse_scalar(value)
        return len(grammar_tree.children) > 1 or isinstance(grammar_tree.children[0], InterpolatedNode)

    def resolve_scalar(self, value, root_node, trace):
        grammar_tree = parse_scalar(value)
        resolved_scalar = self._resolve_scalar(grammar_tree, root_node=root_node, trace=trace)
        return resolved_scalar

    def _resolve_scalar(self, grammar_node, root_node, trace):
        if isinstance(grammar_node, RootNode):
            resolve_results = [
                self._resolve_scalar(child, root_node=root_node, trace=trace)
                for child in grammar_node.children
            ]
            return self._merge_scalar_resolve_results(resolve_results)
        elif isinstance(grammar_node, FixedNode):
            return grammar_node.value
        elif isinstance(grammar_node, InterpolatedNode):
            # resolve children
            resolve_results = [
                self._resolve_scalar(child, root_node=root_node, trace=trace)
                for child in grammar_node.children
            ]
            resolve_result = self._merge_scalar_resolve_results(resolve_results)
            # resolve cur node
            if grammar_node.resolver_key not in self.scalar_resolvers:
                from ..errors import invalid_resolver_key
                raise invalid_resolver_key(
                    grammar_node.resolver_key, list(self.scalar_resolvers.keys()),
                    trace, root_node.source_id
                )
            scalar_resolver = self.scalar_resolvers[grammar_node.resolver_key]
            resolved_scalar = scalar_resolver.resolve(resolve_result, root_node=root_node, trace=trace)
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
            resolve_results = to_primitive(resolve_results)
            return "".join(map(Resolver._tostring, resolve_results))

    @staticmethod
    def _tostring(node):
        if isinstance(node, dict):
            child_str = ",".join(f"'{key}':{Resolver._tostring(value)}" for key, value in node.items())
            return f"{{{child_str}}}"
        if isinstance(node, list):
            child_str = ",".join(Resolver._tostring(item) for item in node)
            return f"[{child_str}]"
        if isinstance(node, float):
            # use yaml format instead of python format as otherwise floats are loaded as string later on
            # yaml.safe_dump has weird behavior when called with plain float (yaml.safe_dump(node) == '1.0e-06\n...\n')
            return yaml.safe_dump([node])[2:].strip()
        return str(node)

    def pre_process(self, node):
        return self._process(node, self.pre_processors)

    def post_process(self, node):
        return self._process(node, self.post_processors)

    def _process(self, node, processors):
        wrapped = dict(root=node)
        self._process_recursive(wrapped, trace=[], processors=processors)
        if "root" not in wrapped:
            from ..errors import empty_result
            raise empty_result()
        return wrapped["root"]

    def _process_recursive(self, node, trace, processors):
        for processor in processors:
            processor.preorder_process(node, trace=trace)
        if isinstance(node, (dict, KCDict)):
            keys = list(node.keys())
            for key in keys:
                # collection might change during processing (e.g. IfPostProcessor)
                if key not in node.keys(): continue
                trace.append((node, key))
                self._process_recursive(node[key], trace=trace, processors=processors)
                trace.pop()
        elif isinstance(node, (list, KCList)):
            for i, item in enumerate(node):
                trace.append((node, i))
                self._process_recursive(item, trace=trace, processors=processors)
