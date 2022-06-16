import unittest

from kappaconfig.functional.load import from_string
from kappaconfig.resolvers.scalar_resolvers.interpolation_resolver import InterpolationResolver
from kappaconfig.resolvers.resolver import Resolver

class TestInterpolationResolver(unittest.TestCase):
    def _resolve_and_assert(self, input_, expected):
        resolver = Resolver(default_scalar_resolver=InterpolationResolver())
        actual = resolver.resolve(from_string(input_))
        self.assertEqual(expected, actual)

    def test_simple_interpolation(self):
        input_ = """
        somekey: 5
        other_key: ${somekey}
        """
        expected = dict(
            somekey=5,
            other_key=5,
        )
        self._resolve_and_assert(input_, expected)

    def test_nested_interpolation(self):
        input_ = """
        some_obj:
          some_key: other_obj.key
        other_obj:
          key: 5
        other_key: ${${some_obj.some_key}}
        """
        expected = dict(
            some_obj=dict(
                some_key="other_obj.key",
            ),
            other_obj=dict(
                key=5,
            ),
            other_key=5
        )
        self._resolve_and_assert(input_, expected)

    def test_dict_interpolation(self):
        input_ = """
        schedule:
          epochs: 5
        model:
          schedule: ${schedule}
        """
        expected = dict(
            schedule=dict(epochs=5),
            model=dict(schedule=dict(epochs=5)),
        )
        self._resolve_and_assert(input_, expected)

    def test_dict_interpolation2(self):
        input_ = """
        schedule_temp:
          epochs: 5
        schedule: ${schedule_temp}
        model:
          schedule:
            epochs: ${schedule.epochs}
        """
        expected = dict(
            schedule_temp=dict(epochs=5),
            schedule=dict(epochs=5),
            model=dict(schedule=dict(epochs=5)),
        )
        self._resolve_and_assert(input_, expected)

    def test_dict_interpolation3(self):
        input_ = """
        schedule_temp:
          epochs: 5
        schedule: ${schedule_temp}
        model:
          schedule: ${schedule}
        """
        expected = dict(
            schedule_temp=dict(epochs=5),
            schedule=dict(epochs=5),
            model=dict(schedule=dict(epochs=5)),
        )
        self._resolve_and_assert(input_, expected)

    def test_dict_interpolation4(self):
        input_ = """
        model:
          schedule: ${schedule}
        schedule: ${schedule_temp}
        schedule_temp:
          epochs: 5
        """
        expected = dict(
            schedule_temp=dict(epochs=5),
            schedule=dict(epochs=5),
            model=dict(schedule=dict(epochs=5)),
        )
        self._resolve_and_assert(input_, expected)
