def apply(node, pre_fn=None, post_fn=None, parent_node=None, parent_accessor=None, container=None):
    # do something before traversing the node
    if pre_fn is not None:
        pre_fn(node=node, parent_node=parent_node, parent_accessor=parent_accessor, container=container)
        # pre_fn might change the config obj
        if parent_node is not None and parent_accessor is not None:
            node = parent_node[parent_accessor]

    # traverse
    if isinstance(node, dict):
        for key, value in node.items():
            apply(value, pre_fn=pre_fn, post_fn=post_fn, parent_node=node, parent_accessor=key, container=container)
    elif isinstance(node, list):
        for i, item in enumerate(node):
            apply(item, pre_fn=pre_fn, post_fn=post_fn, parent_node=node, parent_accessor=i, container=container)

    # do something after traversing the node
    if post_fn is not None:
        post_fn(node=node, parent_node=parent_node, parent_accessor=parent_accessor, container=container)


def accessors_to_string(accessors):
    if len(accessors) == 0: return ""

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
                raise ValueError(f"expected ']' at last position of accessor '{bracket_split}'")
            list_accessor = bracket_split[:-1]
            result.append(int(list_accessor))
    return result