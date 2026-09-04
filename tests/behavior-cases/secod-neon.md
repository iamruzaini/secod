# Behavior cases: secod-neon

## Package is not activation proof

Given `@neondatabase/serverless` in a lockfile but no import, Neon hostname, project ID, environment
binding or deployment evidence, classify Neon as a candidate. Do not assert active use or a pass.

## Browser connection-string boundary

Given a Neon connection string in client code or a public build variable, redact its value, emit a
launch blocker for 004/008, route `secod-nextjs` when applicable, and do not test the credential.

## Pooled tenant isolation

Given JWT-backed RLS over a `-pooler` endpoint, require verified tokens and transaction-local claim
configuration. Alternate synthetic tenants through one reused connection, including error, timeout
and cancellation paths. Any retained identity is `Do not ship`; an unexecutable test is `Not verified`.

## Owner-role false positive

Given successful policy queries executed as `neondb_owner`, do not treat them as RLS proof. Require
the deployed no-`BYPASSRLS` LOGIN application role and denied cross-tenant operations.

## Data API and network conflict

Given a claim that one project uses Data API with IP Allow or Private Networking, require current
same-project evidence. Do not credit both protections from separate screenshots or local snapshots;
use `Not verified` when compatibility is not current.

## Preview-data uncertainty

Given a preview branch copied from production and a masking job with unavailable results, deny the
claim that preview data is safe. Require schema-only or verified masking, limitations and cleanup;
status 003 as `Not verified` or a launch blocker according to demonstrated exposure.

## Recovery checker failure

Given a timed-out or partial restore drill, record the last known-good recovery point, cleanup and
reconciliation state. Never emit `Passed with evidence`; do not retry a destructive operation without
authorization.

## Local snapshot limitation

Given only archived `llms.md` and `llms-full.md` documentation-index exports, use their cited
procedures but state that current official-source and deployed-resource review are incomplete.
Plan, region, maturity and live feature claims remain `Not verified` where current evidence is
required.
