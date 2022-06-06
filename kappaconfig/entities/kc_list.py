from .kc_object import KCObject

class KCList(KCObject):
    def __init__(self, *args):
        self.list = list(args)

    def __repr__(self):
        return repr(self.list)

    def _check_accessor(self, accessor):
        if not isinstance(accessor, int):
            raise ValueError(f"expected int argument but got '{accessor}'")
        if not 0 <= accessor < len(self.list):
            raise IndexError(f"index {accessor} is out of range (0<={accessor}<{len(self.list)} evaluates to false)")

    def __setitem__(self, key, value):
        self._check_accessor(key)
        self.list[key] = value

    def __getitem__(self, item):
        return self.list[item]
