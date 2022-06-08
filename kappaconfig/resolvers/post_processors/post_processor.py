class PostProcessor:
    def process(self, node):
        self._process(node)
        if isinstance(node, dict):
            for key in node.keys():
                self.process(node[key])
        elif isinstance(node, list):
            for item in node:
                self.process(item)

    def _process(self, node):
        raise NotImplementedError