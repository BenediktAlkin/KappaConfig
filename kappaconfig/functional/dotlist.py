from .util import apply, accessors_to_string, string_to_accessors
from ..entities.wrappers import KCObject
import yaml

def from_dotlist(dotlist):
    result = dict(root={})
    for entry in dotlist:
        accessor_value_split = entry.split("=")
        if len(accessor_value_split) != 2:
            raise ValueError("every entry in a dotlist requires a '=' character")
        accessor_string, value = accessor_value_split
        accessors = string_to_accessors(accessor_string)

        # create missing parent objects
        prev_node = result["root"]
        for accessor_idx in range(len(accessors[:-1])):
            cur_accessor = accessors[accessor_idx]
            next_accessor = accessors[accessor_idx + 1]

            # create missing datastructures
            if isinstance(next_accessor, int):
                # create list (if it doesn't exist already)
                if isinstance(cur_accessor, int):
                    if len(prev_node) != cur_accessor:
                        raise ValueError
                    prev_node.append([])
                elif cur_accessor not in prev_node:
                    prev_node[cur_accessor] = []
            else:
                # create dict (if it doesn't exist already)
                if isinstance(cur_accessor, int):
                    if len(prev_node != cur_accessor):
                        raise ValueError
                    prev_node.append({})
                elif cur_accessor not in prev_node:
                    prev_node[cur_accessor] = {}

            # progress to next accessor
            prev_node = prev_node[cur_accessor]

        # parse value
        parsed_value = yaml.safe_load(value)

        # insert current value
        last_accessor = accessors[-1]
        if isinstance(last_accessor, int):
            if len(prev_node) != last_accessor:
                raise ValueError("dotlist with list accessors has to be in sequential order")
            prev_node.append(parsed_value)
        else:
            prev_node[last_accessor] = parsed_value

    return result["root"]


def to_dotlist(root_node):
    if isinstance(root_node, KCObject):
        root_node = root_node.resolve()
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
