from .kc_object import KCObject

class KCDict(KCObject):
    def __init__(self, **kwargs):
        self.dict = kwargs

    def __setitem__(self, key, value):
        self.dict[key] = value

    def __getitem__(self, item):
        return self.dict[item]

    def __contains__(self, item):
        return item in self.dict

    def resolve(self):
        return {key: value.resolve() for key, value in self.dict.items()}