from .resolver import Resolver
from .scalar_resolvers.interpolation_resolver import InterpolationResolver
from .scalar_resolvers.eval_resolver import EvalResolver
from .collection_resolvers.template_resolver import TemplateResolver
from .scalar_resolvers.nested_yaml_resolver import NestedYamlResolver

class DefaultResolver(Resolver):
    def __init__(self, template_path=None, **templates):
        super().__init__(
            TemplateResolver(template_path=template_path, **(templates or {})),
            default_scalar_resolver=InterpolationResolver(),
            eval=EvalResolver(),
            yaml=NestedYamlResolver(template_path=template_path, **(templates or {})),
        )