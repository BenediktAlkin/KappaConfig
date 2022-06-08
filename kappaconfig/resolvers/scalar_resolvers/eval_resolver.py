from .scalar_resolver import ScalarResolver

class EvalResolver(ScalarResolver):
    def resolve(self, value, **__):
        return eval(value)