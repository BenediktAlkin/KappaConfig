```
vars:
  normalization: range
  datasets: ${yaml:data/cifar}

datasets:
  valid:
    template: ${vars.datasets.valid}
  test:
    template: ${vars.datasets.test}
```

```
vars:
  model_key: debug

template: ${select:${vars.model_key}:${yaml:models/vit_solo}}
---
template: ${yaml:models/vit}
debug.attention_heads: 16
```

```
vars:
  encoder_params: ${select:${vars.pretrain_model_key}:${yaml:models/vit}}
  decoder_params: ${select:${vars.pretrain_model_key}:${yaml:models/mae_decoder}}
  model:
    patch_size: ${vars.encoder_params.patch_size}
stages:
  stage0:
    model:
      template: ${vars.model}
```

````
datasets:
  valid:
    template: ${vars.datasets.valid}
    dataset_kwargs:
      normalization: ${vars.dataset_norm}
  test:
    template: ${vars.datasets.test}
    dataset_kwargs:
      normalization: ${vars.dataset_norm}
```
-
- resolver for use-case of using a loaded yaml within an interpolation as template
  e.g. `model_params: ${select:${vars.model_key}:${yaml:models/mae_32}}` -->
  `model_params: ${select:${vars.model_key}:${template:vars.patch_size=[32,8]:${yaml:models/mae_32}}}}`

- ${select:<invalid_key>:${yaml:models/mae_224}} error message is still bad
- KCDict.pop with default return
- navigate to parent with . in interpolation (e.g. ${eval:${vars.total_epochs}-${..[0].max_epoch}})
- resolve should maybe warn if primitive type is encountered and automatically pack it
- warning if templates.vars.something doesn't contain vars
- better error messages