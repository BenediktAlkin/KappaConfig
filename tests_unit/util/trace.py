def simulated_trace(*accessors):
    return [(None, "root")] + [(None, accessor) for accessor in accessors]