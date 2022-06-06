from .collection_resolver import CollectionResolver
from ...entities.wrappers import KCDict

class TemplateResolver(CollectionResolver):
    def __init__(self):
        super().__init__()

    def preorder_resolve(self, node, root_node, result, trace):
        if isinstance(node, KCDict) and "template" in node:
            template = node["template"]
            raise NotImplementedError