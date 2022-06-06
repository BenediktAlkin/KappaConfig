from .collection_resolver import CollectionResolver
from ...entities.wrappers import KCDict, KCScalar
from ...functional.util import mask_out, merge

class TemplateResolver(CollectionResolver):
    def __init__(self, resolver):
        super().__init__()
        self.resolver = resolver

    def preorder_resolve(self, node, root_node, result, trace):
        if isinstance(node, KCDict):
            while True:
                if "template" not in node:
                    break
                # A template can be either a dict or a string. For string templates can have a field 'vars' that is
                # passed to the template before the template is resolved.
                # dict_template:
                #   template:
                #     key: value
                # string_template:
                #   template: ${yaml:some_template.yaml}
                # string_var_template:
                #   template: ${yaml:some_template.yaml}
                #   template.vars:
                #     param: 5
                template = node["template"]


                masked = mask_out(node, ["template"])
                merged = merge(template, masked)
                parent, accessor = trace[-1]
                parent[accessor] = merged
                node = merged




