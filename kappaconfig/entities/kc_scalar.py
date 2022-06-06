from .kc_object import KCObject
from ..grammar.tree_parser import TreeParser

class KCScalar(KCObject):
    def __init__(self, value):
        self.value = value
