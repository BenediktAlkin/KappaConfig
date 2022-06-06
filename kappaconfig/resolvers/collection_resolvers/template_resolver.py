from .collection_resolver import CollectionResolver
from ...entities.wrappers import KCDict, KCScalar
from ...functional.util import mask_in, mask_out, merge
from ...functional.convert import from_primitive
from ..resolver import Resolver
from ..scalar_resolvers.nested_yaml_resolver import NestedYamlResolver

class TemplateResolver(CollectionResolver):
    def __init__(self, template_path=None, **templates):
        super().__init__()
        # nested yaml templates are resolved after loading/merging with template parameters
        self.nested_yaml_resolver = Resolver(yaml=NestedYamlResolver(template_path=template_path, **templates))

    def preorder_resolve(self, node, root_node, result, trace, root_resolver):
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
                    node_without_template_params = node
                elif isinstance(template, KCScalar):
                    # Template is a string template. String templates need to be self contained but can expect
                    # parameters to be "passed" to them.
                    # string_template:
                    #   template: ${yaml:some_template.yaml}
                    # string_var_template:
                    #   template: ${yaml:some_template.yaml}
                    #   template.vars:
                    #     param: 5
                    resolved_scalar = self.nested_yaml_resolver.resolve_scalar(template, root_node=root_node)
                    # merge template parameters into template
                    template_params_keys = list(filter(lambda key: key.startswith("template."), node.keys()))
                    template_params = mask_in(node, template_params_keys)
                    template_params_to_merge = {k.replace("template.", ""): v for k, v in template_params.items()}
                    kc_resolved_scalar = from_primitive(resolved_scalar)
                    merged_template = merge(kc_resolved_scalar, template_params_to_merge)

                    # remove template params from node
                    node_without_template_params = mask_out(node, template_params_keys)

                    # resolve template with template root as root (for resolving parameterized templates)
                    resolved_template_primitive = root_resolver.resolve(merged_template)
                    # remove "vars" field in template
                    resolved_template_primitive_no_vars = mask_out(resolved_template_primitive, ["vars"])
                    resolved_template = from_primitive(resolved_template_primitive_no_vars)
                else:
                    # KCList not implemented yet
                    raise NotImplementedError


                masked = mask_out(node_without_template_params, ["template"])
                merged = merge(resolved_template, masked)
                parent, accessor = trace[-1]
                parent[accessor] = merged
                node = merged




