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

    def __eq__(self, other):
        return type(self) == type(other) and self.value == other.value

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

    def pop(self, key):
        return self.dict.pop(key)

    def __eq__(self, other):
        return type(self) == type(other) and self.dict == other.dict


class KCList(KCObject):
    def __init__(self, *args):
        super().__init__()
        self.list = list(args)

    def __repr__(self):
        return repr(self.list)

    def _check_accessor(self, accessor):
        if not isinstance(accessor, int):
            from ..errors import unexpected_type_error
            raise unexpected_type_error(int, accessor)
        if not 0 <= accessor < len(self.list):
            from ..errors import index_out_of_range_error
            raise index_out_of_range_error(accessor, len(self.list))

    def __setitem__(self, key, value):
        self._check_accessor(key)
        self.list[key] = value

    def __getitem__(self, item):
        return self.list[item]

    def __iadd__(self, other):
        if not isinstance(other, KCList):
            from ..errors import unexpected_type_error
            raise unexpected_type_error(KCList, other)
        self.list += other.list
        return self.list

    def __len__(self):
        return len(self.list)

    def append(self, item):
        self.list.append(item)

    def __eq__(self, other):
        return type(self) == type(other) and self.list == other.list