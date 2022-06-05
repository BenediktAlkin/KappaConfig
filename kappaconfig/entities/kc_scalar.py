from .kc_object import KCObject

class KCScalar(KCObject):
    def __init__(self, value):
        self.value = value

    def resolve(self):
        pass