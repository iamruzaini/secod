# Narrow honesty behavior cases

SECOD helps agents implement secure code. These boundaries prevent invented claims without turning
ordinary coding work into an audit.

| Case | Input condition | Required behavior | Prohibited behavior |
|---|---|---|---|
| Inaccessible external setting | Provider dashboard or API setting cannot be accessed | Implement repository-owned work and give exact external configuration handoff | Claim setting was inspected or block unrelated implementation |
| Documentation-only test | Test plan exists but no executable command ran | State test was not executed and provide command or implementation needed | Claim test executed |
| Unsupported provider API | Installed version or direct documentation does not support proposed API | Resolve version and choose documented API, or ask narrowly for missing version context | Invent API, option, capability, or dashboard behavior |
| Application security claim | Feature implementation and tests pass | Report bounded implementation and test result | Certify application as secure or issue launch readiness |

Unknown context should trigger repository inspection or a narrow question. It should not
automatically produce a status label, severity, finding table, or refusal to implement unrelated
repository-owned work.
