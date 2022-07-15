import yaml

from ..entities.grammar_tree_nodes import RootNode, InterpolatedNode, FixedNode
from ..entities.wrappers import KCScalar
from ..functional.load import from_string


def parse_scalar(value):
    root_node = RootNode()
    _parse_scalar(value, root_node)
    return root_node


def _parse_scalar(value, parent_node):
    if isinstance(value, KCScalar):
        value = value.value
    if not isinstance(value, str):
        from ..errors import unexpected_type_error
        raise unexpected_type_error(str, value)

    while True:
        if len(value) == 0:
            return
        if "${" not in value:
            parent_node.children.append(FixedNode(value))
            return

        brace_start = value.index("${")
        if brace_start != 0:
            parent_node.children.append(FixedNode(value[:brace_start]))
        value = value[brace_start + 2:]
        brace_end = _find_brace_end(value)

        value_in_braces = value[:brace_end]
        colon_idx = _find_colon(value_in_braces)
        if colon_idx == -1:
            if len(value_in_braces) == 0:
                from ..errors import empty_resolver_value_error
                raise empty_resolver_value_error(value_in_braces)
            node = InterpolatedNode(None)
        elif colon_idx == 0:
            from ..errors import empty_resolver_key_error
            raise empty_resolver_key_error(value_in_braces)
        else:
            if len(value_in_braces) == colon_idx + 1:
                from ..errors import empty_resolver_value_error
                raise empty_resolver_value_error(value_in_braces)
            node = InterpolatedNode(value_in_braces[:colon_idx])
        parent_node.children.append(node)

        # parse recursively
        _parse_scalar(value[colon_idx + 1:brace_end], node)
        value = value[brace_end + 1:]


def _find_brace_end(value):
    nesting_level = 1
    for i in range(len(value)):
        if value[i] == "}":
            nesting_level -= 1
            if nesting_level == 0:
                return i
        if value[i] == "$" and i != len(value) - 2 and value[i + 1] == "{":
            nesting_level += 1
    from ..errors import missing_closing_brace_error
    raise missing_closing_brace_error(value)


def _find_colon(value):
    if "${" in value:
        value = value[:value.index("${")]
    if ":" not in value:
        return -1
    return value.index(":")


def parse_resolver_args_and_value(args_and_value, n_args=None):
    args = []
    remaining_str = args_and_value
    while True:
        if ":" not in remaining_str:
            break
        if n_args is not None and len(args) >= n_args:
            # if the value can have a colon inside it (e.g. a ${yaml:<yaml_file>} node can resolve to 'x:5')
            # it needs to specify n_args in order to only parse the parameters
            break
        colon_idx = remaining_str.index(":")
        arg_str = remaining_str[:colon_idx]
        if len(arg_str) == 0:
            from ..errors import empty_parameter_error
            raise empty_parameter_error(args_and_value)

        # parse into primitives (e.g. parse '5' to 5)
        # also removes leading/trailing whitespaces for strings
        parsed_arg = yaml.safe_load(arg_str)
        args.append(parsed_arg)
        remaining_str = remaining_str[colon_idx + 1:]

    # value is the remainig string after the last colon (and is required)
    if len(remaining_str) == 0:
        from ..errors import missing_scalar_resolver_value
        raise missing_scalar_resolver_value(args_and_value)
    value = from_string(remaining_str)

    # raise error if wrong number of parameters
    if n_args is not None and len(args) != n_args:
        if len(args) < n_args:
            from ..errors import missing_parameter_error
            raise missing_parameter_error(args_and_value, n_args)
        else:
            # there is no way to tell if there are superflous parameters as they are absorbed into the value
            # a value can contain colons so there is no way to tell if it is a parameter or part of the value
            pass

    return args, value
