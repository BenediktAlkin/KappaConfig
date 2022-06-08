import yaml
from ..entities.grammar_tree_nodes import RootNode, InterpolatedNode, FixedNode
from ..entities.wrappers import KCScalar
from ..functional.load import from_string

def parse_grammar(value):
    root_node = RootNode()
    _parse(value, root_node)
    return root_node


def _parse(value, parent_node):
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
        _parse(value[colon_idx + 1:brace_end], node)
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

def parse_resolver_args_and_value(args_and_value, n_args):
    args = []
    remaining_str = args_and_value
    for i in range(n_args):
        if not ":" in remaining_str:
            from ..errors import missing_parameter_error
            raise missing_parameter_error(args_and_value, n_args)
        colon_idx = remaining_str.index(":")
        arg_str = remaining_str[:colon_idx]
        if len(arg_str) == 0:
            from ..errors import empty_parameter_error
            raise empty_parameter_error(args_and_value)

        # parse into primitives (e.g. parse '5' to 5)
        # also removes leading/trailing whitespaces for strings
        parsed_arg = yaml.safe_load(arg_str)
        args.append(parsed_arg)
        remaining_str = remaining_str[colon_idx+1:]
    return args, from_string(remaining_str)