# KappaConfig
KappaConfig is a configuration framework that allows you to define a full fletched configuration in yaml. 
Basic yaml and many yaml configuration frameworks are restrictive in how a yaml is processed.
KappaConfig provides a rich extension to parsing yamls into primitive types.


With support for many use-cases out-of-the-box (which you can use, but don't have to):
- reuse defined dict/list/primities via cross reference or templating
- write python expressions in yaml
- use yamls from multiple sources to compose one large yaml during program execution

# Install
Install: `pip install kappaconfig`
Update to latest release: `pip install kappaconfig --upgrade`

# Examples
[This directory](https://github.com/BenediktAlkin/KappaConfig/tree/main/tests_integration/complex_yamls) contains 
various examples on how KappaConfig can be used to create flexible and compact yaml files.
`<file>.yaml` is the compact representation of a yaml that is resolved to `<file>.result.yaml` during runtime and 
subsequently used by the application. `<file>.yaml` abstracts away non-vital fields (for easy configuration design), 
while the resolved file (``<file>.result.yaml``) contains every detail for reproducability.

TODO example

## TODO title
Lots of configurations consist of a small part that varies between different configurations and a large part that stays 
the same or only few variables of it change. 
For example: when running machine learning experiments the core of a dataset configuration (e.g. normalization, splits) 
stays largely the same but things like preprocessing might change between different experiments.

```
cifar10:
  train:
    split: train # use train split
    normalization: range # normalize to range [-1;1]
    filter: # use 45.000 samples for training
      index_from: 0
      index_to: 45000
  valid:
    split: train  # use train split (most datasets don't have a dedicated validation split)
    normalization: range
    filter: # use remaining 5.000 samples for validation
      index_from: 45000
      index_to: 50000
  test:
    split: test # use test split
    normalization: range
```
TODO continue example


# Usage
```
import kappaconfig as kc

# load yaml from file
kc_hp = kc.from_file_uri("hyperparams.yaml")
# initialize default resolver
resolver = kc.DefaultResolver()
# resolve to primitive types
hp = resolver.resolve(hp)
```

# Examples
## Reference existing nodes
Inspired by [OmegaConf](https://github.com/omry/omegaconf)/[Hydra](https://github.com/facebookresearch/hydra)
nodes can reference other nodes.
```
# input
batch_size: 64
train_loader:
  batch_size: ${batch_size}
test_loader:
  batch_size: ${batch_size}
---
# resolved
batch_size: 64
train_loader:
  batch_size: 64
test_loader:
  batch_size: 64
```

## Write python code in yaml
```
# input 
seeds: ${eval:list(range(5))}
---
# resolved
seeds: [0, 1, 2, 3, 4] 
```

## Parameterize templates
```
# warmup_cosine_schedule.yaml
vars: # vars is a special node that is removed after resolving a template
  # default values
  epochs: 100
  warmup_factor: 0.05
kind: sequential_schedule
sub_schedules:
- kind: warmup_schedule
  epochs: ${eval:${vars.epochs}*${vars.warmup_factor}}
- kind: cosine_schedule
  epochs: ${eval:${vars.epochs}*${eval:1-${vars.warmup_factor}}}
---
# template_default_params.yaml
optimizer:
  kind: SGD
  schedule:
    template: ${yaml:warmup_cosine_schedule.yaml}
---
# template_default_params.yaml resolved
optimizer:
  kind: SGD
  schedule:
    kind: sequential_schedule
    sub_schedules:
    - kind: warmup_schedule
      epochs: 5
    - kind: cosine_schedule
      epochs: 95
---
# template_custom_params.yaml
optimizer:
  kind: SGD
  schedule:
    template: ${yaml:warmup_cosine_schedule.yaml}
    template.vars.epochs: 200
---
# template_custom_params.yaml resolved
optimizer:
  kind: SGD
  schedule:
    kind: sequential_schedule
    sub_schedules:
    - kind: warmup_schedule
      epochs: 10
    - kind: cosine_schedule
      epochs: 190
---
```
