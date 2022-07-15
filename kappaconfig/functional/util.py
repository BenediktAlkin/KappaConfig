from ..entities.wrappers import KCDict, KCList, KCObject, KCScalar


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


def select(root_node, accessors, trace=None, source_id=None):
    cur_node = root_node
    for i, accessor in enumerate(accessors):
        if isinstance(cur_node, KCScalar):
            from ..errors import cant_apply_accessor_to_scalar
            raise cant_apply_accessor_to_scalar(accessor, cur_node)

        try:
            cur_node = cur_node[accessor]
        except:
            from ..errors import invalid_accessor_error
            if source_id is None:
                source_id = root_node.source_id if isinstance(root_node, KCObject) else None
            raise invalid_accessor_error(accessors[:i + 1], trace, source_id)
    return cur_node


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
