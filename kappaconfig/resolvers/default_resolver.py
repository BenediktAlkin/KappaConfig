from .collection_resolvers.missing_value_resolver import MissingValueResolver
from .collection_resolvers.template_resolver import TemplateResolver
from .processors.if_post_processor import IfPostProcessor
from .processors.remove_nones_post_processor import RemoveNonesPostProcessor
from .processors.remove_vars_post_processor import RemoveVarsPostProcessor
from .resolver import Resolver
from .scalar_resolvers.eval_resolver import EvalResolver
from .scalar_resolvers.interpolation_resolver import InterpolationResolver
from .scalar_resolvers.merge_with_dotlist_resolver import MergeWithDotlistResolver
from .scalar_resolvers.nested_yaml_resolver import NestedYamlResolver
from .scalar_resolvers.select_resolver import SelectResolver


class DefaultResolver(Resolver):
    def __init__(self, template_path=None, **templates):
        template_resolver = TemplateResolver(template_path=template_path, **(templates or {}))
        super().__init__(
            collection_resolvers=[
                template_resolver,
                MissingValueResolver(),
            ],
            default_scalar_resolver=InterpolationResolver(),
            scalar_resolvers=dict(
                eval=EvalResolver(),
                yaml=NestedYamlResolver(
                    resolve_all=True,
                    template_path=template_path,
                    template_resolver=template_resolver,
                    **(templates or {})
                ),
                select=SelectResolver(),
                merge_with_dotlist=MergeWithDotlistResolver(),
            ),
            post_processors=[
                IfPostProcessor(),
                RemoveVarsPostProcessor(),
                RemoveNonesPostProcessor(),
            ]
        )
