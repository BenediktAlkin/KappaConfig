from .scalar_resolver import ScalarResolver
from ...functional.util import string_to_accessors

class InterpolationResolver(ScalarResolver):
    def resolve(self, value, root_node):
        accessors = string_to_accessors(value)
        return select(root_node=root_node, accessors=accessors)