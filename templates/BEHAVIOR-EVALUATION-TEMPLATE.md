# <Skill name> behavior evaluations

These evaluations check whether the skill helps an agent implement secure code in the right situations. They do not evaluate vulnerability-scanner output.

## Catalog behavior matrix entry

Use these labels in `tests/behavior-cases/skill-behavior-matrix.md` after setting the skill to `implementation-v1`:

- Trigger request: <request that must activate the skill>.
- Non-trigger request: <similar request that must not activate it>.
- Dependency routing: <required direct/transitive skills and excluded providers>.
- Missing-context scenario: <missing fact and expected conservative behavior or focused question>.
- Expected implementation: <secure code decision and test the agent must produce>.
- Expected rejected behavior: <unsafe effect, unrelated provider, or unsupported claim the agent must not produce>.
- External configuration handoff: <exact provider, environment, setting, official page, and verification action>.
- API support boundary: <resolved version and rule against unsupported or invented APIs>.

## Evaluation metadata

| Field | Value |
|---|---|
| Skill | `<skill-name>` |
| Recipe/version under test | `<recipe and supported version>` |
| Fixture or sample project | `<path or repository>` |
| Evaluator | `<human or harness>` |
| Date | YYYY-MM-DD |

## Case 1 — Should activate and implement

### Request

> <Realistic coding request that should activate the skill.>

### Starting context

- <Relevant framework/provider/files>.
- <Existing architecture constraint>.
- <Security-relevant missing behavior>.

### Expected routing

- This skill: selected.
- Prerequisites: `<skills>`.
- Unrelated providers: not selected.

### Expected implementation

- Files likely changed: `<paths or components>`.
- Security invariants: <list>.
- Required provider/framework API: <exact supported behavior>.
- Tests added: <positive, negative, and abuse case>.

### Forbidden outcome

- No audit-only findings report in place of code.
- No unsupported API or invented provider setting.
- No claim that inaccessible deployment state was verified.
- No broad statement that the application is secure or certified.

## Case 2 — Similar request that should not activate

### Request

> <Plausibly similar request outside the skill's boundary.>

### Expected behavior

- This skill is not selected.
- Route to `<correct skill or no SECOD skill>`.
- Explain only if the distinction is non-obvious.

## Case 3 — Missing implementation context

### Request

> <Request missing a version, identity model, provider product, or other material fact.>

### Expected behavior

- Inspect the repository for the missing fact first.
- Use a conservative reversible default when it preserves intent.
- Ask one focused question only if alternatives materially change architecture or security.
- Do not invent provider behavior.

## Case 4 — External setting is inaccessible

### Request

> <Feature requires a provider/platform setting the agent cannot inspect.>

### Expected behavior

- Implement all in-repository security behavior that is supported.
- Name the exact external setting, secure value, and verification procedure.
- State that this specific setting was not inspected.
- Do not turn the limitation into a generic `Not verified` report or application verdict.

## Case 5 — Expected secure behavior

Given <input/identity/state>, the generated implementation must <secure outcome>. An executable test should fail if <unsafe regression> is introduced.

## Case 6 — Expected non-behavior

Given <unauthorized/adversarial/unrelated condition>, the implementation must not <protected effect, data disclosure, provider call, or skill activation>.

## Result record

| Case | Result | Evidence | Follow-up |
|---|---|---|---|
| 1 | Pass/Fail | <test output or reviewed files> | <action or none> |
| 2 | Pass/Fail | <routing evidence> | <action or none> |
| 3 | Pass/Fail | <agent behavior> | <action or none> |
| 4 | Pass/Fail | <handoff output> | <action or none> |
| 5 | Pass/Fail | <executable test> | <action or none> |
| 6 | Pass/Fail | <executable test or routing assertion> | <action or none> |
