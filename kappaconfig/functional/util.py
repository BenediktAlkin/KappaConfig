from ..entities.wrappers import KCDict, KCList, KCObject
from copy import deepcopy

def apply(node, pre_fn=None, post_fn=None, parent_node=None, parent_accessor=None, container=None):
    # do something before traversing the node
    if pre_fn is not None:
        pre_fn(node=node, parent_node=parent_node, parent_accessor=parent_accessor, container=container)
        # pre_fn might change the config obj
        if parent_node is not None and parent_accessor is not None:
            node = parent_node[parent_accessor]

    # traverse
    if isinstance(node, KCDict) or isinstance(node, dict):
        for key, value in node.items():
            apply(value, pre_fn=pre_fn, post_fn=post_fn, parent_node=node, parent_accessor=key, container=container)
    elif isinstance(node, KCList) or isinstance(node, list):
        for i, item in enumerate(node):
            apply(item, pre_fn=pre_fn, post_fn=post_fn, parent_node=node, parent_accessor=i, container=container)

    # do something after traversing the node
    if post_fn is not None:
        post_fn(node=node, parent_node=parent_node, parent_accessor=parent_accessor, container=container)


def accessors_to_string(accessors):
    if accessors is None or len(accessors) == 0:
        return ""

    if isinstance(accessors[0], int):
        result = f"[{accessors[0]}]"
    else:
        result = f"{accessors[0]}"
    for accessor in accessors[1:]:
        if isinstance(accessor, int):
            result += f"[{accessor}]"
        else:
            result += f".{accessor}"
    return result

def string_to_accessors(accessor_str):
    if accessor_str == "": return []

    result = []
    dot_splits = accessor_str.split(".")
    for dot_split in dot_splits:
        bracket_splits = dot_split.split("[")
        # add dictionary accessor
        if bracket_splits[0] != "":
            result.append(bracket_splits[0])

        # add list accessors
        for bracket_split in bracket_splits[1:]:
            # remove closing bracket (']')
            if bracket_split[-1] != "]":
                from ..errors import missing_closing_bracket_error
                raise missing_closing_bracket_error(f"[{bracket_split}")
            list_accessor = bracket_split[:-1]
            result.append(int(list_accessor))
    return result

def trace_to_full_accessor(trace):
    if trace is None: return ""
    accessors = list(map(lambda tr: tr[1], trace[1:]))
    return accessors_to_string(accessors)

def select(root_node, accessors, trace=None, source_id=None):
    cur_node = root_node
    for i, accessor in enumerate(accessors):
        try:
            cur_node = cur_node[accessor]
        except:
            from ..errors import invalid_accessor_error
            if source_id is None:
                source_id = root_node.source_id if isinstance(root_node, KCObject) else None
            raise invalid_accessor_error(accessors_to_string(accessors[:i+1]), trace_to_full_accessor(trace), source_id)
    return cur_node

def merge(base, to_merge):
    base = deepcopy(base)
    to_merge = deepcopy(to_merge)
    return _merge_fn(dict(root=base), dict(root=to_merge))["root"]

def _merge_fn(base, to_merge):
    if not isinstance(base, (KCList, list, KCDict, dict)):
        return to_merge
    if isinstance(to_merge, (KCList, list)) and not isinstance(base, (KCList, list)):
        from ..errors import incompatible_type
        raise incompatible_type(type(base), type(to_merge))
    if isinstance(to_merge, (KCDict, dict)) and not isinstance(base, (KCDict, dict)):
        from ..errors import incompatible_type
        raise incompatible_type(type(base), type(to_merge))

    if isinstance(to_merge, (KCDict, dict)):
        _merge_dict_fn(base, to_merge)
    elif isinstance(to_merge, (KCList, list)):
        _merge_list_fn(base, to_merge)
    else:
        return to_merge
    return base

def _merge_list_fn(base, to_merge):
    for i in range(len(to_merge)):
        if i < len(base):
            base[i] = _merge_fn(base[i], to_merge[i])
        else:
            base.append(to_merge[i])

def _merge_dict_fn(base, to_merge):
    for key, value in to_merge.items():
        accessors = string_to_accessors(key)
        node = select(base, accessors[:-1])
        accessor = accessors[-1]

        # allow appending to a list if the last accessor is 'add' or 'append'
        if isinstance(node, (KCList, list)):
            if accessor in ["add", "append"]:
                if not isinstance(value, (KCList, list)):
                    from ..errors import unexpected_type_error
                    raise unexpected_type_error([KCList, list], value)
                node += value
            elif accessor == "set":
                parent_node = select(base, accessors[:-2])
                parent_node[accessors[-2]] = value
            else:
                from ..errors import list_merge_invalid_resolving_strategy
                raise list_merge_invalid_resolving_strategy(key)
        else:
            if accessor in node:
                node[accessor] = _merge_fn(node[accessor], value)
            else:
                node[accessor] = value

def mask_out(dict_, keys_to_mask_out):
    masked_dict = type(dict_)()
    for key, value in dict_.items():
        if key not in keys_to_mask_out:
            masked_dict[key] = value
    return masked_dict

def mask_in(dict_, keys_to_mask_in):
    masked_dict = type(dict_)()
    for key, value in dict_.items():
        if key in keys_to_mask_in:
            masked_dict[key] = value
    return masked_dict