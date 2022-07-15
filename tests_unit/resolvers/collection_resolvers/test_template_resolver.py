import unittest

from kappaconfig.functional.load import from_string
from kappaconfig.resolvers.collection_resolvers.template_resolver import TemplateResolver
from kappaconfig.resolvers.resolver import Resolver
from kappaconfig.resolvers.scalar_resolvers.eval_resolver import EvalResolver
from kappaconfig.resolvers.scalar_resolvers.interpolation_resolver import InterpolationResolver
from kappaconfig.resolvers.scalar_resolvers.nested_yaml_resolver import NestedYamlResolver


class TestTemplateResolver(unittest.TestCase):
    def _resolve_and_assert(self, input_, expected, templates=None):
        resolver = Resolver(
            collection_resolvers=[
                TemplateResolver(**(templates or {})),
            ],
            default_scalar_resolver=InterpolationResolver(),
            scalar_resolvers=dict(
                eval=EvalResolver(),
                yaml=NestedYamlResolver(**(templates or {})),
            ),
        )
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

    def test_set_list_of_template(self):
        input_ = """
        template: ${yaml:tmp.yaml}
        template.x_transforms.set:
          - kind: random_horizontal_flip
        """
        expected = dict(
            kind="imagenet",
            x_transforms=[
                dict(kind="random_horizontal_flip"),
            ],
        )
        templates = {
            "tmp.yaml": """
            kind: imagenet
            x_transforms:
              - kind: resize
                size: 256
            """
        }
        self._resolve_and_assert(input_, expected, templates)

    def test_append_to_list_of_template(self):
        input_ = """
        template: ${yaml:tmp.yaml}
        template.x_transforms.add:
          - kind: random_horizontal_flip
        """
        expected = dict(
            kind="imagenet",
            x_transforms=[
                dict(kind="resize", size=256),
                dict(kind="random_horizontal_flip"),
            ],
        )
        templates = {
            "tmp.yaml": """
            kind: imagenet
            x_transforms:
              - kind: resize
                size: 256
            """
        }
        self._resolve_and_assert(input_, expected, templates)

    def test_nested_parameter_passing(self):
        input_ = """
        template: ${yaml:optim.yaml}
        template.vars.total_epochs: 100
        """
        templates = {
            "optim.yaml": """
            vars:
              total_epochs: ???
            kind: SGD
            schedule:
              template: ${yaml:schedule}
              template.vars.epochs: ${vars.total_epochs}
            """,
            "schedule.yaml": """
            vars:
              epochs: ???
            kind: linear
            end_epoch: ${vars.epochs}
            """
        }
        expected = dict(
            kind="SGD",
            schedule=dict(
                kind="linear",
                end_epoch=100,
            )
        )
        self._resolve_and_assert(input_, expected, templates)
