from .scalar_resolver import ScalarResolver

class EvalResolver(ScalarResolver):
    def resolve(self, value, *_, **__):
        return eval(value)