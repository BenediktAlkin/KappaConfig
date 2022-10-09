from pathlib import Path

from .scalar_resolver import ScalarResolver
from ..resolver import Resolver
from ..scalar_resolvers.eval_resolver import EvalResolver
from ..scalar_resolvers.interpolation_resolver import InterpolationResolver
from ..scalar_resolvers.merge_with_dotlist_resolver import MergeWithDotlistResolver
from ..scalar_resolvers.select_resolver import SelectResolver
from ...entities.wrappers import KCScalar
from ...functional.load import from_string, from_file_uri
from ..collection_resolvers.missing_value_resolver import MissingValueResolver
from ..processors.if_post_processor import IfPostProcessor
from ..processors.remove_nones_post_processor import RemoveNonesPostProcessor
from ..processors.remove_vars_post_processor import RemoveVarsPostProcessor


class NestedYamlResolver(ScalarResolver):
    def __init__(self, resolve_all, template_path=None, template_resolver=None, **templates):
        super().__init__()
        self.resolve_all = resolve_all
        self.template_path = template_path
        if self.template_path is not None and isinstance(self.template_path, str):
            self.template_path = Path(self.template_path)

        self.templates = templates
        if any(map(lambda template_value: not isinstance(template_value, str), templates.values())):
            raise TypeError("template values have to be string (they are a yaml in string format)")

        scalar_resolvers = dict(
            eval=EvalResolver(),
            yaml=self,
            select=SelectResolver(),
            merge_with_dotlist=MergeWithDotlistResolver()
        )
        if template_resolver is None:
            collection_resolvers = [
                MissingValueResolver(),
            ]
        else:
            collection_resolvers = [
                template_resolver,
                MissingValueResolver(),
            ]
            scalar_resolvers["template"] = template_resolver
        self.resolver = Resolver(
            collection_resolvers=collection_resolvers,
            default_scalar_resolver=InterpolationResolver(),
            scalar_resolvers=scalar_resolvers,
            post_processors=[
                IfPostProcessor(),
                RemoveVarsPostProcessor(),
                RemoveNonesPostProcessor(),
            ]
        )

    def resolve(self, value, **__):
        if isinstance(value, KCScalar):
            value = value.value
        if not isinstance(value, str):
            from ...errors import unexpected_type_error
            raise unexpected_type_error(str, value)
        if not value.endswith(".yaml"):
            value += ".yaml"

        if value in self.templates:
            # load from templates dict (pretty much only used for testing)
            template = from_string(self.templates[value])
            # set source_id (as this simulates loading from file_uri)
            template.source_id = value
        elif self.template_path is None:
            from ...errors import template_path_has_to_be_set
            raise template_path_has_to_be_set(value, list(self.templates.keys()))
        else:
            # load from template_path
            template_path = self.template_path / value
            if not template_path.exists():
                from ...errors import template_file_doesnt_exist
                raise template_file_doesnt_exist(template_path.as_posix())
            template = from_file_uri(self.template_path / value)

        if self.resolve_all:
            resolved = self.resolver.resolve(template)
            return resolved
        else:
            return template
