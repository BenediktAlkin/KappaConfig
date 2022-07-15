from .processor import Processor


class RemoveVarsPostProcessor(Processor):
    def preorder_process(self, node, **_):
        if isinstance(node, dict) and "vars" in node:
            del node["vars"]
