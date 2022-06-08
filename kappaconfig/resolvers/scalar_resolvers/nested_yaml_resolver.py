from .scalar_resolver import ScalarResolver
from ...entities.wrappers import KCScalar
from ...functional.load import from_string, from_file_uri
from pathlib import Path

class NestedYamlResolver(ScalarResolver):
    def __init__(self, template_path=None, **templates):
        super().__init__()
        self.template_path = template_path
        if self.template_path is not None and isinstance(self.template_path, str):
            self.template_path = Path(self.template_path)

        self.templates = templates
        if any(map(lambda template_value: not isinstance(template_value, str), templates.values())):
            raise TypeError

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
        else:
            # load from template_path
            template = from_file_uri(self.template_path / value)

        return template