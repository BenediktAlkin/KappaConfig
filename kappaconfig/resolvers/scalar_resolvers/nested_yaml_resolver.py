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
            raise TypeError("template values have to be string (they are a yaml in string format)")

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

        return template