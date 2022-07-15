def accessors_to_string(accessors):
    if accessors is None or len(accessors) == 0:
        return ""

    if isinstance(accessors[0], int):
        result = f"[{accessors[0]}]"
    else:
        result = f"{accessors[0]}"
    for accessor in accessors[1:]:
        if isinstance(accessor, int):
            result += f"[{accessor}]"
        else:
            result += f".{accessor}"
    return result


def trace_to_full_accessor(trace):
    if trace is None: return ""
    accessors = list(map(lambda tr: tr[1], trace[1:]))
    return accessors_to_string(accessors)
