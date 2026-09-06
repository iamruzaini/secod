# Security-focused tests

Test valid behavior, unauthenticated/unauthorized or cross-tenant denial when applicable, malformed and boundary input, duplicate/concurrent/retried execution, dependency failure, and sensitive error/log redaction.

## Test discipline

- Exercise successful and rejected paths.
- Assert protected effects and state, not only response text.
- Keep fixtures deterministic and isolated.
- Use provider adapters for exact SDK, emulator, sandbox, or deployment behavior.
- Never treat a documentation-only plan as executed test evidence.

## Outage drill

In an authorized non-production environment, inject timeout, connection refusal, and provider
errors separately. Confirm authorization fails closed, mutations roll back or reconcile, retries
remain bounded, cancellation stops child work, and recovery sends only bounded trial traffic.
Abort on real-user impact, uncontrolled cost, irreversible mutation, or lost observability.
