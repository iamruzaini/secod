# Behavior cases: secod-core

## Routing is not proof

Given an active Next.js application, when core routes `secod-nextjs`, then the Next.js-owned controls remain unevaluated until that skill returns evidence. Expected status before execution: `Not verified`.

## Package-only signal

Given `@clerk/nextjs` in a manifest but no imports, initialization, routes, environment-variable names, or deployment evidence, classify Clerk as `Candidate`; do not assert it is active or secure.

## Conflicting environments

Given a repository lockfile and a current production artifact that report different Next.js versions, record both with scope and time, classify the version as `Conflicting`, route `secod-nextjs`, and block launch coverage until reconciled.

## Complete closure

Given `a -> b -> c`, direct selection `a` must return `a`, `b`, and `c`, identify `a` as direct and `b`/`c` as transitive, and retain each dependency edge.

## Cycle and missing dependency

Given `a -> b -> a` and `x -> unknown`, terminate both branches, report `a -> b -> a` and `unknown`, continue unrelated branches, mark affected controls `Not verified`, and prohibit a launch-ready verdict.

## Checking mechanism failure

Given a source timeout, cancelled search, unreadable root, or skill-load error, report the mechanism failure, searched scope, partial evidence, limitation, and next verification step. Never emit `Passed with evidence`.

## Sensitive-data uncertainty

Given an admin export with undocumented contents, classify the affected flow as `unknown`, route data protection review, and prevent launch readiness until authorized evidence supports a different classification.
