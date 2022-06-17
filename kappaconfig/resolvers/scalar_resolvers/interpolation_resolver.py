from .scalar_resolver import ScalarResolver
from ...functional.util import string_to_accessors, select
from ...entities.wrappers import KCScalar

class InterpolationResolver(ScalarResolver):
    def resolve(self, value, root_node, trace, **__):
        accessors = string_to_accessors(value)
        node = select(root_node=root_node, accessors=accessors, trace=trace)
        if isinstance(node, KCScalar):
            return node.value
        return node