# Test surfaces

The PRD requires a reviewed test case in each category before a skill is
release-ready:

- trigger-cases: direct and indirect prompts that should or should not trigger
  a skill.
- behavior-cases: expected procedural behavior on clean fixtures.
- insecure-fixtures: intentionally unsafe applications and provider
  configurations.
- expected-results: reviewed findings, statuses, evidence, and limitations.

The directories exist as a structural foundation only. Empty coverage is not a
passing release gate.
