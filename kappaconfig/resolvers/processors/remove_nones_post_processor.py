from .processor import Processor


class RemoveNonesPostProcessor(Processor):
    """
    removes nodes that are set to None
    e.g.
    save_logger:
      every_n_epochs: 1
      every_n_updates: None
    resolves to:
    save_logger:
      every_n_epochs: 1
    """

    def preorder_process(self, node, **_):
        if isinstance(node, dict):
            keys = list(node.keys())
            for key in keys:
                if node[key] is None:
                    del node[key]
        elif isinstance(node, list):
            i = 0
            while i < len(node):
                if node[i] is None:
                    del node[i]
                else:
                    i += 1
