from .util import apply, accessors_to_string
from collections import defaultdict

def to_dotlist(root_node):
    container = dict(accessors=[], result=[])
    apply(root_node, pre_fn=_to_dotlist_pre_fn, post_fn=_to_dotlist_post_fn, container=container)
    return container["result"]

def from_dotlist(dotlist):
    result = defaultdict(dict)


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
