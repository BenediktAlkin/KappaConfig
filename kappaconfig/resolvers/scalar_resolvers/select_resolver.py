from .scalar_resolver import ScalarResolver
from ...functional.util import string_to_accessors, select
from ...functional.parse_grammar import parse_resolver_args_and_value

class SelectResolver(ScalarResolver):
    """
    allows selecting fields within a nested yaml import
    e.g. model: ${select:base:${yaml:models/vit}}
    """

    def resolve(self, args_and_value, **_):
        args, value = parse_resolver_args_and_value(args_and_value, n_args=1)
        accessors = string_to_accessors(args[0])
        node = select(root_node=value, accessors=accessors)
        return node