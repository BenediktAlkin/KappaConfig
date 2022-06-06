class KCObject:
    def __repr__(self):
        raise NotImplementedError

    def __str__(self):
        return repr(self)

class KCScalar(KCObject):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def __repr__(self):
        return repr(self.value)

class KCDict(KCObject):
    def __init__(self, **kwargs):
        super().__init__()
        self.dict = kwargs

    def __repr__(self):
        return repr(self.dict)

    def __setitem__(self, key, value):
        self.dict[key] = value

    def __getitem__(self, item):
        return self.dict[item]

    def __contains__(self, item):
        return item in self.dict

    def keys(self):
        return self.dict.keys()

    def items(self):
        return self.dict.items()

class KCList(KCObject):
    def __init__(self, *args):
        super().__init__()
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
