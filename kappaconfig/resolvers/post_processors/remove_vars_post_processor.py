from .post_processor import PostProcessor

class RemoveVarsPostProcessor(PostProcessor):
    def preorder_process(self, node, **_):
        if isinstance(node, dict) and "vars" in node:
            del node["vars"]