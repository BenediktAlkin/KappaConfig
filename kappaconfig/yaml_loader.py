import yaml

class YamlLoader:
    @staticmethod
    def from_uri(file_uri):
        with open(file_uri) as f:
            return yaml.safe_load(f)