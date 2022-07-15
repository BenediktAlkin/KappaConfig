from .from_dotlist_resolver import FromDotlistResolver
from ...functional.merge import merge
from ...grammar.scalar_grammar import parse_resolver_args_and_value


class MergeWithDotlistResolver(FromDotlistResolver):
    """
    allows parsing from a dotlist within a scalar and merging it into another dict
    NOTE: dotlist is not allowed to contain strings with colons
    e.g. model: ${merge_with_dotlist:patch_size=3:${yaml:models/vit/base}}
    this is useful for using it directly inside a template parameter:
    e.g.
    model:
      template: ${yaml:models/autoencoder_ctor}
      template.vars.model_params: ${merge_with_dotlist:kernel_size=3:${yaml:models/autoencoder_small}}
    """

    def resolve(self, args_and_value, trace, **_):
        args, base = parse_resolver_args_and_value(args_and_value, n_args=1)
        dotlist_str = args[0]
        dotlist_dict = super().resolve(dotlist_str, trace=trace, **_)
        return merge(base, dotlist_dict)
