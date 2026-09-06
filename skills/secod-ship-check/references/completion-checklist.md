# Secure implementation completion checklist

## Current feature

- Restate requested feature and current task boundary.
- List files changed during current task.
- Use already-selected skills; do not initiate unrelated routing or repository review.

## Implementation

- Check only invariants required by selected skills for changed feature.
- Fix in-scope defects before handoff when user requested implementation.

## Secrets

- Search changed code, configuration, fixtures, generated artifacts, and logs.
- Flag credential-like literals, tokens, private keys, connection strings, and privileged client variables.
- Never print full secret value; identify file and remediation category.

## Tests

- Run relevant positive and rejected-path tests.
- Record exact commands and results.
- State documentation-only or skipped tests accurately.
- Add missing tests when task authorizes code changes.

## External handoff

For each external action, name provider, project/account, environment, setting, direct official URL,
and exact verification step. Do not claim dashboard or production state was inspected without access.

## Output

Summarize changed feature, selected-skill invariants, secret check, tests run, and remaining external
actions. Do not assess unrelated repository conditions, decide shipping, or certify application security.
