from .scalar_resolver import ScalarResolver
from ...functional.util import string_to_accessors, select

class InterpolationResolver(ScalarResolver):
    def resolve(self, value, root_node, **__):
        accessors = string_to_accessors(value)
        node = select(root_node=root_node, accessors=accessors)
        return node.value