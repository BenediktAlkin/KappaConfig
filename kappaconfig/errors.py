def unexpected_type_error(expected_type_or_types, actual_value):
    if isinstance(expected_type_or_types, list):
        expected_type_str = str(list(map(lambda t: t.__name__, expected_type_or_types)))
        expected_type_str = f"[{expected_type_str}]"
        plural_str = "(s)"
    else:
        expected_type_str = f"'{expected_type_or_types.__name__}'"
        plural_str = ""
    msg = f"expected type{plural_str} {expected_type_str} but got '{type(actual_value).__name__}' ({actual_value})"
    return TypeError(msg)

def index_out_of_range_error(idx, max_idx):
    return IndexError(f"index {idx} is out of range (0<={idx}<{max_idx} evaluates to false)")

def dotlist_entry_requires_equal_sign_error():
    return ValueError("every entry in a dotlist requires a '=' character")

def dotlist_requires_sequential_insert_error():
    msg = "constructing a list from a dotlist requires the indices of the list to start at 0 and be in order"
    return ValueError(msg)

def requires_primitive_node_error():
    return TypeError("requires primitive node")

def empty_resolver_key_error(value_in_brace):
    return ValueError(f"empty resolver key in '${{{value_in_brace}}}'")

def empty_resolver_value_error(value_in_brace):
    return ValueError(f"empty resolver value in '${{{value_in_brace}}}'")

def missing_closing_brace_error(value):
    return ValueError(f"missing '}}' in '{value}'")

def missing_closing_bracket_error(value):
    return ValueError(f"missing ']' in '{value}'")

class MissingValueError(Exception):
    pass

def missing_value_error(full_accessor):
    return MissingValueError(full_accessor)

class InvalidAccessorError(Exception):
    pass

def invalid_accessor_error(accessor_until_invalid, full_accessor):
    return InvalidAccessorError(f"invalid accessor '{accessor_until_invalid}' within '{full_accessor}'")