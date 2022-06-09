from .resolver import Resolver
from .scalar_resolvers.interpolation_resolver import InterpolationResolver
from .scalar_resolvers.eval_resolver import EvalResolver
from .collection_resolvers.template_resolver import TemplateResolver
from .collection_resolvers.missing_value_resolver import MissingValueResolver
from .scalar_resolvers.nested_yaml_resolver import NestedYamlResolver
from .scalar_resolvers.select_resolver import SelectResolver
from .post_processors.remove_vars_post_processor import RemoveVarsPostProcessor
from .post_processors.remove_nones_post_processor import RemoveNonesPostProcessor


class DefaultResolver(Resolver):
    def __init__(self, template_path=None, **templates):
        super().__init__(
            collection_resolvers=[
                TemplateResolver(template_path=template_path, **(templates or {})),
                MissingValueResolver(),
            ],
            default_scalar_resolver=InterpolationResolver(),
            scalar_resolvers=dict(
                eval=EvalResolver(),
                yaml=NestedYamlResolver(template_path=template_path, **(templates or {})),
                select=SelectResolver(),
            ),
            post_processors=[
                RemoveVarsPostProcessor(),
                RemoveNonesPostProcessor(),
            ]
        )