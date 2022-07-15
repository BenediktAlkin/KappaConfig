from .accessor_grammar import parse_accessors


def parse_dotlist_entry(entry):
    if "=" not in entry:
        from ..errors import dotlist_entry_requires_equal_sign_error
        raise dotlist_entry_requires_equal_sign_error(entry)
    equals_idx = entry.index("=")
    accessor_string = entry[:equals_idx]
    value_string = entry[equals_idx + 1:]

    accessors = parse_accessors(accessor_string)
    return accessors, value_string, accessor_string
