import unittest

from kappaconfig.functional.load import from_string
from kappaconfig.resolvers.collection_resolvers.template_resolver import TemplateResolver
from kappaconfig.resolvers.resolver import Resolver

class TestTemplateResolver(unittest.TestCase):
    def _resolve_and_assert(self, input_, expected):
        resolver = Resolver()
        template_resolver = TemplateResolver(resolver=resolver)
        resolver.collection_resolvers.append(template_resolver)
        actual = resolver.resolve(from_string(input_))
        self.assertEqual(expected, actual)

    def test_simple(self):
        input_ = """
        some_obj:
          template:
            template_key: template_value
          obj_key: 5
        """
        expected = dict(
            some_obj=dict(
                template_key="template_value",
                obj_key=5,
            ),
        )
        self._resolve_and_assert(input_, expected)

    def test_simple_overwrite(self):
        input_ = """
        some_obj:
          template:
            template_key: template_value
          template_key: 5
        """
        expected = dict(
            some_obj=dict(
                template_key=5,
            ),
        )
        self._resolve_and_assert(input_, expected)
