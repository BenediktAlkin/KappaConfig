import unittest

from kappaconfig.resolvers.default_resolver import DefaultResolver
import kappaconfig.errors as errors
from kappaconfig.functional.load import from_string

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
        expected = errors.invalid_accessor_error("vars", "trainer.loggers.train_loss_logger.every_n_epochs")
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
        expected = errors.invalid_accessor_error("vars.category", "train.category", "datasets.yaml")
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
        expected = errors.invalid_accessor_error("vars", "progress_logger.every_n_epochs", "loggers/default.yaml")
        with self.assertRaises(type(expected)) as ex:
            resolver.resolve(from_string(source))
        self.assertEqual(expected.args[0], str(ex.exception))

