from .scalar_resolver import ScalarResolver
from ...functional.util import select
from ...entities.wrappers import KCScalar
from ...grammar.accessor_grammar import parse_accessor

class InterpolationResolver(ScalarResolver):
    def resolve(self, value, root_node, trace, **__):
        accessors = parse_accessor(value)
        node = select(root_node=root_node, accessors=accessors, trace=trace)
        if isinstance(node, KCScalar):
            return node.value
        return node