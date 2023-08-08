import os

from .scalar_resolver import ScalarResolver


class EnvResolver(ScalarResolver):
    def resolve(self, value, root_node, trace, **__):
        try:
            return os.environ[value]
        except Exception as e:
            from ...errors import invalid_environment_variable_key
            raise invalid_environment_variable_key(value, e, trace, root_node.source_id)
