import unittest

from kappaconfig.functional.load import from_string
from kappaconfig.resolvers.collection_resolvers.template_resolver import TemplateResolver
from kappaconfig.resolvers.scalar_resolvers.nested_yaml_resolver import NestedYamlResolver
from kappaconfig.resolvers.scalar_resolvers.eval_resolver import EvalResolver
from kappaconfig.resolvers.scalar_resolvers.interpolation_resolver import InterpolationResolver
from kappaconfig.resolvers.resolver import Resolver

class TestTemplateResolver(unittest.TestCase):
    def _resolve_and_assert(self, input_, expected, templates=None):
        resolver = Resolver(eval=EvalResolver(), default_scalar_resolver=InterpolationResolver())
        template_resolver = TemplateResolver(**(templates or {}))
        resolver.collection_resolvers.append(template_resolver)
        resolver.scalar_resolvers["yaml"] = NestedYamlResolver(**(templates if templates else {}))
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

    def test_simple_string_template(self):
        input_ = """
        some_obj:
          template: ${yaml:tmp.yaml}
          template_key: 5
          other_key: 120
        """
        expected = dict(
            some_obj=dict(
                template_key=5,
                other_key=120,
            ),
        )
        templates = {"tmp.yaml": "template_key: 10"}
        self._resolve_and_assert(input_, expected, templates)

    def test_overwrite_template_value(self):
        input_ = """
        some_obj:
          template: ${yaml:tmp.yaml}
          template.template_key: 20
          other_key: 120
        """
        expected = dict(
            some_obj=dict(
                template_key=20,
                other_key=120,
            ),
        )
        templates = {"tmp.yaml": "template_key: 10"}
        self._resolve_and_assert(input_, expected, templates)

    def test_parameterized_template(self):
        input_ = """
        schedule:
          template: ${yaml:tmp.yaml}
          template.vars.total_epochs: 20
        """
        expected = dict(
            schedule=dict(
                vars=dict(
                    total_epochs=20,
                ),
                warmup_epochs=1,
                cosine_epochs=19,
            )
        )
        templates = {
            "tmp.yaml": """
            vars:
              total_epochs: 100
            warmup_epochs: ${eval:${vars.total_epochs}*0.05}
            cosine_epochs: ${eval:${vars.total_epochs}*0.95}
            """
        }
        self._resolve_and_assert(input_, expected, templates)
