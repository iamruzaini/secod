---
name: secod-data-files
description: Authorize every upload, download, storage object, share link and export; validate actual file content and bound storage and processing. Triggers include multipart/route upload handlers, direct-to-storage presigned flows, storage SDKs (S3, GCS, R2, Supabase Storage, Firebase Storage, Convex file storage, Vercel Blob), share-link routes, image/PDF/archive processing libraries, antivirus/CDR integration, export and browser-rendering jobs; package presence alone is Candidate.
---

# SECOD Data Files

## Mission

Prove that every byte a user can push into or pull out of the application is authorized,
validated as actual content, bounded in size and processing cost, and served without granting
capability beyond its owner's intent: uploads cannot become code execution or cross-tenant
reads, downloads and share links cannot outlive their grant, exports cannot exhaust the server.

Repository-only review cannot prove bucket/account public-access state, live CDN cache
behavior, malware-scanner verdicts, enforced lifecycle rules, or real third-party storage
behavior. `secod-ship-check` owns final launch readiness; this skill never issues it.

## Scope and ownership

Owned controls: upload authorization and file-type/content validation (allowlists, magic-byte
checks, generated filenames); count/individual/aggregate size limits; decompression-bomb
protection; the malware-processing decision (antivirus, CDR, sandbox, or documented rejection)
where relevant; staging location and upload expiry; safe storage placement; safe content
disposition on serve/download; signed/shared URL authorization decisions (tenant/owner scope,
audience, expiry, single-use decision, rotation, revocation) including hashed-at-rest share
verifiers for server-validated file share links; cache/CDN privacy for private objects;
export/rendering resource bounds (time, input/output size, memory, page/item count,
concurrency); cancellation, timeout, deterministic cleanup of temporary files and long-lived
rendering resources; retention, deletion, and backup handling of stored files.

Excluded controls (owned elsewhere): path traversal and injection in request parameters
(`secod-inputs-apis`; this skill owns filename handling at the storage layer);
session/API-token/share-link lifecycle mechanics — verifier generation, hashed-at-rest storage,
comparison (`secod-identity-access`; this skill decides *that* a file share URL is a
server-validated bearer link and requires hashed-at-rest verifiers for it); rate limits,
quotas, and cost ceilings (`secod-abuse-limits`; this skill owns structural size/concurrency
bounds on file operations); encryption at rest and key management
(`secod-crypto-data-protection`); XSS/safe rendering of served content, CSP, general
cache-control headers (`secod-web-app-security`); OS command execution inside processing
pipelines (`secod-runtime-execution`); bucket policy, IAM, SAS/presigning platform
configuration, public-access posture (`secod-aws-s3-cloudfront`, `secod-google-cloud-storage`,
`secod-supabase`, `secod-firebase`, `secod-cloudflare-workers`,
`secod-vercel-platform`); audit-event plumbing and log redaction
(`secod-observability-response`); launch verdicts (`secod-ship-check`).

Direct dependencies (from `secod/catalog.json`): `secod-core`.

Conditional routes: `secod-identity-access` (bearer-verifier lifecycle depth),
`secod-inputs-apis`, `secod-abuse-limits`, `secod-web-app-security`,
`secod-runtime-execution`, `secod-crypto-data-protection`,
`secod-observability-response`, and the storage provider adapters listed above.

## Required inputs

Repository: upload/multipart handlers, direct-to-storage client code, presigned URL generation
and consumption, storage SDK usage and versions, share-link models and resolution routes,
image/PDF/archive/video processing libraries, scanner integration, export/report and rendering
jobs, temporary-file handling, CDN/proxy configuration, IaC bucket/lifecycle definitions, file-
flow tests.

Environment/version: runtime and framework versions, storage service and region per
environment, function/serverless payload limits, deployment targets.

Commonly unavailable from repository alone (require supplied evidence, else `Not verified`):
bucket/account public-access and policy state; production CDN/cache behavior for private
objects; scanner service availability, version, verdict latency; enforced lifecycle/expiry of
managed storage; revocation reach of already-issued signed URLs; backup contents.

Human-supplied evidence: storage inventory (buckets/containers/projects × environment × data
class); scanner/CDR product and configuration records; dated lifecycle-rule or retention
enforcement evidence; revocation test results; accepted-risk records for any intentionally
public content.

## Applicability and discovery

Signal groups:

- Package/SDK: storage clients (`@aws-sdk/client-s3`, `@google-cloud/storage`,
  `@vercel/blob`, `@supabase/supabase-js` storage, `firebase/storage`,
  Convex file storage, `uploadthing`), multipart parsers (`multer`, `formidable`, `busboy`),
  processing libraries (`sharp`, `pdf-lib`, `archiver`, `unzipper`, `ffmpeg*`, LibreOffice
  wrappers), scanners (`clamscan`, VirusTotal-style APIs).
- Environment variables: `*_BUCKET`, `AWS_S3_*`, `GCS_BUCKET`, `BLOB_READ_WRITE_TOKEN`,
  storage-using `SUPABASE_*`, `UPLOAD_*`,
  `SCAN_*`/`CLAMAV*`/`VT_API_KEY` class scanner credentials.
- Routes/webhooks: multipart POST handlers, `/upload`, `/download`, `/files/*`, `/export`,
  `/attachments/*`, share routes (`/s/:token`, `/share/:id`), storage-event webhooks
  (object-created/upload-complete).
- Configuration: `bodySizeLimit`/request-size settings, function memory/timeouts, CDN/cache
  rules, bucket lifecycle rules in IaC, quarantine directory setup.
- Deployment/provider evidence: bucket policy/public-access dashboards, signed URL
  configurations, storage event subscriptions, lifecycle rule state.

Classification follows `secod-core`: `Candidate` (storage package present, example variable,
dormant helper); `Likely` (upload/serve/export code exists but deployed/provider state
unverified); `Active` (repository behavior correlates with deployed/runtime/Dashboard/API/
provider evidence). Maintain separate development/preview/staging/production inventories —
buckets, public-access state, CDN behavior, and lifecycle rules routinely differ per
environment; conflicting or shared environment signals keep affected controls `Not verified`.

## Review workflow

1. Inventory environments and trust boundaries: every storage location, upload/serve/export/
   share flow, processing pipeline stage. Parallelizable once the inventory exists.
2. Correlate active flows: who uploads, what happens after storage (serve, process, share,
   export), which flows mint signed/shared URLs, which run rendering jobs.
3. Verify applicable controls below against code plus supplied external evidence.
4. Run safe negative tests: reason through spoofed-type, polyglot/double-extension,
   cross-tenant-ID, expired/reused-link, oversized/decompression-bomb, and cancelled-export
   cases against traced code/config. No production data changes without explicit
   authorization.
5. Classify evidence, emit findings, route gaps to owning skills, hand off to
   `secod-ship-check`.

Steps 1–2 are parallelizable across environments only when evidence is independent and no
state changes.

## Control requirements

The catalog defines no stable control IDs for this skill yet; identifiers below are
`PROVISIONAL-df-N` and require catalog approval before promotion. Map each control to OWASP
ASVS 5.0.0 Data Protection requirements using version-qualified identifiers (`v5.0.0-14.x`)
and the OWASP File Upload Cheat Sheet principles in `references/sources.md`.

### `PROVISIONAL-df-1` — Upload authorization and file-content validation

**Applicability:** Every flow that persists client-supplied bytes (multipart handlers, Server
Actions accepting blobs, direct-to-storage PUT/POST). Protects against code execution,
overwrites, and unauthorized writes.

**Inspect and verify:** Authentication and tenant/object authorization checked before any byte
is written; extension/MIME allowlist limited to business-critical types, applied after decoding
the filename, resistant to double extensions, null bytes, trailing characters, and case tricks;
client-declared `Content-Type` treated as untrusted; magic-byte/file-signature validation
against the expected type for every allowed format; filenames replaced with application-
generated values (UUID-class) or strictly validated (length bound, character subset, no path
segments, no reserved names); original name kept only as display metadata.

**Unsafe evidence:** User-controlled filename used as storage key; single-signal type checking
(extension or header alone) on a flow serving files back to users or other systems; denylist
extension filtering; signed-out upload without a documented public-intake design.

**Required negative test:** An upload whose declared type is `image/png` but whose bytes are an
HTML/script polyglot or double-extension payload must be rejected by signature validation; an
unauthorized principal's upload to another tenant's prefix must fail authorization.

**Passing / Not verified:** Pass requires every persisted-byte flow traced with authorization
plus layered type validation (allowlist + signature). Unestablishable storage destinations stay
`Not verified`.

**Related skill routing:** Path traversal in parameters → `secod-inputs-apis`; processing
subprocess safety → `secod-runtime-execution`.

### `PROVISIONAL-df-2` — Size limits and decompression-bomb protection

**Applicability:** Every upload intake and every archive/extraction step. Protects storage
capacity, memory, and CPU from exhaustion.

**Inspect and verify:** Per-request/per-file individual size limit enforced server-side (not
only in framework defaults or client UI); count limit per request; aggregate quota per
user/tenant where storage is shared; request-body limits aligned with the smallest enforcement
layer; archive extraction bounds declared before extraction: maximum uncompressed size,
maximum entry count, maximum compression ratio, maximum per-entry and total extracted bytes,
entry-name traversal checks; streamed processing instead of whole-file buffering where sizes
are untrusted.

**Unsafe evidence:** No explicit size check anywhere in the traced path; archives extracted
without pre-computed output bounds; ratio/total-size checks absent on `.zip`/`.gz`/`.tar`
inputs; image/document processors invoked on attacker-sized inputs without dimension/page
bounds.

**Required negative test:** A small archive that expands beyond the declared uncompressed limit
must be rejected before allocation exceeds the bound; a batch over the count limit must be
rejected wholesale, not partially written.

**Passing / Not verified:** Pass requires server-side limits traced on every intake and
extraction path with concrete bound values. Framework-default-only limits without confirmation
they apply to the deployed runtime stay `Not verified`.

**Related skill routing:** Quota ceilings and abuse rates → `secod-abuse-limits`; processing
subprocess isolation → `secod-runtime-execution`.

### `PROVISIONAL-df-3` — Malware and active-content processing decision

**Applicability:** Every upload that will be consumed by people, staff, or automated pipelines
where the type carries executable/active risk (documents with macros, PDFs, office files,
archives, images processed by parsers). The decision may be "scan", "disarm", "sandbox",
"restrict types", or documented acceptance — never silence.

**Inspect and verify:** An explicit recorded decision exists per risky type; where scanning/
CDR/sandboxing is chosen: scanner wired into the intake path before the file becomes available
to consumers, scan failure/unavailability holds the file in quarantine (fail closed), scanner
result recorded; where the decision is restriction: risky formats excluded from the allowlist
with justification; where the decision is acceptance: named owner and residual-risk record.
Public retrievability raises the bar — illegal-content reporting path considered.

**Unsafe evidence:** Risky types accepted with no scanner, no disarm step, and no acceptance
record; scanner present but failures pass files through; scanning happens after files are
already served.

**Required negative test:** With the scanner dependency unavailable (simulated), a newly
uploaded file must remain quarantined and unservable until a verdict exists.
**Passing / Not verified:** Pass requires the decision traceable per type plus wiring evidence.
Scanner effectiveness/version needs supplied vendor/service evidence else `Not verified`.

### `PROVISIONAL-df-4` — Staging, storage placement, and upload expiry

**Applicability:** Every upload between first byte and final committed state, plus where
committed files physically live relative to application execution.

**Inspect and verify:** Unvalidated/staged uploads land outside executable paths and outside
the webroot (or in object storage with no public serving); staging objects expire (presigned
upload TTL, lifecycle rule, or explicit sweeper) so abandoned partials cannot accumulate
forever; committed keys namespaced by tenant/id so listing cannot leak siblings; upload
completion is atomic from the consumer's view (no half-written reads); direct-to-storage flows
validate the eventual object (type/size recheck on the stored object, not just the request).

**Unsafe evidence:** Uploads written into directories served statically by the app or web
server with handler mappings intact; staging area with no expiry mechanism; direct-to-storage
flows trusting the upload request without validating the resulting object.

**Required negative test:** A staged upload abandoned past the configured TTL must become
unreachable/reaped; an object uploaded via presigned PUT with disallowed type/size must be
detected at completion time and quarantined/rejected.

**Passing / Not verified:** Pass requires placement plus expiry evidence per flow. Managed
lifecycle-rule enforcement needs supplied Dashboard/API evidence else `Not verified`.

**Related skill routing:** Bucket/network platform posture → storage provider adapters.

### `PROVISIONAL-df-5` — Safe download and content disposition

**Applicability:** Every flow that serves stored bytes to a browser or client. Protects users
from active content executing under the application's origin.

**Inspect and verify:** Downloads of user-uploaded or otherwise untrusted content delivered
with `Content-Disposition: attachment` (or equivalent forced-download) and a safe,
non-spoofed `Content-Type` from a neutral or isolated origin; `X-Content-Type-Options:
nosniff` set on those responses; inline rendering permitted only for validated, actively
sanitized types with the sanitization owned by `secod-web-app-security`; user-uploaded content
served from a separate cookie-less domain/origin where architecture allows; no path/ID
confusion letting one object key resolve to another's bytes.

**Unsafe evidence:** Untrusted uploads served inline under the main app origin; content type
echoed from the stored filename; SVG/HTML served inline from user uploads.

**Required negative test:** Fetching an uploaded HTML/SVG fixture through the traced serve path
must return `Content-Disposition: attachment` (or be blocked), never render inline on the
application origin.

**Passing / Not verified:** Pass requires serve-path headers traced for every untrusted-content
route. Live CDN-transformed responses need supplied captures else `Not verified`.

**Related skill routing:** XSS/sanitization for rendered content → `secod-web-app-security`.

### `PROVISIONAL-df-6` — Signed and shared URL authorization

**Applicability:** Every presigned URL, SAS, capability URL, or share link that grants access
to a stored object. Treat each as a bearer capability: possession authorizes nothing except
what was explicitly granted.

**Inspect and verify:** Issuance happens only after backend authentication and tenant/owner/
action authorization; scope narrowed to one operation, one object/prefix, required
content-type/length/checksum constraints where supported; short expiry proportionate to purpose
with the value recorded; single-use/downgrade decision made deliberately (one-time tokens for
high-value objects where supported, else documented multi-read rationale); rotation/revocation
strategy exists and covers already-issued URLs within a bounded window (or expiry short enough
to compensate); share links resolved server-side validate the verifier against a stored
hash/keyed digest — never a plaintext lookup — with CSPRNG verifiers, and never expose the raw
verifier in logs; the client cannot influence object ID/prefix/permission fields inside the
signed payload.

**Unsafe evidence:** Presigned URLs minted without per-object authorization (e.g., client
passes full key/path); permanent or non-expiring share links; share verifier stored plaintext;
revocation impossible with long expiries; signed URL returned in logs, analytics payloads, or
referrer-visible contexts.

**Required negative test:** A share/presigned URL issued for tenant A's object must fail (403/
invalid signature) when redirected to tenant B's object key; an expired or revoked link must
stop resolving; a database dump of the shares table must not reveal usable verifiers.

**Passing / Not verified:** Pass requires issuance-side authorization traced per flow plus
expiry/revocation evidence. Actual revocation reach of previously issued URLs needs supplied
provider evidence else `Not verified`.

**Related skill routing:** Verifier generation/hashing/comparison mechanics and lifecycle
depth → `secod-identity-access`; platform SAS/presigning configuration → storage provider
adapters; audit events for issuance/revocation → `secod-observability-response`.

### `PROVISIONAL-df-7` — Cache and CDN privacy for private objects

**Applicability:** Every response carrying private/user-specific file bytes or file metadata
passing through any shared cache, CDN, or proxy.

**Inspect and verify:** Private responses carry explicit no-shared-cache directives
(`Cache-Control: private, no-store` class) or are excluded from caching by configuration;
signed-URL responses evaluated for edge caching (some CDNs cache by URL ignoring query
variants — confirm behavior); cache keys cannot collide across tenants; error pages and
redirects do not leak cached private bodies; purge mechanism exists for wrongly cached
private objects.

**Unsafe evidence:** Authorization-checked downloads with default cacheability through a shared
CDN; tenant-specific thumbnails/exports sharing one cache key; no answer to "how would we purge
a leaked cache entry".

**Required negative test:** Two principals requesting their own copies of the same logical
resource must never receive each other's bytes via cache; reasoning must cover the deployed
CDN's key normalization.

**Passing / Not verified:** Pass requires directive/configuration evidence per route. Live edge
behavior without supplied traces stays `Not verified`.

**Related skill routing:** General cache-control and cache-poisoning review →
`secod-web-app-security`; platform CDN behavior → storage/hosting adapters.

### `PROVISIONAL-df-8` — Export and rendering resource bounds

**Applicability:** Every report/CSV/PDF/zip export, thumbnail pipeline, headless-browser
render, video/image transcode, or bulk serialization job.

**Inspect and verify:** Explicit wall-clock timeout per job; input row/item count cap and
output size cap; streaming/chunked emission rather than unbounded in-memory accumulation;
memory ceiling aligned with the runtime; concurrent-job limit per user/tenant and globally;
pagination respected rather than loading unbounded result sets; renderer given bounded
page/viewport/resource budgets (headless browsers: navigation, asset, and time caps).

**Unsafe evidence:** Exports iterating entire tables into memory; no timeout on render workers;
concurrency unbounded per user; output assembled as one growing string/buffer.

**Required negative test:** A job exceeding its item or byte budget must abort with a partial,
clearly-marked result or clean failure — never complete by silently truncating or by OOM.

**Passing / Not verified:** Pass requires bounds present and enforced in code for every
identified job type. Platform-enforced ceilings claimed without documentation stay
`Not verified`.

**Related skill routing:** Rate/cost quotas on expensive operations → `secod-abuse-limits`;
headless-browser network egress → `secod-inputs-apis`/platform adapters.

### `PROVISIONAL-df-9` — Cancellation, timeout, and deterministic cleanup

**Applicability:** Every temporary file, staged artifact, render sandbox, and long-lived
worker created for upload/processing/export flows.

**Inspect and verify:** Client disconnect/cancellation propagates to the job (abort signals,
worker termination); timeouts propagate rather than orphan work; temporary files written to
per-job directories removed on success, failure, and cancellation alike — deterministic cleanup
paths exist for all three; startup reconciliation sweeps orphans from crashed runs; long-lived
rendering resources (browser instances, transcoder pools) recycle with hard lifetime caps.

**Unsafe evidence:** Temp files written to a shared directory with cleanup only on success;
cancelled exports leave running workers; no crash-recovery sweep; render pool grows without
bound under load.

**Required negative test:** Cancel an export mid-run (simulated): worker stops, partial output
and temp artifacts are removed, and no orphan process remains; kill a job forcibly: next
startup sweep removes its leftovers.

**Passing / Not verified:** Pass requires all three terminal states (success/failure/cancel)
covered per job type. Behavior of managed platforms' cleanup claims stays `Not verified`
without supplied evidence.

**Related skill routing:** Timeout/cancellation propagation patterns → `secod-failure-safety`
via routing; degraded-mode tests → `secod-abuse-limits`.

### `PROVISIONAL-df-10` — Retention, deletion, and backup handling of stored files

**Applicability:** Every stored object and every backup/export containing file data.

**Inspect and verify:** Retention defined per file class (period + trigger + owner); deletion
paths cover the object plus every derived copy (thumbnails, transcoded variants, CDN cache,
search indexes, AI/embedding copies routed to owning skills); deletion verification step
confirms removal; backups containing file data follow an explicit policy — expiry-bounded
retention or documented re-delete on restore; legal-hold/immutability features deliberately
configured; account/tenant teardown reaches object storage, not just database rows.

**Unsafe evidence:** Deleted accounts' objects persisting with no lifecycle bound; derived
copies (thumbnails/variants) unreachable by the delete path; immutability/retention locks
enabled without a documented recovery decision.

**Required negative test:** Delete a test file through the traced path, then probe primary,
derived-copy, and cache locations (or reason through each store's mechanism when live testing
is unauthorized) — residuals must be bounded by documented policy, never indefinite.

**Passing / Not verified:** Pass requires store-by-store mapping plus verification evidence.
Provider-side deletion outcomes and backup contents stay `Not verified` without supplied
confirmation.

**Related skill routing:** Deletion-propagation lifecycle depth and backup encryption →
`secod-crypto-data-protection`; provider deletion APIs → storage provider adapters.

## Exceptional and failure conditions

Fail closed on target-reachable failure flows:

- Scanner dependency unavailable or timed out: hold uploads in quarantine, never release on
  scan-absence; document the hold-and-retry path.
- Partial upload/intake failure: staged object without a committed record must be reconciled
  by expiry or sweeper; never expose half-committed objects to consumers. Presigned uploads
  expiring mid-transfer: retry mints a fresh authorized URL; post-expiry completions rejected.
- Extraction failing mid-archive: remove partial extraction deterministically; never serve a
  partially expanded tree.
- Export/render cancellation or timeout: terminate the worker, mark the job failed or
  partially-complete explicitly, clean artifacts; a silent truncated success is a defect.
- Share/signed-URL revocation: takes effect within the documented window; where caches delay
  reachability, the bound is stated, never invented — unknown reach is `Not verified`.
- Storage-provider outage: uploads/downloads fail closed with clear errors; no fallback that
  writes user data to unapproved local/temp locations.
- Never invent provider retry schedules, delivery guarantees, or revocation latencies; rely
  only on documented provider behavior or mark `Not verified`.
- A failed checker or incomplete negative test never counts as success.

## Dependency and routing rules

Direct dependencies (from `secod/catalog.json`): `secod-core`.

Conditional routes: `secod-identity-access` (bearer-verifier mechanics and lifecycle),
`secod-inputs-apis` (path traversal, SSRF in fetch-from-URL upload flows), `secod-abuse-limits`
(quota/cost), `secod-web-app-security` (serving user content, sanitization),
`secod-runtime-execution` (processing subprocesses), `secod-crypto-data-protection` (deletion
propagation, encrypted backups), `secod-observability-response` (upload/share/delete audit
events), `secod-failure-safety` patterns via routed skills, and storage provider adapters
(`secod-aws-s3-cloudfront`, `secod-google-cloud-storage`, `secod-supabase`, `secod-firebase`,
`secod-cloudflare-workers`, `secod-vercel-platform`) for
bucket policy, IAM, SAS/presigning configuration, and Dashboard evidence.

If `secod-core` or a required routed skill is missing/unresolved/malformed/incomplete: mark
affected controls `Not verified`, name the missing owner/evidence, never invent replacement
dependencies, never issue launch readiness.

## Evidence and status rules

Statuses: `Do not ship`, `Fix before launch`, `Recommended hardening`, `Passed with evidence`,
`Not verified`.

Target-specific thresholds:

- `Passed with evidence`: every upload/serve/share/export flow inventoried and traced;
  authorization plus layered content validation on each intake; server-side size and extraction
  bounds with values; disposition and cache directives evidenced; issuance-side authorization,
  expiry, revocation, hashed-at-rest share verifiers proven; cleanup covered for all three
  terminal states; retention mapped store-by-store.
- `Do not ship`: unauthenticated or cross-tenant write/read of stored objects; uploads landing
  in executable/statically-served paths with handlers intact; unbounded archive extraction on
  reachable paths; private objects publicly readable via storage or CDN with no boundary.
- `Fix before launch`: signature/type validation missing where uploads are served onward;
  user-controlled storage keys; no server-side size limit; untrusted content served inline on
  the app origin; non-expiring, non-revocable share links; plaintext share verifiers; exports
  without timeout/memory bounds; missing deterministic temp cleanup.
- `Recommended hardening`: no malware-processing decision for risky types; no aggregate quota;
  staging without expiry; retention undefined for some file classes; renderer pools without
  lifetime caps.
- `Not verified`: bucket/account public-access state, live CDN cache behavior, scanner
  effectiveness, enforced lifecycle rules, revocation reach of issued URLs, backup contents —
  each with the exact missing evidence named.

Never pass inferred, package-only, inaccessible, stale, contradictory, incomplete, unsupported,
or failed evidence.

## Required output

One finding per applicable control: `control_id`, `title`, `status`, `scope`, `evidence`,
`impact`, `recommended_fix`, `verification`, `limitations`, `source_refs`, `routed_skills`.

End the report with: applicability inventory (file flows × stores × environments; share-link
register; processing-job register); test results; requested external evidence (bucket policy/
public-access confirmations, CDN behavior traces, scanner records, lifecycle-enforcement proof,
revocation tests — by owner); `Not verified` items with next verification step; launch
blockers. Route overall launch readiness to `secod-ship-check`.

## Negative fixtures and tests

All fixtures for this skill are documentation-only plans; none execute code locally.

| Fixture | Type | Controls exercised |
| --- | --- | --- |
| `tests/insecure-fixtures/secod-data-files/README.md` | Documentation-only plan | All controls |
| Polyglot upload; zip bomb; unscanned macro; public staging; inline active content | Documentation-only cases | -1 through -5 |
| Cross-tenant share; private CDN cache; unbounded export; cancelled worker; retained objects | Documentation-only cases | -6 through -10 |
| Missing-evidence case: bucket public-access and CDN behavior unverifiable | Documentation-only plan | -4, -6, -7 |
| Failure case: scanner outage releases file to consumers anyway | Documentation-only case | -3 |

Reasoning-based verification only. Never claim Markdown fixture plans executed as code. Never
run destructive, production-changing, user-creating, payment-creating, refunding, key-rotating,
dashboard-changing, or account-changing tests without explicit authorization.

## References

- [`references/sources.md`](references/sources.md) — source register: OWASP ASVS 5.0.0 (V14 Data
  Protection), OWASP File Upload Cheat Sheet, OWASP Unrestricted File Upload, OWASP Top 10
  2025 A10 (fail-closed exceptional-condition behavior).
