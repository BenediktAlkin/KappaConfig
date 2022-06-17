from .scalar_resolver import ScalarResolver

class EvalResolver(ScalarResolver):
    def resolve(self, value, root_node, trace, **__):
        try:
            return eval(value)
        except Exception as e:
            from ...errors import invalid_evaluate_expression
            from ...functional.util import trace_to_full_accessor
            raise invalid_evaluate_expression(value, e, trace_to_full_accessor(trace), root_node.source_id)