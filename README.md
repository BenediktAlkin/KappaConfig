# KappaConfig

KappaConfig is a configuration framework that allows you to define a full fletched configuration in yaml. 
Basic yaml and many yaml configuration frameworks are restrictive in how a yaml is processed.
KappaConfig provides a rich extension to parsing yamls into primitive types.


With support for many use-cases out-of-the-box (which you can use, but don't have to):
- reuse defined dict/list/primities via cross reference or templating
- write python expressions in yaml
- use yamls from multiple sources to compose one large yaml during program execution
