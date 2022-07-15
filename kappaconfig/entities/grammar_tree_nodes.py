class GrammarTreeNode:
    def __repr__(self):
        raise NotImplementedError

    def __str__(self):
        return repr(self)


class RootNode(GrammarTreeNode):
    def __init__(self):
        super().__init__()
        self.children = []

    def __repr__(self):
        return "".join(map(str, self.children))


class FixedNode(GrammarTreeNode):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def __repr__(self):
        return self.value


class InterpolatedNode(GrammarTreeNode):
    def __init__(self, resolver_key, *args):
        super().__init__()
        self.children = []
        self.resolver_key = resolver_key
        self.args = args

    def __repr__(self):
        children_repr = str(list(map(str, self.children)))
        resolver_repr = f"{self.resolver_key}:" if self.resolver_key else ""
        return f"${{{resolver_repr}{children_repr}}}"
