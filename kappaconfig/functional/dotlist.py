import yaml

from .convert import from_primitive
from .to_string import accessors_to_string
from .unpack_accessors import create_accessor_structure
from .util import apply
from ..entities.wrappers import KCObject, KCDict
from ..errors import DotlistGrammarError, AccessorGrammarError
from ..grammar.dotlist_grammar import parse_dotlist_entry


def from_dotlist(dotlist, ignore_invalid_entries=False):
    result = KCDict()
    for entry in dotlist:
        try:
            accessors, value, full_accessor = parse_dotlist_entry(entry)
        except (DotlistGrammarError, AccessorGrammarError):
            if ignore_invalid_entries:
                continue
            raise
        value = from_primitive(yaml.safe_load(value))
        create_accessor_structure(result, accessors, value)

    return result


def to_dotlist(root_node):
    if isinstance(root_node, KCObject):
        from ..errors import requires_primitive_node_error
        raise requires_primitive_node_error()
    container = dict(accessors=[], result=[])
    apply(root_node, pre_fn=_to_dotlist_pre_fn, post_fn=_to_dotlist_post_fn, container=container)
    return container["result"]


def _to_dotlist_pre_fn(node, parent_accessor, container, **_):
    if isinstance(node, dict) or isinstance(node, list):
        if parent_accessor is not None:
            container["accessors"].append(parent_accessor)
    else:
        if parent_accessor is None:
            cur_node_accessors = []
        else:
            cur_node_accessors = [parent_accessor]
        accessors = container["accessors"] + cur_node_accessors
        if len(accessors) == 0:
            node_str = str(node)
        else:
            accessor_str = accessors_to_string(container["accessors"] + cur_node_accessors)
            node_str = f"{accessor_str}={str(node)}"
        container["result"].append(node_str)


def _to_dotlist_post_fn(node, parent_accessor, container, **_):
    if isinstance(node, dict) or isinstance(node, list):
        if parent_accessor is not None:
            container["accessors"].pop()
