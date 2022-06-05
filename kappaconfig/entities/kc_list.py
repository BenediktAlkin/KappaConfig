from .kc_object import KCObject

class KCList(KCObject):
    def __init__(self, initial_list):
        self._list = initial_list

    def _check_accessor(self, accessor):
        if not isinstance(accessor, int):
            raise ValueError(f"expected int argument but got '{accessor}'")
        if not 0 <= accessor < len(self._list):
            raise IndexError(f"index {accessor} is out of range (0<={accessor}<{len(self._list)} evaluates to false)")

    def __setitem__(self, key, value):
        self._check_accessor(key)
        self._list[key] = value

    def __getitem__(self, item):
        self._check_accessor(item)
        return self._list[item]
