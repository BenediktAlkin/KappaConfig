import sys

import yaml

from .convert import from_primitive
from .dotlist import from_dotlist


def from_file_uri(file_uri):
    with open(file_uri) as f:
        source = yaml.safe_load(f)
    root_node = from_primitive(source)
    root_node.source_id = file_uri
    return root_node


def from_string(yaml_string):
    if not isinstance(yaml_string, str):
        from ..errors import unexpected_type_error
        raise unexpected_type_error(str, yaml_string)
    return from_primitive(yaml.safe_load(yaml_string))


def from_cli(ignore_invalid_args=True):
    """
    e.g. python main.py obj.key=value
    NOTE: unittests can add unexpected arguments that should be removed beforehand (e.g. with sys.argv = sys.argv[:1])
    """
    return from_primitive(from_dotlist(sys.argv[1:], ignore_invalid_entries=ignore_invalid_args))
