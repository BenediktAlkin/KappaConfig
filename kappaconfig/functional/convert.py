from .util import apply
from copy import deepcopy
from ..entities.wrappers import KCDict, KCList, KCScalar

def from_primitive(root_node):
    root_node = deepcopy(root_node)
    wrapped_node = dict(root=root_node)
    apply(root_node, parent_node=wrapped_node, parent_accessor="root", pre_fn=_from_primitive_fn)
    return wrapped_node["root"]

def _from_primitive_fn(node, parent_node, parent_accessor, **_):
    if isinstance(node, dict):
        parent_node[parent_accessor] = KCDict(**node)
    elif isinstance(node, list):
        parent_node[parent_accessor] = KCList(*node)
    elif not isinstance(node, (KCDict, KCList, KCScalar)):
        parent_node[parent_accessor] = KCScalar(node)
