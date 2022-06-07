from .collection_resolver import CollectionResolver
from ...entities.wrappers import KCScalar

class MissingValueResolver(CollectionResolver):
    def __str__(self, missing_value_token="???"):
        super().__init__()
        self.missing_value_token = missing_value_token

    def preorder_resolve(self, node, root_node, result, trace, root_resolver):
        if isinstance(node, KCScalar) and isinstance(node.value, str) and node.value == self.missing_value_token:
            raise ValueError
