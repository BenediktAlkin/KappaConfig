def unexpected_type(expected_type_or_types, actual_value):
    if isinstance(expected_type_or_types, list):
        expected_type_str = str(list(map(lambda t: t.__name__, expected_type_or_types)))
        expected_type_str = f"[{expected_type_str}]"
        plural_str = "(s)"
    else:
        expected_type_str = f"'{expected_type_or_types.__name__}'"
        plural_str = ""
    return f"expected type{plural_str} {expected_type_str} but got '{type(actual_value).__name__}' ({actual_value})"

def index_out_of_range(idx, max_idx):
    return f"index {idx} is out of range (0<={idx}<{max_idx} evaluates to false)"

def dotlist_entry_requires_equal_sign():
    return "every entry in a dotlist requires a '=' character"

def dotlist_requires_sequential_insert():
    return "constructing a list from a dotlist requires the indices of the list to start at 0 and be in order"

def requires_primitive_node():
    return "requires primitive node"

def empty_resolver_key(value_in_brace):
    return f"empty resolver key for interpolation '${{{value_in_brace}}}'"

def missing_closing_brace(value):
    return f"missing '}}' in '{value}'"

def missing_closing_bracket(value):
    return f"missing ']' in '{value}'"