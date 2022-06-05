from .kc_object import KCObject

class KCScalar(KCObject):
    def __init__(self, value):
        self.value = value

    def resolve(self):
        if not isinstance(self.value, str):
            return self.value

        # TODO
        return self.value