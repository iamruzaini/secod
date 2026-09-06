# Routed task context

Build one compact context record and pass it unchanged to every selected skill. Omit empty fields;
never insert secret values.

```yaml
feature:
  request: "User-visible behavior being implemented"
  acceptance: "Concrete completion condition"
application:
  kind: "web | api | worker | native-mobile | react-native-expo | flutter"
  root: "repository-relative application root"
stack:
  language: "language and resolved version when known"
  runtime: "runtime and resolved version when known"
  framework: "framework/router and resolved version when known"
  package_manager: "package manager and resolved version when relevant"
providers:
  - name: "provider"
    products: ["products used by this feature"]
    evidence: "Requested | Detected"
trust_boundaries:
  - from: "untrusted caller or component"
    to: "trusted enforcement component"
    data: ["data classes crossing boundary"]
identity:
  authentication: "session/token/workload model"
  authorization: "role/ownership/tenant model"
files:
  inspect: ["repository-relative paths"]
  likely_changes: ["repository-relative paths"]
tests:
  existing: ["relevant test paths"]
  needed: ["positive, negative, abuse, failure cases"]
routing:
  direct: ["directly selected SECOD skills"]
  transitive: ["dependency-selected SECOD skills"]
assumptions: ["narrow reversible assumptions"]
external_actions: ["exact provider/deployment actions not performed locally"]
```

## Rules

- Keep paths repository-relative when possible.
- Record resolved versions and evidence source; do not guess deployed versions.
- Name exact provider products, not only provider families.
- Describe trust boundaries as data/effect crossings, not generic architecture labels.
- Include only files connected to current task.
- Separate direct routing decisions from transitive dependencies.
- Keep inaccessible external settings under `external_actions`; do not turn them into global
  application status.
- Update record when implementation changes architecture or selected provider products.

## Downstream use

Selected skills should inspect this context before rediscovering repository state. They may
inspect additional nearby files required for implementation, but should not expand into unrelated
audits. Reconcile overlapping guidance against same trust boundary and user goal.
