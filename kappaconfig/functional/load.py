import sys
import yaml
from .convert import from_primitive
from .dotlist import from_dotlist

def from_file_uri(file_uri):
    with open(file_uri) as f:
        return from_primitive(yaml.safe_load(f))

def from_string(yaml_string):
    if not isinstance(yaml_string, str):
        from ..errors import unexpected_type_error
        raise unexpected_type_error(str, yaml_string)
    return from_primitive(yaml.safe_load(yaml_string))

def from_cli():
    """ e.g. python main.py obj.key=value """
    # filter out stuff from tests
    for i in range(1, len(sys.argv)):
        if "tests" in sys.argv[i] and ".py" in sys.argv[i]:
            del sys.argv[i]
    return from_primitive(from_dotlist(sys.argv[1:]))