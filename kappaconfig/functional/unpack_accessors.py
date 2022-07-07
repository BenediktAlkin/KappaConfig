from ..entities.wrappers import KCDict, KCObject, KCList, KCScalar
from .util import apply, accessors_to_string
from copy import deepcopy
from ..grammar.accessor_grammar import parse_accessor

def unpack_accessors(root_node):
    # TODO prettier error message
    assert isinstance(root_node, KCObject)

    root_node = deepcopy(root_node)
    wrapped = KCDict(root=root_node)
    apply(wrapped, pre_fn=_unpack_accessors_pre_fn)
    return root_node

def _unpack_accessors_pre_fn(node, **_):
    if not isinstance(node, KCDict):
        return

    keys = list(node.keys())
    for key in keys:
        accessors = parse_accessor(key)
        if len(accessors) == 1:
            continue
        value = node.pop(key)

        # create missing parent objects
        prev_node = node
        for accessor_idx in range(len(accessors[:-1])):
            cur_accessor = accessors[accessor_idx]
            next_accessor = accessors[accessor_idx + 1]

            # lists can only be created in sequential order
            if isinstance(cur_accessor, int):
                if len(prev_node) != cur_accessor:
                    from ..errors import dotlist_requires_sequential_insert_error
                    raise dotlist_requires_sequential_insert_error()

            # create missing datastructures
            if isinstance(next_accessor, int):
                # create list (if it doesn't exist already)
                if isinstance(cur_accessor, int):
                    prev_node.append([])
                elif cur_accessor not in prev_node:
                    prev_node[cur_accessor] = KCList()
            else:
                # create dict (if it doesn't exist already)
                if isinstance(cur_accessor, int):
                    prev_node.append({})
                elif cur_accessor not in prev_node:
                    prev_node[cur_accessor] = KCDict()

            # progress to next accessor
            prev_node = prev_node[cur_accessor]

        # in some cases the unpacking is invalid
        # obj: 5
        # obj.value: 3
        # can't process obj.value as it tries to access the property 'value' of 'obj' which doesn't exist as it is 5
        if isinstance(prev_node, KCScalar):
            from ..errors import invalid_unpack_operation
            raise invalid_unpack_operation(key, accessors_to_string(accessors[:-1]))

        # insert current value
        last_accessor = accessors[-1]
        if isinstance(last_accessor, int):
            if len(prev_node) != last_accessor:
                from ..errors import dotlist_requires_sequential_insert_error
                raise dotlist_requires_sequential_insert_error()
            prev_node.append(value)
        else:
            prev_node[last_accessor] = value
