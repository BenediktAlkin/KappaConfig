class KCObject:
    def __repr__(self):
        raise NotImplementedError

    def __str__(self):
        return repr(self)