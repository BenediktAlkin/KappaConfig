from .collection_resolver import CollectionResolver
from ...entities.wrappers import KCScalar
from ...functional.util import trace_to_full_accessor

class MissingValueResolver(CollectionResolver):
    def preorder_resolve(self, node, root_node, result, trace, root_resolver):
        if isinstance(node, KCScalar) and isinstance(node.value, str) and node.value == "???":
            from ...errors import missing_value_error
            raise missing_value_error(trace_to_full_accessor(trace))
