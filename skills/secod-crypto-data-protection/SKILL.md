---
name: secod-crypto-data-protection
description: Use established cryptographic primitives and libraries; minimize protected data and define its complete key, retention, backup, and deletion lifecycle. Triggers include TLS configuration, CSPRNG token/nonce generation, password hashing or KDF selection, encryption of stored data or backups, hardcoded or rotated keys, algorithm deprecation (MD5/SHA-1/ECB/custom crypto), sensitive-data classification, third-party data sharing, analytics/tracking inventory, retention schedules, deletion propagation across databases/providers/caches/backups/search/AI stores; package presence alone is Candidate.
---

# SECOD Crypto Data Protection

## Mission

Prove that the application uses established cryptography correctly and handles protected data
with a complete, verifiable lifecycle: correct primitives and parameters, managed keys, minimal
data collection, defined retention, deletion that actually propagates, and encrypted restorable
backups.

Repository-only review cannot prove deployed TLS posture, managed-service encryption-at-rest,
backup contents or restorability, provider-side deletion outcomes, or real third-party data
handling. `secod-ship-check` owns final launch readiness; this skill never issues it. This is
security and privacy engineering review — never a claim of legal, GDPR, or compliance
certification.

## Scope and ownership

Owned controls: application TLS configuration decisions; CSPRNG use for tokens/nonces/salts;
password KDF selection and parameters; algorithm/mode selection including authenticated
encryption where required; prohibition of custom cryptography; key separation, storage design,
rotation, revocation, recovery, and cryptographic agility with deprecation/migration plans;
sensitive-data classification, purpose inventory, minimization; third-party-sharing inventory;
data-residency and cross-region transfer assumptions recorded as engineering decisions;
analytics/cookie/telemetry/tracking-data inventory; retention schedules and deletion triggers;
deletion propagation and verification across application databases, providers, caches/CDNs,
backups, search indexes, object storage, AI files, embeddings and vector stores; backup
encryption and restore verification.

Excluded controls (owned elsewhere): credential verification flow, session/share-link/token
lifecycle and bearer-verifier storage (`secod-identity-access`; this skill owns KDF parameters
and CSPRNG primitive choice only); secret values in source/bundles/env placement
(`secod-secrets-config`; this skill owns key material lifecycle); request/API boundary injection,
SSRF, webhook signature verification mechanics (`secod-inputs-apis`); upload/download content
(`secod-data-files`); log redaction and audit-event plumbing (`secod-observability-response`);
advisory monitoring of crypto libraries (`secod-vulnerability-management`);
platform-managed TLS termination/certificates (`secod-vercel-platform`, Cloudflare/AWS/GCP
routers); data-class confirmation depth at intake (`secod-threat-model` routes here); launch
verdicts (`secod-ship-check`).

Direct dependencies (from `secod/catalog.json`): `secod-core`.

Conditional routes: `secod-identity-access` (KDF parameter depth beyond selection),
`secod-secrets-config` (key placement), `secod-threat-model` (classification intake),
`secod-observability-response` (deletion/rotation audit events), `secod-vulnerability-management`
(crypto library advisories), platform adapters for managed-service encryption evidence.

## Required inputs

Repository: crypto library usage and versions (node:crypto/WebCrypto/libsodium/bcrypt/argon2/
cryptography/pycryptodome/jose-class), random-value call sites, password-hashing code, cipher
configuration, key constants or derivation code, backup jobs, deletion/analytics/telemetry code,
data models marking sensitive fields, cookie/tracker integration.

Environment/version: runtime versions, framework versions, database/storage engines and their
encryption features, deployment targets per environment.

Commonly unavailable from repository alone (require supplied evidence, else `Not verified`):
effective deployed TLS protocol/cipher posture; managed-database/object-storage/cache
encryption-at-rest state; backup existence, encryption, and restore results; provider-side and
cache/CDN/index deletion outcomes after a deletion event; third-party recipients' actual data
practices; residency of provider regions in active use.

Human-supplied evidence: data-purpose and third-party-sharing registers (recipient, fields,
purpose, sensitivity, region, retention); retention schedule with owners; backup policy and dated
restore-test records; residency decision records; DPA/provider documentation relied upon.

### External evidence intake

Use `scripts/validate_evidence_bundle.py <manifest.json>` and the
[`references/evidence-bundle.md`](references/evidence-bundle.md) contract for deployed TLS posture,
managed-service encryption at rest, provider-side deletion outcomes, backup encryption, and dated
restore tests.
Each artifact must be authorized and redacted, hash-bound to a local file, tied to an environment
and deployment, and current at review time through `captured_at` and `valid_until`.

Required artifact kinds are `deployed_tls_posture` (`SECOD-CDP-01`),
`managed_service_encryption_at_rest` (`SECOD-CDP-04`), `provider_deletion_outcome`
(`SECOD-CDP-08`), and both `backup_encryption_at_rest` and `restore_test_result`
(`SECOD-CDP-09`). A structurally complete bundle makes evidence reviewable; it never grants
`Passed with evidence` without content review, target correlation, and negative-test results.
Missing, stale, contradictory, failed, or incomplete artifacts preserve `Not verified` and name
the exact missing kind. Never substitute repository inference for these artifacts.

## Applicability and discovery

Signal groups:

- Package/SDK: crypto/KDF libraries, TLS middleware, tracker/analytics SDKs, backup tools,
  vector-store or embedding SDKs.
- Environment variables: `*_KEY`, `*ENCRYPTION*`, `*SECRET*` derivation inputs, KMS references,
  retention/deletion job schedules.
- Routes/webhooks: account-deletion endpoints, export features, consent/cookie endpoints,
  admin purge jobs.
- Configuration: cipher/TLS settings, hashing config, backup configs, tracker allowlists,
  cache/index TTLs.
- Deployment/provider evidence: managed-service encryption flags, KMS/keyring usage, region
  selection, backup snapshots.

Classification follows `secod-core`: `Candidate` (package present, example variable name, dormant
file); `Likely` (code/configuration exists but deployed/provider state unverified); `Active`
(repository behavior correlates with deployed/runtime/Dashboard/API/provider evidence). Maintain
separate development/preview/staging/production inventories — keys, retention, tracking, and
residency routinely differ per environment; conflicting or shared environment signals keep
affected controls `Not verified`.

## Review workflow

1. Inventory environments and trust boundaries: every store holding protected data, every key,
   every environment, every third-party recipient. Parallelizable once the inventory exists.
2. Correlate active flows: which flows create, read, transform, replicate, retain, or delete
   protected data; which generate tokens/nonces/hashes; which ship data to trackers.
3. Verify applicable controls below against code plus supplied external evidence.
4. Run safe negative tests: reason through weak-randomness, weak-algorithm, key-reuse,
   incomplete-deletion, and unrestorable-backup cases against traced code/config. No production
   data changes without explicit authorization.
5. Classify evidence, emit findings, route gaps to owning skills, hand off to `secod-ship-check`.

Steps 1–2 are parallelizable across environments only when evidence is independent and no state
changes.

## Control requirements

The catalog approves the nine stable control IDs below. Map each control to OWASP ASVS 5.0.0
sections using version-qualified identifiers (`v5.0.0-11.x`, `v5.0.0-12.x`, `v5.0.0-14.x`)
in `references/sources.md`.

### `SECOD-CDP-01` — TLS and secure communication

**Applicability:** Every outbound/inbound network connection carrying protected data that the
application itself configures. Protects confidentiality/integrity in transit.

**Inspect and verify:** HTTPS enforced for all application-controlled endpoints (no plain-HTTP
listeners serving authenticated traffic); internal service-to-service calls either TLS or on an
explicitly documented trusted-network boundary; certificate validation never disabled
(`rejectUnauthorized: false`, `verify=False`, `InsecureSkipVerify`, disabled verifier options);
TLS version floors set to current guidance via `v5.0.0-12.x`; HSTS and header delivery owned by
`secod-web-app-security`. Platform termination details route to adapters.

**Unsafe evidence:** Disabled certificate validation anywhere in shipped code; HTTP endpoints
carrying credentials/tokens; "localhost only" justification applied to shared networks.

**Required negative test:** A connection to an attacker-controlled endpoint with a self-signed
certificate must fail validation in every traced client path.

**Passing / Not verified:** Pass requires every application-configured connection traced with
validation intact and documented floors. Deployed effective TLS posture needs supplied captures
or adapter evidence else `Not verified`.

**Related skill routing:** Termination/certificates → platform adapters; browser headers →
`secod-web-app-security`.

### `SECOD-CDP-02` — CSPRNG for tokens, nonces, and salts

**Applicability:** Every security-relevant random value: tokens, nonces, IVs, salts, reset codes,
ids used as capabilities. Predictability defeats every downstream control.

**Inspect and verify:** Only cryptographically secure generators used (`crypto.randomBytes`/
`randomUUID`, WebCrypto `getRandomValues`, `secrets` module, `SecureRandom`); no `Math.random`,
time-, counter-, or hash-of-predictable-input-derived values for security purposes; entropy
adequate for value lifetime (128+ bits for unguessable tokens); nonces/IVs unique per key per
SP 800-38D requirements; salt unique per record.

**Unsafe evidence:** `Math.random()` feeding tokens/nonces/salts; fixed or zero IVs; reused salts
across users; short numeric OTPs generated from insecure randomness.

**Required negative test:** Generate two consecutive values from each traced generator path and
show the security-relevant ones come from CSPRNG APIs; predictability probe (seed/time-based) must
not reproduce a token.

**Passing / Not verified:** Pass requires complete call-site trace of security-relevant
randomness to CSPRNG sources. Any unreachable dynamic path stays `Not verified`.

**Related skill routing:** Token lifecycle semantics → `secod-identity-access`.

### `SECOD-CDP-03` — Password and secret-derivation KDFs

**Applicability:** Every password verifier, API-key digest, or low-entropy secret stored or
derived by the application. Selection and parameters only; verification flow is
`secod-identity-access`.

**Inspect and verify:** Memory-hard/modern KDF chosen deliberately (Argon2id preferred, bcrypt/
scrypt/PBKDF2 accepted with current-parameter justification per the Password Storage Cheat Sheet
in `references/sources.md`); per-record unique salt; parameters recorded and revisitable;
verification constant-time via library compare; legacy hashes (MD5/SHA-1/unsalted SHA-2) have an
explicit upgrade-on-login migration path, not silent acceptance; pepper/secret-derived keys come
from managed key material, not source code.

**Unsafe evidence:** Fast hashes (MD5/SHA-1/plain SHA-256) storing passwords; hardcoded global
salt; KDF cost parameters at defaults frozen since install without review; plaintext or
reversible password storage.

**Required negative test:** Login with a legacy-hashed fixture account must trigger rehash to
current parameters (or be explicitly denied), never silently continue on the weak verifier forever.

**Passing / Not verified:** Pass requires algorithm+parameter evidence per storage site and a
migration story for any legacy hash. Runtime parameter enforcement needs supplied evidence else
`Not verified`.

**Related skill routing:** Credential verification/session semantics → `secod-identity-access`;
library advisories → `secod-vulnerability-management`.

### `SECOD-CDP-04` — Algorithm selection, authenticated encryption, no custom cryptography

**Applicability:** Every encrypt/sign/MAC operation in the application and every managed store
holding protected data. Protects against confidentiality loss and undetected tampering.

**Inspect and verify:** Established libraries and standard modes only; custom cipher/MAC/hash
constructions prohibited; AEAD (AES-GCM/ChaCha20-Poly1305 or equivalent) wherever both
confidentiality and integrity are required; CBC without a secure MAC treated as unauthenticated;
GCM/CTR nonce uniqueness enforced by construction per SP 800-38D; ECB prohibited; deprecated
algorithms (DES, RC4, MD5, SHA-1 for signatures) absent or on a dated migration plan; key sizes
per current NIST guidance; associated data bound so ciphertexts cannot be transplanted between
records/purposes. Managed stores must have encryption at rest enabled; record provider, service,
resource, encryption mode, key-management mode, environment, and capture expiry.

**Unsafe evidence:** Hand-rolled XOR/stream constructions; ECB output on structured data;
encrypt-without-MAC claimed as tamper-proof; ciphertext copied between rows without AAD binding.

**Required negative test:** Tampered ciphertext (bit flip or cross-record transplant) must fail
decryption/authentication rather than yield attacker-modified plaintext.

**Passing / Not verified:** Pass requires every cipher invocation inventoried with mode, key size,
and IV strategy justified. Managed-service encryption requires current Dashboard/API evidence;
untested decryption paths and unsupported provider claims stay `Not verified`.

**Related skill routing:** Library advisory status → `secod-vulnerability-management`.

### `SECOD-CDP-05` — Key management lifecycle, agility, and migration

**Applicability:** Every symmetric/asymmetric key, signing key, and key-derivation input the
application controls. Compromise of key management defeats strong algorithms (SP 800-57).

**Inspect and verify:** Keys separated by purpose (encryption ≠ signing ≠ session ≠ backup);
storage via KMS/secret manager/HSM or documented equivalent — never source code, client bundles,
URLs, logs, or repo files; rotation procedure exists with dual-key read/write overlap defined;
revocation possible within one deploy cycle; recovery/escrow defined for keys whose loss destroys
data; cryptographic agility: algorithms identified in an inventory (`v5.0.0-11.1`) with
deprecated/retired entries, owners, and migration plans; versioned ciphertext format enabling
migration; key identifiers stored with ciphertext.

**Unsafe evidence:** One all-purpose key; keys committed to the repository or derivable from
public constants; no rotation path; encrypted data that becomes unrecoverable on single-key loss
without an accepted-risk record; no algorithm inventory.

**Required negative test:** Rotation drill reasoning: after rotating, new writes must use the new
key id and old reads must still succeed during the declared overlap; revoked key must fail
operations.

**Passing / Not verified:** Pass requires key inventory, storage mechanism evidence, and a
documented rotation/recovery procedure. Managed-KMS state needs supplied Dashboard/API evidence
else `Not verified`.

**Related skill routing:** Secret placement hygiene → `secod-secrets-config`; audit events for
rotation → `secod-observability-response`.

### `SECOD-CDP-06` — Data classification, minimization, sharing, residency

**Applicability:** Every field collected, processed, stored, or transmitted that is sensitive,
personal, financial, health-related, or otherwise protected. Collecting less is stronger than any
cipher.

**Inspect and verify:** Sensitive-data classification exists per data model with sensitivity tiers
(`v5.0.0-14.x`); purpose inventory records why each class is collected; minimization enforced:
fields unused by any flow are removed, free-text fields do not become sensitive-data sinks;
third-party-sharing inventory records recipient, fields, purpose, sensitivity, region, and
retention for every outbound share; data-residency and cross-region transfer assumptions written
as engineering decisions with named owner — reviewed here as risk decisions, never as legal
certification.

**Unsafe evidence:** Unmapped sensitive columns; logging/tracing of full protected payloads;
sharing PII with analytics providers outside the register; "we think it's fine" residency with no
recorded decision.

**Required negative test:** Probe one flow per class: request more fields than the purpose
requires and show excess is rejected/dropped, not persisted.

**Passing / Not verified:** Pass requires classification × purpose × recipient coverage with no
unowned classes. Third-party actual behavior beyond the contract stays `Not verified`.

**Related skill routing:** Classification intake → `secod-threat-model`; telemetry redaction →
`secod-observability-response`; client-visible exposure → `secod-web-app-security`.

### `SECOD-CDP-07` — Analytics, cookie, telemetry, and tracking-data inventory

**Applicability:** Every client-side or server-side tracker, analytics SDK, session-recording,
consent, or advertising integration.

**Inspect and verify:** Complete inventory of trackers/SDKs with data categories captured;
identifiers sent to third parties enumerated (user ids, emails leaking into analytics calls
reviewed); cookies inventoried with purpose, scope, duration (`v5.0.0-14.x`); consent-gated
loading verified in code order (gate before load, not after); server-side forwarding of user data
to measurement endpoints listed in the `SECOD-CDP-06` register.

**Unsafe evidence:** Undocumented tag-manager scripts; email/user-id auto-capture into analytics
events; consent banner present but scripts firing before opt-in.

**Required negative test:** With consent withheld, traced loader paths must not execute tracking
network calls.

**Passing / Not verified:** Pass requires inventory reconciled against bundle/network traces
supplied by the user. Live script behavior needs supplied evidence else `Not verified`.

**Related skill routing:** Third-party script supply chain → `secod-web-app-security`; register
ownership → `SECOD-CDP-06` routing.

### `SECOD-CDP-08` — Retention schedules and deletion propagation

**Applicability:** Every store holding protected data: application databases, providers,
caches/CDNs, backups, search indexes, object storage, AI files, embeddings and vector stores.

**Inspect and verify:** Retention schedule defines period + trigger + owner per data class;
deletion paths exist and are reachable for account/data deletion; propagation covers every store
class above — each mapped store has a deletion mechanism (row delete, provider API call, index
purge, cache invalidate, embedding/vector delete, AI-file delete); backups handled by explicit
policy (expiry-bounded retention or documented re-delete on restore) because backup deletion is
usually destructive to recoverability; verification step confirms deletion (post-check query/API
read); orphan detection for partial failures.

**Unsafe evidence:** Deletion endpoint that soft-deletes while replicas/embeddings persist
indefinitely with no reconciliation; no answer to "which caches/indexes still hold this user's
data"; deleted-account content still retrievable from search.

**Required negative test:** Delete a test record through the traced path, then query every mapped
store (or reason through each store's mechanism when live testing is unauthorized) — residual
copies must be bounded by the documented policy, not indefinite.

**Passing / Not verified:** Pass requires store-by-store propagation mapping plus verified
outcome evidence. Provider-side deletion outcomes without supplied confirmation stay
`Not verified`.

**Related skill routing:** Audit events for deletion → `secod-observability-response`;
provider-specific deletion APIs → owning provider adapters.

### `SECOD-CDP-09` — Backup encryption and restore verification

**Applicability:** Every backup/snapshot/export of protected data the application or its managed
services produce.

**Inspect and verify:** Backups encrypted with keys independent from the primary datastore keys
(one compromise must not unlock both); backup storage location/residency recorded; restore
procedure documented AND evidenced by a dated successful restore test — an untested backup is
assumed lost; restore includes re-applying the `SECOD-CDP-08` backup-deletion policy; access to backups
least-privileged.

**Unsafe evidence:** Unencrypted dumps in object storage; backup credentials co-stored with
database credentials; no restore test ever executed; restore runbook referencing deleted tooling.

**Required negative test:** Restore reasoning: restoring the latest snapshot must produce working,
correctly-encrypted data and must carry forward the deletion/retention obligations; a corrupted
backup must be detected by checksum/test rather than silently restored.

**Passing / Not verified:** Pass requires encryption evidence plus a supplied dated restore-test
record. Backup contents/restorability are unverifiable from repository alone — always
`Not verified` without supplied evidence.

**Related skill routing:** Managed-service backup settings → platform/data adapters; incident
restoration procedures → `secod-observability-response`.

## Exceptional and failure conditions

Fail closed on target-reachable failure flows:

- Deletion-job timeout or provider-API failure: mark the item for reconciliation retry with a
  bounded schedule; never report deleted while any mapped store remains; unresolved items surface
  as findings, not silence.
- Partial deletion across stores: durable ledger of completed/pending stores; cancellation or
  crash mid-run must leave the ledger authoritative so the next run resumes instead of skipping.
- Key rotation overlap: old-key reads remain valid only inside the declared overlap window;
  expired-window failures fail closed, never fall back to accepting unknown key versions.
- Encryption/decryption dependency failure (KMS unavailable): operations requiring the key fail
  closed; degraded plaintext fallback prohibited.
- Restore-test failure: withdraw any `Passed with evidence` on `SECOD-CDP-09` until a passing test exists.
- Never invent provider retry schedules or guarantees; rely only on documented provider behavior
  or mark `Not verified`.
- A failed checker or incomplete negative test never counts as success.

## Dependency and routing rules

Direct dependencies (from `secod/catalog.json`): `secod-core`.

Conditional routes: `secod-identity-access` (KDF parameter depth, token semantics),
`secod-secrets-config` (placement), `secod-threat-model` (classification intake),
`secod-observability-response` (audit events, restoration), `secod-vulnerability-management`
(library advisories), platform/data adapters for managed-service encryption, backup, and deletion
evidence.

If `secod-core` or a required routed skill is missing/unresolved/malformed/incomplete: mark
affected controls `Not verified`, name the missing owner/evidence, never invent replacement
dependencies, never issue launch readiness.

## Evidence and status rules

Statuses: `Do not ship`, `Fix before launch`, `Recommended hardening`, `Passed with evidence`,
`Not verified`.

Target-specific thresholds:

- `Passed with evidence`: full inventory per applicable control; every random/cipher/KDF/key site
  traced; classification/minimization/sharing/residency registers complete; deletion propagation
  mapped store-by-store; supplied external evidence matches intent.
- `Fix before launch`: predictable randomness on security values; fast-hash password verifiers
  without migration; custom crypto; disabled certificate validation; unbounded retention of
  deletable personal data; unencrypted backups; deletion that provably leaves permanent copies.
- `Recommended hardening`: suboptimal-but-safe KDF parameters pending tune; missing algorithm
  inventory entries; consent gating load-order improvable; restore test older than policy allows.
- `Not verified`: deployed TLS posture, managed-service encryption/backup state, provider-side
  deletion outcomes, third-party actual behavior, restore results — each with exact evidence
  needed.

Never pass inferred, package-only, inaccessible, stale, contradictory, incomplete, unsupported,
or failed evidence.

## Required output

One finding per applicable control: `control_id`, `title`, `status`, `scope`, `evidence`,
`impact`, `recommended_fix`, `verification`, `limitations`, `source_refs`, `routed_skills`.

End the report with: applicability inventory (data classes × stores × environments; key
inventory; third-party/tracker register); test results; requested external evidence (restore-test
records, provider encryption/deletion confirmations, residency decisions — by owner);
`Not verified` items with next verification step; launch blockers. Route overall launch readiness
to `secod-ship-check`.

## Negative fixtures and tests

Unsafe crypto cases remain documentation-only. Evidence-intake fixtures execute only local,
synthetic bundle validation; they never inspect a provider or claim production proof.

| Fixture | Type | Controls exercised |
| --- | --- | --- |
| `tests/insecure-fixtures/secod-crypto-data-protection/README.md` | Mixed plan/intake test | All controls |
| `Math.random()`-generated password-reset token | Documentation-only case | `SECOD-CDP-02` |
| MD5-hashed passwords, no rehash path | Documentation-only case | `SECOD-CDP-03` |
| AES-ECB on structured records | Documentation-only case | `SECOD-CDP-04` |
| Committed all-purpose encryption key, no rotation | Documentation-only case | `SECOD-CDP-05` |
| PII columns with no classification or purpose entry | Documentation-only case | `SECOD-CDP-06` |
| Analytics SDK firing before consent rejection | Documentation-only case | `SECOD-CDP-07` |
| Account deletion leaving embeddings/search copies indefinitely | Documentation-only case | `SECOD-CDP-08` |
| Missing managed-service, deletion, or restore evidence | Executable intake test | `SECOD-CDP-01`, `SECOD-CDP-04`, `SECOD-CDP-08`, `SECOD-CDP-09` |
| Failure case: deletion job times out mid-propagation, no ledger | Documentation-only case | `SECOD-CDP-08` |

Reasoning-based verification only. Never claim Markdown fixture plans executed as code. Never run
destructive, production-changing, user-creating, payment-creating, refunding, key-rotating,
dashboard-changing, or account-changing tests without explicit authorization.

## References

- [`references/sources.md`](references/sources.md) — source register: OWASP ASVS 5.0.0 (V11/V12/V14), NIST
  SP 800-57 Part 1 Rev. 5, NIST SP 800-38D, OWASP Cryptographic Storage / Key Management /
  Password Storage Cheat Sheets, OWASP Top 10 2025 A10 (fail-closed behavior).
