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

