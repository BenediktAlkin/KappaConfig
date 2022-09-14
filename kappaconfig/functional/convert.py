from copy import deepcopy

from .util import apply
from ..entities.wrappers import KCDict, KCList, KCScalar


def from_primitive(root_node):
    root_node = deepcopy(root_node)
    wrapped_node = dict(root=root_node)
    apply(root_node, parent_node=wrapped_node, parent_accessor="root", pre_fn=_from_primitive_fn)
    return wrapped_node["root"]


def _from_primitive_fn(node, parent_node, parent_accessor, **_):
    if isinstance(node, dict):
        # KCDict(**node) doesn't work here since yaml allows keys other than strings
        parent_node[parent_accessor] = KCDict(node)
    elif isinstance(node, list):
        parent_node[parent_accessor] = KCList(*node)
    elif not isinstance(node, (KCDict, KCList, KCScalar)):
        parent_node[parent_accessor] = KCScalar(node)


def to_primitive(root_node):
    root_node = deepcopy(root_node)
    wrapped_node = dict(root=root_node)
    apply(root_node, parent_node=wrapped_node, parent_accessor="root", pre_fn=_to_primitive_fn)
    return wrapped_node["root"]


def _to_primitive_fn(node, parent_node, parent_accessor, **_):
    if isinstance(node, KCDict):
        parent_node[parent_accessor] = dict(**node.dict)
    elif isinstance(node, KCList):
        parent_node[parent_accessor] = [*node.list]
    elif isinstance(node, KCScalar):
        parent_node[parent_accessor] = node.value
