from .accessor_grammar import parse_accessor

def parse_dotlist_entry(entry):
    split = entry.split("=")
    if len(split) == 1:
        from..errors import dotlist_entry_requires_equal_sign_error
        raise dotlist_entry_requires_equal_sign_error(entry)
    if len(split) > 2:
        from..errors import dotlist_entry_multiple_equal_signs_error
        raise dotlist_entry_multiple_equal_signs_error(entry)

    accessor = parse_accessor(split[0])
    return accessor, split[1]
