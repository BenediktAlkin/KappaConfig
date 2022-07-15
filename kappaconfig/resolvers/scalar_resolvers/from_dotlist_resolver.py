from .scalar_resolver import ScalarResolver
from ...functional.load import from_dotlist


class FromDotlistResolver(ScalarResolver):
    """
    allows parsing from a dotlist within a scalar
    e.g. model: ${from_dotlist:some_value=3 obj.value=4}
    """

    def resolve(self, value, trace, **_):
        dotlist = value.split(" ")
        if any(map(lambda entry: len(entry) == 0, dotlist)):
            from ...errors import dotlist_resolver_empty_entry
            raise dotlist_resolver_empty_entry(value, trace)
        return from_dotlist(dotlist)
