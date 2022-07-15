from .functional.to_string import accessors_to_string, trace_to_full_accessor


def _source_id_str(source_id):
    if source_id is None:
        return ""
    return f" of source '{source_id}'"


def unexpected_type_error(expected_type_or_types, actual_value):
    if isinstance(expected_type_or_types, list):
        expected_type_str = str(list(map(lambda t: t.__name__, expected_type_or_types)))
        expected_type_str = f"[{expected_type_str}]"
        plural_str = "(s)"
    else:
        expected_type_str = f"'{expected_type_or_types.__name__}'"
        plural_str = ""
    return TypeError(
        f"expected type{plural_str} {expected_type_str} but got '{type(actual_value).__name__}' ({actual_value})"
    )


def index_out_of_range_error(idx, max_idx):
    return IndexError(f"index {idx} is out of range (0<={idx}<{max_idx} evaluates to false)")


class DotlistGrammarError(Exception):
    pass


def dotlist_entry_requires_equal_sign_error(entry):
    return DotlistGrammarError(f"invalid dotlist entry '{entry}' (every entry in a dotlist requires a '=' character)")


def requires_sequential_insert_error():
    return ValueError(
        "constructing a list from a dotlist requires the indices of the list to start at 0 and be in order"
    )


def dotlist_resolver_empty_entry(value, trace):
    return ValueError(
        f"expected space-seperated dotlist entries (e.g. 'value=3 obj.key=34') but found empty entry in '{value}' "
        f"of node '{trace_to_full_accessor(trace)}'"
    )


def requires_primitive_node_error():
    return TypeError("requires primitive node")


def empty_resolver_key_error(value_in_brace):
    return ValueError(f"empty resolver key in '${{{value_in_brace}}}'")


def empty_resolver_value_error(value_in_brace):
    return ValueError(f"empty resolver value in '${{{value_in_brace}}}'")


def missing_closing_brace_error(value):
    return ValueError(f"missing '}}' in '{value}'")


class AccessorGrammarError(Exception):
    pass


def empty_accessor_error(full_accessor):
    return AccessorGrammarError(f"empty accessor in '{full_accessor}'")


def dict_accessor_has_to_be_identifier_error(full_accessor, dict_accessor):
    msg = f"dictionary accessor '{dict_accessor}' in '{full_accessor}' has to be valid python identifier"
    return AccessorGrammarError(msg)


def dict_accessor_has_to_start_with_letter_error(full_accessor, dict_accessor):
    return AccessorGrammarError(
        f"dictionary accessor '{dict_accessor}' of '{full_accessor}' has to start with letter but started with "
        f"'{dict_accessor[0]}'"
    )


def missing_closing_bracket_error(full_accessor, list_accessor):
    return AccessorGrammarError(f"missing ']' in '{list_accessor}' of accessor '{full_accessor}'")


def list_accessor_has_to_be_int_error(full_accessor, list_accessor):
    return AccessorGrammarError(
        f"list accessor '{list_accessor}' of accessor '{full_accessor}' has to convertable to int")


class MissingValueError(Exception):
    pass


def missing_value_error(trace):
    return MissingValueError(trace_to_full_accessor(trace))


class InvalidAccessorError(Exception):
    pass


def invalid_accessor_error(accessors_until_invalid, trace, source_id=None):
    return InvalidAccessorError(
        f"invalid accessor '{accessors_to_string(accessors_until_invalid)}' in node '{trace_to_full_accessor(trace)}'"
        f"{_source_id_str(source_id)}"
    )


def recursive_resolving_error(trace):
    return RecursionError(f"encountered recursion in node '{trace_to_full_accessor(trace)}'")


class CantApplyAccessorToScalar(Exception):
    pass


def cant_apply_accessor_to_scalar(accessor, scalar):
    # in some cases the scalar repr is already wrapped into ' --> remove duplicate ''
    scalar_str = f"'{scalar}'".replace("''", "'")
    return CantApplyAccessorToScalar(f"can't apply accessor '{accessor}' to scalar {scalar_str}")


def empty_parameter_error(args_and_value_str):
    return ValueError(f"empty parameter in '{args_and_value_str}'")


def missing_parameter_error(args_and_value_str, n_args):
    return ValueError(f"missing parameter in '{args_and_value_str}', expected {n_args} parameters")


def missing_scalar_resolver_value(args_and_value_str):
    return ValueError(f"missing value for ScalarResolver in '{args_and_value_str}'")


def invalid_resolver_key(resolver_key, valid_keys, trace, source_id=None):
    # don't use key error here as it escapes the whole string and the ' characters
    return ValueError(
        f"invalid resolver key '{resolver_key}' in node '{trace_to_full_accessor(trace)}' "
        f"(valid keys are: {valid_keys}){_source_id_str(source_id)}"
    )


def empty_result():
    return MissingValueError("empty result")


def incompatible_type(type1, type2):
    return TypeError(f"type '{type1}' is incompatible with '{type2}'")


def list_merge_invalid_resolving_strategy(key):
    return ValueError(f"merging two lists requires valid resolving strategy (key='{key}')")


def template_path_has_to_be_set(template_key, valid_templates):
    return ValueError(
        f"invalid template key '{template_key}' (no template path set and template key is not in "
        f"{str(valid_templates)})"
    )


def template_file_doesnt_exist(file_uri):
    return FileNotFoundError(f"template file '{file_uri}' doesn't exist")


def invalid_evaluate_expression(expression, error, trace, source_id=None):
    return ValueError(
        f"invalid eval expression '{expression}' (raised {type(error).__name__}: {str(error)}) in node "
        f"'{trace_to_full_accessor(trace)}'{_source_id_str(source_id)}"
    )


def invalid_unpack_operation(full_accessors, scalar_accessors):
    return ValueError(
        f"invalid unpack operation: can't unpack '{accessors_to_string(full_accessors)}' as "
        f"'{accessors_to_string(scalar_accessors)}' is a scalar"
    )
