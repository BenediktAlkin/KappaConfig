import unittest

from kappaconfig.functional.load import from_string
from kappaconfig.resolvers.resolver import Resolver
from kappaconfig.resolvers.scalar_resolvers.eval_resolver import EvalResolver
from kappaconfig.resolvers.scalar_resolvers.interpolation_resolver import InterpolationResolver


class TestEvalResolver(unittest.TestCase):
    def _resolve_and_assert(self, input_, expected):
        resolver = Resolver(
            default_scalar_resolver=InterpolationResolver(),
            scalar_resolvers=dict(
                eval=EvalResolver()
            ),
        )
        actual = resolver.resolve(from_string(input_))
        self.assertEqual(expected, actual)

    def test_simple(self):
        input_ = """
        somekey: ${eval:5+6}
        """
        expected = dict(
            somekey=11,
        )
        self._resolve_and_assert(input_, expected)

    def test_nested(self):
        input_ = """
        some_obj: 
          some_key: 5
        other_key: ${eval:list(range(${some_obj.some_key}))}
        """
        expected = dict(
            some_obj=dict(
                some_key=5,
            ),
            other_key=list(range(5)),
        )
        self._resolve_and_assert(input_, expected)

    def test_nested2(self):
        src = """
        vars:
          n_test_rotations: 2
        transforms: ${eval:list(dict(kind='fixed_rotation', angle=360/${vars.n_test_rotations}*i) for i in range(${vars.n_test_rotations}))}
        """
        expected = dict(
            vars=dict(n_test_rotations=2),
            transforms=[
                dict(kind="fixed_rotation", angle=0),
                dict(kind="fixed_rotation", angle=180),
            ],
        )
        self._resolve_and_assert(src, expected)
