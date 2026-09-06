# Expected result: secod-core

`secod-core` identifies current feature, relevant application root, stack and resolved versions,
provider products, trust boundaries, sensitive data, likely changed files, and existing tests.

It selects only applicable generalized/framework/provider/mobile skills, computes complete
transitive dependency closure, excludes unused providers, and passes same compact task context to
each selected skill.

Selected skills then guide secure code and tests. Core returns feature context, selected skills,
and dependency closure without expanding into unrelated review work or certifying application security.
