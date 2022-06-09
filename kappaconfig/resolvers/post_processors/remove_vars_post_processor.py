from .post_processor import PostProcessor

class RemoveVarsPostProcessor(PostProcessor):
    def _process(self, node):
        if isinstance(node, dict) and "vars" in node:
            del node["vars"]