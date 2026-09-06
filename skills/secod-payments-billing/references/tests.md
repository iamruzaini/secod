# Security-focused tests

Test valid behavior, unauthenticated/unauthorized or cross-tenant denial when applicable, malformed and boundary input, duplicate/concurrent/retried execution, dependency failure, and sensitive error/log redaction.

## Test discipline

- Exercise successful and rejected paths.
- Assert protected effects and state, not only response text.
- Keep fixtures deterministic and isolated.
- Use provider adapters for exact SDK, emulator, sandbox, or deployment behavior.
- Never treat a documentation-only plan as executed test evidence.
