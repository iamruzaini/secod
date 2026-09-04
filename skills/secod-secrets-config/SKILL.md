---
name: secod-secrets-config
description: Review how privileged credentials and bearer capabilities are created, stored, scoped, rotated, revoked, and kept out of source, client bundles, URLs, logs, outputs, and git history; separate environments and block unsafe production configuration. Triggers include `.env*` files, committed credentials or key-prefix literals (`sk_live_`, `AKIA`, `sb_secret_`, `ghp_`, PEM blocks), `NEXT_PUBLIC_*`/`VITE_*` variables, docker-compose/Kubernetes/Terraform/CI plaintext secrets, seed scripts and demo accounts, rotation or revocation requests, leaked-secret disclosures, and git-history cleanup requests; package presence alone is Candidate.
---

# Secrets and Configuration Security

## Mission

Keep privileged credentials and bearer capabilities server-side, least-privileged, classifiable,
rotatable, and revocable; keep development, preview, staging, test, and live environments
separated; and block unsafe production configuration including default credentials and
development bypasses.

Repository-only review cannot prove deployed environment-variable values, dashboard secret-store
state, server-side push-protection status, provider-side cache purge results, completed rotations,
or runtime debug-flag state. It establishes candidates and verifies repository-correlated
behavior. `secod-ship-check` owns final launch readiness; this skill never issues it.

## Scope and ownership

Owned controls: secret-free source/bundle/transport/output surfaces; bearer-capability browser
isolation; credential scoping; secret-versus-configuration classification and template parity;
secret storage mechanism selection; environment separation; rotation and revocation readiness;
production configuration safety; git-history exposure response; default-credential elimination.

Excluded controls (owned elsewhere): session/share-link/capability verifier generation, hashing,
expiry, and lifecycle (`secod-identity-access`); webhook authenticity, replay, and signature
validation (`secod-inputs-apis`); cryptographic primitive and key-derivation choices
(`secod-crypto-data-protection`); CI token minimization, Action pinning, release integrity
(`secod-packages-delivery`); scanner program governance, SBOM, triage SLAs
(`secod-vulnerability-management`); audit-log redaction and incident runbooks
(`secod-observability-response`); image-layer and BuildKit build-secret mechanics
(`secod-container-runtime`); platform-specific secret-store behavior (hosting/provider adapters
such as `secod-vercel-platform`, `secod-cloudflare`, `secod-aws-*`, and the Google Cloud
family); debug-endpoint exposure (`secod-inputs-apis`); exceptional-condition
behavior (`secod-failure-safety`).

Direct dependencies: `secod-core`.

Conditional routes: hosting/provider adapters when their secret-storage surfaces are Active or
Likely (resolve exact slugs from the live `secod/catalog.json`); `secod-container-runtime` when
container builds exist; `secod-crypto-data-protection` when key-material lifecycle choices arise;
`secod-observability-response` for revocation-event visibility; `secod-ship-check` always.

## Required inputs

Repository inputs: full file tree including nested workspaces; manifests, lockfiles, and
configuration; committed example/template environment files (`.env.example`-class); source for
variable references, defaults, logging, serialization; CI workflows and deployment definitions;
IaC and manifests carrying environment or secret declarations; seed scripts and fixtures;
accessible git history (full clone with all refs, not shallow) when history review applies.

Environment-variable **names** only. Never read, quote, copy, or export secret **values**, and
never read `.env` contents; discovery uses names and structural signals only.

Commonly unavailable from repository alone (require supplied evidence, else `Not verified`):
deployed values and scope of variables per environment; dashboard/secret-store/vault
configuration; server-side push-protection enablement; provider-side cache and code-review-ref
purge outcomes; rotation completion dates and revocation-test records; production runtime flag
state; fork/clone census after history leaks.

Human-supplied evidence: authorized read-only dashboard/API exports, environment inventories per
environment (development, preview, staging, production separately), rotation/revocation records,
push-protection settings, deployment logs.

## Applicability and discovery

Always applicable: every review touches credentials or configuration somewhere.

Signal groups:

- Package/SDK: secret-scanner configs (gitleaks/trufflehog-class), secret-manager clients,
  dotenv loaders, key-management SDKs.
- Environment variables: names referenced in code, validators, examples, templates, CI, IaC;
  client-exposed prefixes (`NEXT_PUBLIC_*`, `VITE_*`, `REACT_APP_*`, `EXPO_PUBLIC_*`,
  `NUXT_PUBLIC_*`).
- Routes/webhooks: handlers serializing tokens into responses, redirect builders embedding
  credentials in query strings, RPC/Server Action payloads accepting privileged tokens.
- Configuration: compose/Kubernetes/Helm/Terraform/CI YAML with literal credentials or secret
  declarations, wrangler/platform secret bindings, seed scripts, demo/bootstrap fixtures,
  `.env.example`-class templates.
- Deployment/provider evidence: platform secret-store bindings, authorized dashboard exports,
  push-protection settings, deployment logs.

Classification:

- `Candidate`: package present, example variable name, dormant file, template entry, or weak
  signal only; no corroborating use.
- `Likely`: code/configuration exists and correlates with use, but deployed/provider state is
  unverified.
- `Active`: repository behavior correlates with deployed, runtime, Dashboard, Management API, or
  other provider evidence.

Maintain separate inventories for development, preview, staging, and production. Conflicting or
shared environment signals are classified `Conflicting` and force affected controls to
`Not verified`. Never paste matched secret values into findings; record path, line, variable or
key name, and match class with the value redacted.

## Review workflow

1. Inventory environments and trust boundaries: environments, deploy targets, client/server
   bundle boundaries, CI/build contexts, secret stores. Parallelizable across roots when strictly
   read-only.
2. Correlate active features and flows: enumerate every credential name, its consumer code paths,
   its classification, and every bearer capability crossing a trust boundary. Parallelizable per
   root after step 1 completes there.
3. Verify the controls below in order; resolve platform routes from the live catalog.
4. Run safe negative tests: local read-only scans, template-parity diffs, fixture reviews.
   Deployed-system probes (default-credential checks against a running system) require explicit
   authorization.
5. Classify evidence, emit findings, route each to its owner, hand off to `secod-ship-check`.

## Control requirements

The catalog defines no stable control IDs for this skill yet; identifiers below are
`PROVISIONAL-secrets-config-N` and require catalog approval before promotion.

### `PROVISIONAL-secrets-config-1` — No secrets in source, bundles, transport, or output surfaces

**Applicability:** Every repository. Protects confidentiality of every privileged credential.

**Inspect and verify:** Scan tracked files and available history for high-entropy literals,
known key prefixes (`sk_live_`, `sk_test_`, `AKIA`, `sb_secret_`, `ghp_`, `xoxb-`, PEM
`-----BEGIN ... PRIVATE KEY-----` blocks), connection strings with embedded credentials, and
hardcoded tokens in source, tests, docs, scripts, and CI. Verify client entrypoints, public
directories, and client-bundle inputs contain no server-only modules, constants, or imported
credentials. Check URL construction for tokens, keys, or passwords in query strings or paths.
Check log, trace, error, and analytics emission points for credential interpolation. Check prompt
construction and AI context assembly for secrets. Check response bodies and headers for raw
session, share, Access, or provider credentials. Prefer a maintained scanner (gitleaks/
trufflehog-class) plus targeted `rg` searches; redact every match value in output.

**Unsafe evidence:** Any live-looking credential left unredacted in output; a credential import
reachable from client code; a token-bearing URL emitted to logs; scanner findings dismissed
without verification.

**Required negative test:** A fixture commit containing a fake high-entropy key must be flagged
by the scan procedure; a log statement interpolating a credential must be reported, never passed.

**Passing / Not verified:** Pass requires recorded scan coverage over all discovered scopes plus
history where available, with zero unresolved live-credential findings and redacted evidence.
Unscannable scopes, failed or timed-out scans, or missing history keep affected coverage
`Not verified`.

**Related skill routing:** Client-rendering boundaries (`secod-web-app-security`);
log-redaction obligations (`secod-observability-response`); prompt-context isolation
(`secod-ai-api-integrations`).

### `PROVISIONAL-secrets-config-2` — Bearer capabilities never reach user-authored code or client RPC

**Applicability:** Every session identifier, share link, capability URL, Access token, and
provider credential the application mints or proxies.

**Inspect and verify:** Trace each bearer capability from minting through storage, delivery, and
consumption. Confirm raw verifiers/tokens are never serialized into client components, props,
RPC or Server Action payloads, `postMessage` targets, URLs, `localStorage`/`sessionStorage`, or
JS-readable cookies where HttpOnly is feasible. Confirm server-side comparisons use hashed or
keyed digests rather than client-supplied plaintext lookups. Confirm client RPC argument schemas
do not accept privileged tokens or caller-asserted capability claims as authorization input.

**Unsafe evidence:** A raw share-link verifier returned in an API response; a provider key
imported by a client bundle entrypoint; an RPC trusting a client-supplied capability string
without server-side validation.

**Required negative test:** A fixture endpoint returning the session token in a JSON body must
be flagged `Do not ship`; a client-RPC fixture honoring a caller-supplied tenant capability must
be flagged.

**Passing / Not verified:** Pass requires every inventoried bearer flow traced end-to-end with
server-only custody evidence at each hop. Any incomplete trace keeps that flow `Not verified`.

**Related skill routing:** Verifier generation, hashing, expiry, and lifecycle
(`secod-identity-access`); webhook authenticity (`secod-inputs-apis`).

### `PROVISIONAL-secrets-config-3` — Credentials are scoped and least-privileged

**Applicability:** Every Active provider credential, database role, API key, service account,
and machine identity.

**Inspect and verify:** For each credential, record its declared scope/permissions from repo
config or IaC where visible, and the operations consuming code actually performs. Flag
wildcard scopes beyond demonstrated need, administrative credentials used for routine reads,
one credential shared across unrelated services or environments, and long-lived credentials
where short-lived or scoped alternatives exist in the stack. Where scope is not visible in the
repository, request an authorized dashboard/IAM export.

**Unsafe evidence:** A service-role/admin/superuser credential used in the normal request path;
a single API key serving production and development; wildcard resource scope justified only by
convenience.

**Required negative test:** A fixture whose app runtime connects with an unrestricted superuser
URL must be flagged `Fix before launch` with a named least-privilege alternative.

**Passing / Not verified:** Pass requires each Active credential to have recorded intended
scope, observed use, and a matching-or-justified relationship. Scope not provable from the
repository keeps that credential `Not verified` pending dashboard evidence.

**Related skill routing:** Platform IAM/RBAC specifics (exact provider adapter); tenant/object
authorization in data access (data-plane adapters such as `secod-supabase`).

### `PROVISIONAL-secrets-config-4` — Secret values versus non-secret configuration, with template parity

**Applicability:** Every environment variable and configuration value.

**Inspect and verify:** Classify every referenced variable name as secret (credentials, keys,
tokens, private material) or non-secret configuration (hosts, flags, feature toggles, public
IDs). Cross-check `.env.example`-class templates and schema validators against code-referenced
names: missing template entries; template entries containing plausible real values; secret
names with inline fallback defaults in code (`process.env.X || "<literal>"`-class); secrets
misclassified as public config; non-secret values misclassified as secrets (creating false
rotation burden). Confirm validators surface missing secret names without printing values.

**Unsafe evidence:** A template file containing a live-format credential; a secret with an
inline default; a validator that dumps the environment on failure.

**Required negative test:** A fixture `.env.example` containing a live-format key must be
flagged; a missing-template case must enumerate absent names, never pass silently.

**Passing / Not verified:** Pass requires a complete per-environment classification table with
template and validator parity. Names that cannot be resolved to a classification keep affected
coverage `Not verified`.

**Related skill routing:** Client-exposed variable discipline (`secod-nextjs`,
`secod-vercel-platform`, framework adapters).

### `PROVISIONAL-secrets-config-5` — Secrets live in managed storage, injected at deploy/runtime

**Applicability:** Every location where credentials are persisted or injected: environment
variables, secret managers, vaults, platform secret stores, CI secret stores.

**Inspect and verify:** Identify the storage mechanism per environment from deployment configs,
IaC, and CI. Prefer encrypted secret stores or platform secret bindings over plaintext
environment entries in manifests. Search for literal credentials in compose files, Kubernetes
manifests, Terraform, task definitions, CI YAML, and CLI-invoked commands. Verify injection
happens at deploy/runtime, never at build time, and that build args and image layers receive no
secrets. Verify client-exposed prefixes (`NEXT_PUBLIC_*`, `VITE_*`, equivalents) reference no
secret-classified names.

**Unsafe evidence:** A plaintext password in a committed manifest; a secret passed as a build
argument; a secret behind a client-exposed prefix regardless of claimed harmlessness.

**Required negative test:** A compose fixture with a literal password must be flagged; a
`NEXT_PUBLIC_*` secret fixture must be flagged.

**Passing / Not verified:** Pass requires every Active secret traced to a managed store with
injection-point evidence. Repository evidence cannot prove store configuration; that portion
stays `Not verified` pending dashboard export.

**Related skill routing:** Exact store semantics (`secod-vercel-platform`, `secod-cloudflare`,
AWS/Google Cloud families); build-layer mechanics
(`secod-container-runtime`); CI secret hygiene (`secod-packages-delivery`).

### `PROVISIONAL-secrets-config-6` — Environments are separated, including test/live and development/production

**Applicability:** Every application deployed to more than one environment, and every payment,
messaging, or provider integration with test/live modes.

**Inspect and verify:** Map each environment to its distinct credential set, project, account,
or workspace using structural signals: distinct project refs, hosts, account IDs, binding names,
and per-environment configuration files. Verify preview and development configurations cannot
reach production data stores or live provider modes; verify test-mode and live-mode provider keys
are never mixed. Treat identical credential identities across environments as sharing.

**Unsafe evidence:** One credential identity serving production and lower environments; staging
configured against the production database host; live payment keys in a sandbox flow; merged
cross-environment inventories.

**Required negative test:** A staging fixture referencing the production host must be flagged;
mixed test/live keys must be flagged.

**Passing / Not verified:** Pass requires a per-environment inventory showing distinct
credential identities, evidenced structurally or by supplied export. Shared or conflicting
signals are `Conflicting`: affected controls `Not verified`.

**Related skill routing:** Provider environment models (payment adapters, messaging adapter,
platform adapters); preview protection (`secod-vercel-platform`, hosting adapters).

### `PROVISIONAL-secrets-config-7` — Every long-lived credential has a working rotation and revocation path

**Applicability:** Every long-lived credential in any environment, prioritized by privilege.

**Inspect and verify:** Record per credential: owner, rotation expectation, and revocation
procedure (documented dashboard steps or scripted API calls). Check for versioned-secret support
permitting overlapping validity during rotation, and for consumers that tolerate version
switchover. Verify incident procedures reference these paths. The repository cannot prove a
rotation happened or a revocation works: require supplied evidence of last rotation date and a
tested revocation, else `Not verified`.

**Unsafe evidence:** Credentials with no identified revocation path; rotation plans naming
nonexistent tooling; revocation requiring full downtime without documented acceptance;
"removed from HEAD" treated as revoked.

**Required negative test:** A missing-evidence fixture must record rotation status `Not
verified`, never `Passed with evidence`.

**Passing / Not verified:** Pass requires owner plus procedure plus supplied currency evidence
per credential. Privileged credentials without any revocation path are `Fix before launch`;
lower-privilege gaps are `Recommended hardening`; unevidenced status stays `Not verified`.

**Related skill routing:** Revocation-event visibility and alerting
(`secod-observability-response`); key-material lifecycle decisions
(`secod-crypto-data-protection`); API-key lifecycle mechanics (`secod-identity-access`).

### `PROVISIONAL-secrets-config-8` — Production runs without debug flags, development bypasses, or insecure defaults

**Applicability:** The production environment configuration of every deployed application.

**Inspect and verify:** Inventory every debug flag, verbose-error mode, mock/stub authentication
path, authorization bypass switch, seeded demo dataset, maintenance backdoor, and insecure
default (permissive CORS, disabled TLS verification, permissive cookie settings) discoverable
in code and configuration. Verify each bypass is gated so that production cannot activate it,
including the unset-variable default direction: a bypass that activates when its flag is unset
is a fail-open defect. Verify production deploy configuration overrides every insecure default.
Verify `NODE_ENV`/environment-conditioned weakening genuinely excludes production.

**Unsafe evidence:** A bypass reachable in production because a flag defaults to enabled;
debug mode enabled by production environment values; a TLS-verification opt-out carried into
production; demo data seeded into production.

**Required negative test:** A fixture where the bypass activates when `BYPASS_AUTH` is unset
must be flagged as a fail-open defect; a production deploy config enabling debug must be
flagged.

**Passing / Not verified:** Pass requires every discovered toggle classified with its production
value evidenced by deployment configuration or export. Runtime values not provable from the
repository stay `Not verified` pending supplied evidence.

**Related skill routing:** Debug-surface exposure while signed out (`secod-inputs-apis`);
fail-safe behavior (`secod-failure-safety`); hosting adapter environment evidence.

### `PROVISIONAL-secrets-config-9` — Git-history exposure: revoke first, then rewrite, then block recurrence

**Applicability:** Any secret ever committed, whether found by history scanning or disclosed by
report. Any secret ever committed is exposed even after removal from HEAD.

Order matters; follow exactly.

**Inspect and verify:** When a committed credential is found or reported, verify the response
plan follows this sequence:

1. Rotate or revoke the exposed credential immediately, before any cleanup. Cleanup never
   substitutes for revocation.
2. Rewrite history with a purpose-built tool (`git-filter-repo`, including its
   `--sensitive-data-removal` flow, or BFG-class) in a fresh clone.
3. Coordinate force-pushes across all refs, including tags.
4. Require all collaborators to re-clone rather than pull.
5. Purge provider-side caches and code-review ref namespaces where supported.
6. Remove orphaned LFS objects.
7. Assume forks and every existing clone retain the data indefinitely.
8. Block recurrence with pre-commit/pre-push secret scanning (gitleaks/trufflehog-class) plus
   server-side push protection.

Scan available history (`git log --all`-based scanner runs) for additional exposures whenever
one is found.

**Unsafe evidence:** Any plan rewriting history before revocation; any claim that removing the
secret from HEAD remediates exposure; any assumption that purges reach forks or existing clones;
recurrence controls absent after a confirmed leak.

**Required negative test:** A remediation plan ordering cleanup before rotation must be rejected
as misordered; a fixture with a removed-but-unrevoked key remains `Do not ship` until rotation
evidence is supplied.

**Passing / Not verified:** Pass requires supplied evidence of completed revocation plus both
recurrence controls (repo-level scanning hooks and server-side push protection). Revocation
claims without evidence, or push-protection claims without dashboard export, stay `Not verified`
or `Do not ship` for the affected credential.

**Related skill routing:** Push protection and hook enforcement evidence
(`secod-vulnerability-management`, `secod-packages-delivery`); breach containment runbooks
(`secod-observability-response`); session/refresh-family revocation
(`secod-identity-access`).

### `PROVISIONAL-secrets-config-10` — Default credentials eliminated before deployment

**Applicability:** Every deployed component that ships vendor/default credentials: admin
consoles, databases, devices, frameworks with default accounts, and application seed data.

**Inspect and verify:** Inventory documented vendor defaults for every detected component from
official vendor documentation; inventory seed scripts, migrations, fixtures, and bootstrap code
creating default users, passwords, API keys, or demo tenants. Verify vendor/default passwords,
API keys, and console or device credentials are replaced with instance-unique or
installation-time credentials before deployment; verify unused default accounts, tokens, and
demo/bootstrap data are removed or disabled for production.

**Unsafe evidence:** A migration seeding an administrative account with a documented default
password; an unchanged vendor default in deployed configuration; demo tenants or bootstrap
datasets present in production.

**Required negative test:** A fixture migration seeding `admin/<known default>` must be flagged.
Verification against a deployed system means testing documented defaults while signed out; this
is a network probe and requires explicit authorization. Without authorization it stays
`Not verified`, never `Passed with evidence`.

**Passing / Not verified:** Pass requires either an authorized default-credential probe against
the deployment showing rejection of documented defaults, or structural evidence the defaults
never existed in production. Source absence alone proves nothing about deployed state.

**Related skill routing:** Component-specific defaults (exact provider/runtime adapter);
seeded-account authorization implications (`secod-identity-access`).

## Exceptional and failure conditions

- Scanner failure, timeout, or cancellation: record searched scope, partial evidence, and next
  step; affected controls stay `Not verified`. Never pass from partial scans.
- Shallow or unavailable history: history-dependent controls (-1, -9) stay `Not verified`;
  request a full clone with all refs.
- Partial rotation (some credentials rotated, others not): the unrotated remain exposed; overall
  status for -9 stays `Do not ship` until the set is complete.
- Unknown revocation timing: treat the credential as still valid.
- Conflicting repository versus deployment evidence: record both with scope and time, classify
  `Conflicting`, keep affected controls `Not verified`, name the reconciling owner.
- Webhook duplicate, replay, redelivery, and failure handling belong to `secod-inputs-apis`;
  this skill covers only credential exposure inside those payloads.
- Session/token revocation event visibility belongs to `secod-observability-response`; this
  skill verifies procedure existence and currency evidence only.
- A failed checker or incomplete test never counts as success.

## Dependency and routing rules

Direct dependencies (from `secod/catalog.json`): `secod-core`.

Conditional routes: hosting/provider adapters owning platform secret storage, resolved at review
time from the live catalog; `secod-container-runtime`; `secod-crypto-data-protection`;
`secod-observability-response`.

If an applicable dependency, route, or adapter is missing, unresolved, malformed, or fails to
load: mark affected controls `Not verified`, name the missing owner or evidence, never invent
replacement dependencies, and never issue or imply launch readiness.

## Evidence and status rules

Statuses: `Do not ship`, `Fix before launch`, `Recommended hardening`, `Passed with evidence`,
`Not verified`.

Target-specific thresholds:

- `Passed with evidence`: complete credential/configuration inventory per environment; every
  applicable control verified with redacted, cited repository evidence plus supplied external
  evidence where the repository cannot prove the claim.
- `Fix before launch`: any live credential in a client-reachable or committed surface; raw
  bearer capabilities reaching user-authored code; privileged credentials without revocation
  path; cross-environment credential sharing; production-reachable bypasses; confirmed leaks
  lacking revocation evidence.
- `Recommended hardening`: wildcard scopes with weak justification; template drift;
  non-secret values misclassified as secrets; lower-privilege rotation gaps.
- `Not verified`: failed or partial scans, unavailable history, unevidenced rotation/revocation,
  unauthorized deployed-system probes, conflicting environment signals, inaccessible dashboards,
  snapshot-only documentation.

Never pass inferred, package-only, inaccessible, stale, contradictory, incomplete, unsupported,
or failed evidence.

## Required output

One finding per applicable control: `control_id`, `title`, `status`, `scope`, `evidence`,
`impact`, `recommended_fix`, `verification`, `limitations`, `source_refs`, `routed_skills`.
Redact every secret value in every field.

End the report with: applicability inventory (credentials, variables, and bearer flows by class
and environment); test results; requested external evidence (dashboard/API exports, rotation
records, push-protection settings, by owner); `Not verified` items with the next verification
step; launch blockers. Route overall launch readiness to `secod-ship-check`.

## Negative fixtures and tests

Run the standard-library fixture harness from `secod/`:

`python tests/insecure-fixtures/secod-secrets-config/run_fixtures.py`

It executes deterministic safe and unsafe cases for all ten controls: redacted source/log scans,
bearer exposure, excess privilege, template parity, storage/client boundaries, environment
separation, rotation/revocation evidence, production bypasses, revoke-first history response and
default credentials. Missing external evidence remains `Not verified`; unauthorized deployed
probes are not performed. Fixture success proves harness behavior only, never production state.

Safe local commands: read-only scanner runs (`gitleaks detect`-class), `rg` pattern searches
over tracked files, `git log`/history inspection, template-parity diffs. Never print matched
secret values. Never claim fixture success proves reviewed-repository or production behavior. Never run destructive,
production-changing, user-creating, payment-creating, refunding, key-rotating,
dashboard-changing, or account-changing tests without explicit authorization; this includes
default-credential probes against deployed systems and any history rewrite.

## References

- [`references/sources.md`](sources.md) — source register with review-expiry tracking for
  history-removal tooling, secret scanning, and default-credential guidance.
