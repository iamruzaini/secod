# Polar: security-focused tests

Add tests with provider SDK mocked, emulated, or sandboxed at boundary appropriate to project.

## Required cases

- Expected authenticated and authorized success.
- Missing or invalid identity and credentials.
- Wrong tenant, owner, resource, product, model, or environment.
- Malformed and oversized provider input.
- Duplicate, replay, retry, timeout, and out-of-order behavior where applicable.
- Provider failure without partial privileged effects or secret leakage.
- Logs and returned errors contain no credentials or protected payloads.
- Installed SDK/runtime version compiles and uses only documented APIs.

External dashboard settings are separate deployment steps; tests must not claim those settings were inspected.
