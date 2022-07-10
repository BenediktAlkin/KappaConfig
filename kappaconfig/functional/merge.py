from ..entities.wrappers import KCDict, KCList
from copy import deepcopy
from ..grammar.accessor_grammar import parse_accessors
from .util import select

def merge(base, to_merge):
    """
    merges two objects into one
    :param base:
    :param to_merge:
    :param allow_path_accessors:
    if True -> base={'obj.property': 5} to_merge={'obj': 3} will return {'obj.property': 5, 'obj': 3}
    if False -> base={'obj.property': 5} to_merge={'obj': 3} will return {'obj'} as base is resolved into
    {'obj': {'property': 5}}
    if False -> base={'obj': 3} to_merge={'obj.property': 5} will throw an error as 'obj' should have a property
    'property' but 'obj' is an int
    :return: merged object where to_merge dominates base i.e. base={'obj': 5} to_merge={'obj': 3} will return {'obj': 3}
    """
    # TODO allow_path_accessors is not implemented yet in merge
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
        accessors = parse_accessors(key)
        node = select(base, accessors[:-1])
        accessor = accessors[-1]

        if isinstance(node, (KCList, list)):
            # allow appending to a list if the last accessor is 'add' or 'append'
            if accessor in ["add", "append"]:
                if not isinstance(value, (KCList, list)):
                    from ..errors import unexpected_type_error
                    raise unexpected_type_error([KCList, list], value)
                node += value
            # allow overwriting a list if the last accessor is 'set'
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