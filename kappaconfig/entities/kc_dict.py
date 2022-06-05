from .kc_object import KCObject

class KCDict(KCObject):
    def __init__(self, initial_dict):
        self._dict = initial_dict

    def __setitem__(self, key, value):
        self._dict[key] = value

    def __getitem__(self, item):
        return self._dict[item]

    def __contains__(self, item):
        return item in self._dict