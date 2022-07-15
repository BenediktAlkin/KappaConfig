def parse_accessors(full_accessor):
    if full_accessor == "": return []

    result = []
    dot_splits = full_accessor.split(".")
    for dot_split in dot_splits:
        if len(dot_split) == 0:
            from ..errors import empty_accessor_error
            raise empty_accessor_error(full_accessor)

        bracket_splits = dot_split.split("[")
        # add dictionary accessor
        if bracket_splits[0] != "":
            dict_accessor = bracket_splits[0]
            if not dict_accessor[0].isalpha():
                from ..errors import dict_accessor_has_to_start_with_letter_error
                raise dict_accessor_has_to_start_with_letter_error(full_accessor, dict_accessor)
            if not dict_accessor.isidentifier():
                from ..errors import dict_accessor_has_to_be_identifier_error
                raise dict_accessor_has_to_be_identifier_error(full_accessor, dict_accessor)
            result.append(bracket_splits[0])

        # add list accessors
        for bracket_split in bracket_splits[1:]:
            # remove closing bracket (']')
            if bracket_split[-1] != "]":
                from ..errors import missing_closing_bracket_error
                raise missing_closing_bracket_error(full_accessor, f"[{bracket_split}")
            list_accessor = bracket_split[:-1]
            try:
                int_accessor = int(list_accessor)
            except ValueError:
                from ..errors import list_accessor_has_to_be_int_error
                raise list_accessor_has_to_be_int_error(full_accessor, f"[{list_accessor}]")
            result.append(int_accessor)
    return result
