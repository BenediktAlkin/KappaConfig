from .collection_resolver import CollectionResolver
from ...entities.wrappers import KCDict, KCScalar
from ...functional.util import mask_out, merge
from ...functional.convert import from_primitive

class TemplateResolver(CollectionResolver):
    def __init__(self, resolver=None):
        super().__init__()
        self.resolver = resolver

    def preorder_resolve(self, node, root_node, result, trace):
        if isinstance(node, KCDict):
            while True:
                if "template" not in node:
                    break
                template = node["template"]

                if isinstance(template, KCDict):
                    # template is a dictionary template (nothing needs to be resolved)
                    # dict_template:
                    #   template:
                    #     key: value
                    resolved_template = template
                elif isinstance(template, KCScalar):
                    # Template is a string template. String templates need to be self contained but can expect
                    # parameters to be "passed" to them.
                    # string_template:
                    #   template: ${yaml:some_template.yaml}
                    # string_var_template:
                    #   template: ${yaml:some_template.yaml}
                    #   template.vars:
                    #     param: 5
                    if self.resolver is None:
                        raise ValueError
                    resolved_scalar = self.resolver.resolve_scalar(template, root_node=root_node)
                    resolved_template = from_primitive(resolved_scalar)
                else:
                    # KCList not implemented yet
                    raise NotImplementedError


                masked = mask_out(node, ["template"])
                merged = merge(resolved_template, masked)
                parent, accessor = trace[-1]
                parent[accessor] = merged
                node = merged




