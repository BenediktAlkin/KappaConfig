import unittest

from kappaconfig.functional.load import from_string
from kappaconfig.resolvers.resolver import Resolver
from kappaconfig.resolvers.scalar_resolvers.nested_yaml_resolver import NestedYamlResolver
from kappaconfig.resolvers.scalar_resolvers.select_resolver import SelectResolver


class TestNestedYamlResolver(unittest.TestCase):
    def _resolve_and_assert(self, input_, expected, templates):
        resolver = Resolver(
            scalar_resolvers=dict(
                select=SelectResolver(),
                yaml=NestedYamlResolver(**templates),
            ),
        )
        actual = resolver.resolve(from_string(input_))
        self.assertEqual(expected, actual)

    def test_scalar_nested_yaml(self):
        input_ = """
        somekey: ${yaml:test.yaml}
        """
        templates = {"test.yaml": "5"}
        expected = dict(
            somekey=5,
        )
        self._resolve_and_assert(input_, expected, templates)

    def test_list_nested_yaml(self):
        input_ = """
        somekey: ${yaml:test.yaml}
        """
        templates = {"test.yaml": "- 5"}
        expected = dict(
            somekey=[5],
        )
        self._resolve_and_assert(input_, expected, templates)

    def test_scalar_root_yaml(self):
        input_ = """
        ${yaml:test.yaml}
        """
        templates = {"test.yaml": "5"}
        expected = 5
        self._resolve_and_assert(input_, expected, templates)

    def test_simple(self):
        input_ = """
        somekey: ${yaml:test.yaml}
        """
        templates = {"test.yaml": "template_key: template_value"}
        expected = dict(
            somekey=dict(
                template_key="template_value",
            ),
        )
        self._resolve_and_assert(input_, expected, templates)

    def test_nested(self):
        input_ = """
        some_obj: ${yaml:${yaml:test.yaml}}
        """
        templates = {"test.yaml": "other_yaml.yaml", "other_yaml.yaml": "some_key"}
        expected = dict(
            some_obj="some_key"
        )
        self._resolve_and_assert(input_, expected, templates)

    def test_select_from_nested_yaml(self):
        input_ = """
        some_obj: ${select:some_key:${yaml:test}}
        """
        templates = {"test.yaml": "some_key: some_value"}
        expected = dict(
            some_obj="some_value"
        )
        self._resolve_and_assert(input_, expected, templates)
