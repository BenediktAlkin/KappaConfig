# TODO this errorcase is not resolved yet/doesn't have a good error message
# TODO this is an error because merge (specifically _merge_dict_fn) always parses the accessors from 'to_merge'
# TODO if one would swap base and to_merge, it would pass without problems
# TODO maybe a flag like 'parse_accessors' should be passed to merge
# from kappaconfig.functional.load import from_string
# from kappaconfig.functional.util import merge
# import unittest
#
#
# class TestMerge(unittest.TestCase):
#     def test_try_to_merge_unresolved_template(self):
#         base = """
#         model:
#           feature_kwargs:
#             kind: max_all
#         """
#         to_merge = """
#         model:
#           template: ${yaml:models/mae_ctor}
#           template.vars.model_params: 5
#         """
#         base_kc = from_string(base)
#         to_merge_kc = from_string(to_merge)
#         # this should fail as the template was not resolved and therefore
#         # template.vars is invalid as template is a string (${yaml:some_template} is not resolved)
#         result = merge(base_kc, to_merge_kc)
#         print("fin")
