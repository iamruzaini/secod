# SECOD

Security coding skills for AI builders.

SECOD is a repository foundation for a 57-skill, evidence-based security
library. It is deliberately not presented as a release-ready security product:
the official provider references, deterministic checks, behavior tests,
insecure fixtures, and release evidence are still to be completed.

Current status: beta/prerelease.

SECOD is licensed under the Apache License 2.0. See `LICENSE` for the full
terms.

## Repository roles

- skills holds the portable Agent Skills directories and is the product source
  of truth.
- docs contains the PRD analysis and the initial Skill Contract Matrix.
- tests contains the required validation surfaces for trigger, behavior,
  insecure-fixture, and expected-result coverage.
- scripts contains repository-level, read-only validation utilities.
- .codex-plugin and .claude-plugin contain distribution metadata scaffolds.

## Trust boundary

Never mark a control as passed without technical evidence. Missing
configuration, inaccessible provider settings, and absent tests are Not
verified.

## Before a public v1.0.0 release

1. Resolve the GitHub owner, domain, hosting, and sponsor decisions.
2. Complete every skill contract with current official sources.
3. Build and test realistic insecure fixtures for every skill and provider.
4. Complete the supported-agent installation and plugin marketplace metadata.
5. Pass all release gates in the PRD.
