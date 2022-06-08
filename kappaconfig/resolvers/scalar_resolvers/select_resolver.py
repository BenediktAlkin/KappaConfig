from .scalar_resolver import ScalarResolver
from ...functional.util import string_to_accessors, select

class SelectResolver(ScalarResolver):
    """
    allows selecting fields within a nested yaml import
    e.g. model: ${select(base):${yaml:models/vit}}
    """

    def resolve(self, value, grammar_node, **_):
        accessors = string_to_accessors(grammar_node.args[0])
        node = select(root_node=value, accessors=accessors)
        return node.value