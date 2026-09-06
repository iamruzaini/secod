# Expected result: secod-container-runtime

Use minimal immutable images, non-root identity, dropped privileges, protected build secrets, health checks, and runtime tests.

Missing context: Base image, runtime, orchestrator, or writable-path need is unclear; inspect before choosing directives.

Rejected behavior: Never default to root, privileged mode, broad mounts, or mutable production identity.
