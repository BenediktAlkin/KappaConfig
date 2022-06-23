import unittest

from kappaconfig.functional.load import from_string
from kappaconfig.resolvers.processors.if_post_processor import IfPostProcessor
from kappaconfig.resolvers.resolver import Resolver


class TestIfPostProcessor(unittest.TestCase):
    def _resolve_and_assert(self, source, expected, **kwargs):
        resolver = Resolver(post_processors=[IfPostProcessor(**kwargs)])
        actual = resolver.resolve(from_string(source))
        self.assertEqual(expected, actual)

    def test_dict(self):
        source = """
        node1:
          node2:
            if: False
        """
        expected = None
        self._resolve_and_assert(source, expected)

    def test_dict_allow_empty(self):
        source = """
        node1:
          node2:
            if: False
        """
        expected = dict(node1={})
        self._resolve_and_assert(source, expected, allow_empty_result=True)

    def test_list(self):
        source = """
        - if: False
        """
        expected = None
        self._resolve_and_assert(source, expected)

    def test_list_allow_empty(self):
        source = """
        - if: False
        """
        expected = []
        self._resolve_and_assert(source, expected, allow_empty_result=True)

    def test_list_multiple_entries(self):
        source = """
        - if: False
        - 5
        """
        expected = [5]
        self._resolve_and_assert(source, expected)

    def test_nested_dict(self):
        source = """
        trainer:
          kind: some
          early_stopper:
            if: False
            tolerance: 5
          loggers:
          - kind: progress_logger
          - kind: valid_loss_logger
            if: False
          - kind: test_loss_logger
        """
        expected = dict(trainer=dict(
            kind="some",
            loggers=[
                dict(kind="progress_logger"),
                dict(kind="test_loss_logger"),
            ]
        ))
        self._resolve_and_assert(source, expected)
