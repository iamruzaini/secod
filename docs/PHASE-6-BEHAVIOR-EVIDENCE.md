# Phase 6 behavior evidence

Test date: 2026-09-05

Phase 6 validates the repository's behavior contracts and deterministic
negative fixtures. It does not claim that an LLM or agent host executed all 57
skills against a production application.

## Gates executed

| Gate | Result |
| --- | --- |
| 57-skill trigger/non-trigger/missing-evidence/finding matrix | PASS: 57/57 sections validated |
| Dependency routing | PASS: 9 representative stack scenarios; 57 catalog nodes; unknown edges and cycles rejected |
| Evidence boundaries | PASS: all 57 skill contracts retain `Not verified` and launch-readiness boundaries |
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

The critical runner reports `expectations_reproduced: true` only when both the
unsafe and guarded fixture expectations pass. It deliberately reports
`production_evidence: false` and `readiness_verdict: not_issued`.

## Reproduction commands

```powershell
python scripts/validate_behavior_cases.py
python scripts/test_dependency_routing.py
python scripts/validate_evidence_boundaries.py
python tests/insecure-fixtures/secod-critical-behaviors/run_fixtures.py
```

The complete seven-suite command list remains in the release-test evidence and
CI workflow. These local fixtures are evidence that the expected test logic
works; they are not security certification, deployment verification, or proof
that a referenced provider dashboard was inspected.
