from .accessor_grammar import parse_accessor

def parse_dotlist_entry(entry):
    if "=" not in entry:
        from..errors import dotlist_entry_requires_equal_sign_error
        raise dotlist_entry_requires_equal_sign_error(entry)
    equals_idx = entry.index("=")
    accessor_string = entry[:equals_idx]
    value_string = entry[equals_idx + 1:]

    accessor = parse_accessor(accessor_string)
    return accessor, value_string
