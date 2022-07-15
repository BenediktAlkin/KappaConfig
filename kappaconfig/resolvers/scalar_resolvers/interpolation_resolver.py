from .scalar_resolver import ScalarResolver
from ...entities.wrappers import KCScalar
from ...functional.util import select
from ...grammar.accessor_grammar import parse_accessors


class InterpolationResolver(ScalarResolver):
    def resolve(self, value, root_node, trace, **__):
        accessors = parse_accessors(value)
        node = select(root_node=root_node, accessors=accessors, trace=trace)
        if isinstance(node, KCScalar):
            return node.value
        return node
