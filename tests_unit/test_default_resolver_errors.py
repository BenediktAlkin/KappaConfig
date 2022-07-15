import unittest

from kappaconfig.resolvers.default_resolver import DefaultResolver
import kappaconfig.errors as errors
from kappaconfig.functional.load import from_string
from .util.trace import simulated_trace

class TestDefaultResolverErrors(unittest.TestCase):
    def test_trace_to_invalid_interpolation(self):
        source = """
        trainer:
          batch_size: 64
          loggers:
            train_loss_logger:
              every_n_epochs: ${vars.every_n_epochs}
        """
        resolver = DefaultResolver()
        expected = errors.invalid_accessor_error(["vars"], simulated_trace("trainer", "loggers", "train_loss_logger", "every_n_epochs"))
        with self.assertRaises(type(expected)) as ex:
            resolver.resolve(from_string(source))
        self.assertEqual(expected.args[0], str(ex.exception))

    def test_trace_to_invalid_interpolation_in_template(self):
        source = """
        datasets: 
          template: ${yaml:datasets}
        """
        datasets_template = """
        vars:
          size: 224
        train:
          kind: mvtec
          category: ${vars.category}
        """
        templates = {"datasets.yaml": datasets_template}
        resolver = DefaultResolver(**templates)
        expected = errors.invalid_accessor_error(
            ["vars", "category"], simulated_trace("train", "category"), "datasets.yaml")
        with self.assertRaises(type(expected)) as ex:
            resolver.resolve(from_string(source))
        self.assertEqual(expected.args[0], str(ex.exception))

    def test_trace_to_invalid_interpolation_in_nested_template(self):
        source = """
        trainer: 
          template: ${yaml:trainers/discriminator}
        """
        discriminator_trainer = """
        kind: discriminator_trainer
        loggers:
          template: ${yaml:loggers/default}
        """
        default_loggers = """
        progress_logger:
          kind: progress_logger
          every_n_epochs: ${vars.every_n_epochs}
        """
        templates = {
            "trainers/discriminator.yaml": discriminator_trainer,
            "loggers/default.yaml": default_loggers,
        }
        resolver = DefaultResolver(**templates)
        expected = errors.invalid_accessor_error(["vars"], simulated_trace("progress_logger", "every_n_epochs"), "loggers/default.yaml")
        with self.assertRaises(type(expected)) as ex:
            resolver.resolve(from_string(source))
        self.assertEqual(expected.args[0], str(ex.exception))


    def test_no_template_path(self):
        source = """
        trainer: ${yaml:trainers/discriminator}
        """
        resolver = DefaultResolver()
        expected = errors.template_path_has_to_be_set("trainers/discriminator.yaml", [])
        with self.assertRaises(type(expected)) as ex:
            resolver.resolve(from_string(source))
        self.assertEqual(expected.args[0], str(ex.exception))

    def test_no_template_path_valid_inmemory_templates(self):
        source = """
        trainer: ${yaml:trainers/discriminator}
        """
        resolver = DefaultResolver(**{"some_template.yaml": ""})
        expected = errors.template_path_has_to_be_set("trainers/discriminator.yaml", ["some_template.yaml"])
        with self.assertRaises(type(expected)) as ex:
            resolver.resolve(from_string(source))
        self.assertEqual(expected.args[0], str(ex.exception))

    def test_invalid_template_key(self):
        source = """
        trainer: ${yaml:trainers/discriminator}
        """
        resolver = DefaultResolver(template_path="some_path")
        expected = errors.template_file_doesnt_exist("some_path/trainers/discriminator.yaml")
        with self.assertRaises(type(expected)) as ex:
            resolver.resolve(from_string(source))
        self.assertEqual(expected.args[0], str(ex.exception))

    def test_invalid_resolver_key(self):
        source = """
        trainer: ${asdf:trainers/discriminator}
        """
        resolver = DefaultResolver()
        expected = errors.invalid_resolver_key(
            "asdf",
            list(resolver.scalar_resolvers.keys()),
            simulated_trace("trainer"),
        )
        with self.assertRaises(type(expected)) as ex:
            resolver.resolve(from_string(source))
        self.assertEqual(expected.args[0], str(ex.exception))

    def test_invalid_resolver_key_in_nested(self):
        source = """
        trainer: 
          template: ${yaml:trainers/discriminator}
        """
        discriminator_trainer = """
        some: ${asdf:qwer}
        """
        templates = {"trainers/discriminator.yaml": discriminator_trainer}
        resolver = DefaultResolver(**templates)
        expected = errors.invalid_resolver_key(
            "asdf",
            list(resolver.scalar_resolvers.keys()),
            simulated_trace("some"),
            "trainers/discriminator.yaml",
        )
        with self.assertRaises(type(expected)) as ex:
            resolver.resolve(from_string(source))
        self.assertEqual(expected.args[0], str(ex.exception))

    def test_invalid_eval(self):
        source = """
        trainer: ${eval:asdfasdf}
        """
        resolver = DefaultResolver()
        expected = errors.invalid_evaluate_expression(
            "asdfasdf",
            NameError("name 'asdfasdf' is not defined"),
            simulated_trace("trainer"),
        )
        with self.assertRaises(type(expected)) as ex:
            resolver.resolve(from_string(source))
        self.assertEqual(expected.args[0], str(ex.exception))

    def test_invalid_eval_in_nested(self):
        source = """
        trainer: 
          template: ${yaml:trainers/discriminator}
        """
        discriminator_trainer = """
        some: ${eval:asdfasdf}
        """
        templates = {"trainers/discriminator.yaml": discriminator_trainer}
        resolver = DefaultResolver(**templates)
        expected = errors.invalid_evaluate_expression(
            "asdfasdf",
            NameError("name 'asdfasdf' is not defined"),
            simulated_trace("some"),
            "trainers/discriminator.yaml",
        )
        with self.assertRaises(type(expected)) as ex:
            resolver.resolve(from_string(source))
        self.assertEqual(expected.args[0], str(ex.exception))

    def test_invalid_select_accessor(self):
        source = """
        trainer: ${select:some:asdf}
        """
        resolver = DefaultResolver()
        expected = errors.cant_apply_accessor_to_scalar("some", "asdf")
        with self.assertRaises(type(expected)) as ex:
            resolver.resolve(from_string(source))
        self.assertEqual(expected.args[0], str(ex.exception))

    def test_invalid_select_accessor2(self):
        source = """
        trainer: ${select:some.value:${eval:dict(some=dict(asdf=5))}}
        """
        resolver = DefaultResolver()
        expected = errors.invalid_accessor_error(["some", "value"], simulated_trace("trainer"))
        with self.assertRaises(type(expected)) as ex:
            resolver.resolve(from_string(source))
        self.assertEqual(expected.args[0], str(ex.exception))

    def test_invalid_select_accessor_nested(self):
        source = """
        trainer: 
          template: ${yaml:trainers/discriminator}
        """
        discriminator_trainer = """
        some: ${select:key:${eval:dict(asdf='qwer')}}
        """
        templates = {"trainers/discriminator.yaml": discriminator_trainer}
        resolver = DefaultResolver(**templates)
        expected = errors.invalid_accessor_error(["key"], simulated_trace("some"), "trainers/discriminator.yaml")
        with self.assertRaises(type(expected)) as ex:
            resolver.resolve(from_string(source))
        self.assertEqual(expected.args[0], str(ex.exception))
