from .scalar_resolver import ScalarResolver

class InterpolationResolver(ScalarResolver):
    def inorder_resolve(self, node, root_node, result):
        raise NotImplementedError