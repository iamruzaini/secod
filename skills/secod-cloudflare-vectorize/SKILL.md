---
name: secod-cloudflare-vectorize
description: Satisfy secod-cloudflare-workers, secod-ai-api-integrations, secod-data-files and secod-observability-response. Apply when Vectorize indexes/bindings, embeddings, vector…
---

# SECOD Cloudflare Vectorize

## Scope and applicability

Satisfy `secod-cloudflare-workers`, `secod-ai-api-integrations`, `secod-data-files` and `secod-
observability-response`. Apply when Vectorize indexes/bindings, embeddings, vector
query/upsert/delete, namespaces, metadata indexes or Vectorize-backed RAG are detected.
Similarity search is not authorization; every retrieval remains tenant scoped.

## Control requirements

Exact index/binding/environment, embedding model/dimension, source document/R2/D1 data path,
namespace, tenant/owner metadata field/index, upsert/delete/query code, returned
values/metadata/topK, retention/deletion/reindex, Worker/Pages binding and production/preview
inventory; indexes and bindings are separated by environment and sensitive tenant where
architecture requires it, clients cannot choose arbitrary index, namespace, metadata filter,
embedding model or topK, and server code always applies a tenant/owner namespace plus metadata
filter before query, with the needed metadata index created before relevant vectors are inserted
or re-upserted after index creation; source-document authorization/filtering occurs before
embedding, vector IDs/metadata contain no secrets/unnecessary private data, query responses
return the minimum values/metadata and are re-authorized before display or model context, and
retrieved text/model output remains untrusted under `secod-ai-api-integrations`;
ingestion/update/delete is authenticated, tenant-bound and idempotent, Vectorize's asynchronous
delete is tracked to completion, source/R2/D1/cache/vector deletion and retention are
reconciled, and stale vectors/metadata indexes cannot preserve revoked tenant data;
query/input/topK/returned payload, embedding, ingestion, retries and cost are bounded, safe logs
omit raw private corpus/query/result where not required, and model/index/version migration and
re-embedding are reviewed; negative tests for missing/wrong namespace or metadata filter,
client-selected/cross-tenant index/query, vector/source deletion lag, metadata/value over-
return, untrusted retrieved-content prompt injection, embedding/cost abuse and production-
preview index/binding/data drift.

## Evidence to inspect

- Repository code, configuration, tests, deployment definitions, and CI evidence relevant to this skill.
- Provider or framework dashboard/API evidence when the required setting cannot be established from the repository.
- Direct primary-source evidence recorded in `references/sources.md`; absent, stale, or inaccessible evidence is **Not verified**.

## Dependencies and routing

Direct dependencies: `secod-core`, `secod-cloudflare-workers`, `secod-ai-api-integrations`, `secod-data-files`, `secod-observability-response`.

When a required dependency is not installed or cannot be invoked, record the affected
control as **Not verified** and do not issue a passing or launch-ready conclusion.

## Negative fixtures and tests

- Run the maintained trigger case and insecure fixture plan at `tests/` for this skill.
- Test the unsafe or missing-control cases implied by the control requirements, including
  unavailable-provider and partial-failure behavior where applicable.
- Keep tests read-only unless the user explicitly authorizes a change.

## Output schema

For each finding return: `control_id`, `status`, `evidence`, `impact`, `recommended_fix`,
`verification`, `limitations`, and `source_refs`. Valid status values are `Do not ship`,
`Fix before launch`, `Recommended hardening`, `Passed with evidence`, and `Not verified`.

## Verification and safe failure

Never infer dashboard, deployment, provider, or production settings from package presence.
Redact secrets and bearer credentials. Fail closed: preserve unknown or failed checks as
**Not verified**, identify the next verification step, and never claim launch readiness from
incomplete evidence.

## References

Use the source register in `references/sources.md`. For each security-critical source,
record the direct URL, documentation index URL, version, reviewed date, review expiry,
hash/ETag when available, owner, plan/tier, region, feature maturity, and linked control IDs.
