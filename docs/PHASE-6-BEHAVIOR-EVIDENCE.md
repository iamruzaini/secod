# Phase 6 behavior evidence

Test date: 2026-09-05

Phase 6 validates the repository's behavior contracts and deterministic
negative fixtures. It does not claim that an LLM or agent host executed all 60
skills against a production application.

## Gates executed

| Gate | Result |
| --- | --- |
| 60-skill implementation behavior matrix | PASS: 60/60 sections validated across eight behaviors |
| Dependency routing | PASS: 15 representative stack scenarios; 60 catalog nodes; unknown edges and cycles rejected |
| Honesty boundaries | PASS: external settings, unexecuted tests, unsupported APIs, and certification claims are bounded |
| Existing skill-owned executable suites | PASS: 7 suites; 84 tests total |
| Cross-skill critical behavior suite | PASS: 14/14 tests |
| Production or agent-host behavior proof | NOT RUN: requires a real application and supported agent execution harness |

## Critical behavior coverage

| Test ID | Insecure behavior |
| --- | --- |
| `test_01_broken_tenant_authorization` | Tenant/object authorization can return another tenant's record |
| `test_02_missing_server_side_authorization` | Server trusts a client-supplied authorization flag |
| `test_03_exposed_secret` | Privileged provider secret is included in a client payload |
| `test_04_weak_webhook_verification` | Webhook verification accepts a valid signature without freshness/deduplication |
| `test_05_payment_replay` | The same payment event is applied more than once |
| `test_06_unrestricted_file_upload` | Upload accepts disallowed type or oversized content |
| `test_07_public_storage_object` | Private object is readable through public storage visibility |
| `test_08_command_injection` | User input is concatenated into a shell command |
| `test_09_ssrf` | Outbound fetch accepts private or non-HTTP destinations |
| `test_10_missing_rate_limits` | Endpoint has no request bound |
| `test_11_retry_storm` | Retry policy repeats without a bounded attempt count |
| `test_12_sensitive_log_entry` | Logs retain a bearer token or sensitive value |
| `test_13_unsafe_ai_tool_execution` | Model-selected tool executes without an allowlist |
| `test_14_cross_tenant_vector_search` | Retrieval returns vectors outside the request tenant |

The critical runner reports `expectations_reproduced: true` only when both
unsafe and guarded implementation expectations pass. Fixture execution does
not inspect production or certify application security.

## Reproduction commands

```powershell
python scripts/validate_behavior_cases.py
python scripts/test_dependency_routing.py
python scripts/validate_evidence_boundaries.py
python tests/insecure-fixtures/secod-critical-behaviors/run_fixtures.py
```

The 14 skill-owned suite commands and separate critical-behavior command run in
CI. These local fixtures are evidence that expected test logic works; they are
not security certification, deployment verification, or proof that a referenced
provider dashboard was inspected.
