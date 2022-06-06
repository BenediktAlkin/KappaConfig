import yaml
from .convert import from_primitive

def from_file_uri(file_uri):
    with open(file_uri) as f:
        return from_primitive(yaml.safe_load(f))

def from_string(yaml_string):
    return from_primitive(yaml.safe_load(yaml_string))