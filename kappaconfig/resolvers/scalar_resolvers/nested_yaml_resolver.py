from .scalar_resolver import ScalarResolver
from ...entities.wrappers import KCObject
from ...functional.load import from_string, from_file_uri

class NestedYamlResolver(ScalarResolver):
    def __init__(self, resolver=None, template_path=None, **templates):
        super().__init__()
        self.resolver = resolver
        self.template_path = template_path
        self.templates = templates

    def resolve(self, value, *_, **__):
        if not isinstance(value, str) or not value.endswith(".yaml"):
            raise ValueError

        if value in self.templates:
            # load from templates dict (pretty much only used for testing)
            template = from_string(self.templates[value])
        else:
            # load from template_path
            template = from_file_uri(self.template_path / value)

        # resolve nested yaml
        if self.resolver and isinstance(template, KCObject):
            template = self.resolver.resolve(template)

        return template