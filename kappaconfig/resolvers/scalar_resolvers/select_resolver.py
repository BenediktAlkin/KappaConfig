from .scalar_resolver import ScalarResolver
from ...functional.util import select
from ...grammar.accessor_grammar import parse_accessors
from ...grammar.scalar_grammar import parse_resolver_args_and_value


class SelectResolver(ScalarResolver):
    """
    allows selecting fields within a nested yaml import
    e.g. model: ${select:base:${yaml:models/vit}}
    """

    def resolve(self, args_and_value, root_node, trace, **_):
        args, value = parse_resolver_args_and_value(args_and_value, n_args=1)
        accessors = parse_accessors(args[0])
        node = select(root_node=value, accessors=accessors, trace=trace, source_id=root_node.source_id)
        return node
