---
name: secod-packages-delivery
description: Review dependency supply chain, CI/CD pipelines and release/delivery integrity for reproducibility, least privilege, reviewability and rollback. Triggers include lockfiles, package manifests, .npmrc/registry config, install scripts, GitHub Actions/workflow YAML, deployment workflows, artifact/container publishing, provenance/attestation verification, signed tags/releases and rollback evidence; package presence alone is Candidate.
---

# Packages Delivery Security

## Mission

Make dependencies, CI/CD and releases reproducible, least-privileged, reviewable and
rollback-capable: frozen lockfiles with maturity/install-script policy; advisory monitoring
with supported-version policy and patch/upgrade evidence; trusted registries and namespace
ownership; minimal CI tokens; full-SHA Action pins; safe fork and `pull_request_target`
handling; hermetic builds where practical; protected environments and IaC review; immutable
artifacts with candidate promotion; verified provenance consumption; signed releases with
checksums; tested rollback and runtime-test fidelity.

Repository-only review cannot prove registry/publisher state, advisory-feed currency, CI
runtime behavior, artifact-registry contents, environment-protection settings or that any
control passed without the listed evidence. `secod-ship-check` owns final launch readiness;
this skill never issues it.

## Scope and ownership

Owned controls: lockfile freezing and install reproducibility; dependency maturity and
supported-version policy; install-script and registry-trust policy (dependency confusion);
package namespace ownership verification; minimal CI tokens; full-SHA Action pinning; fork and
`pull_request_target` safety; build isolation/hermetic inputs; protected environments and IaC
review; immutable/content-addressed artifacts and candidate promotion; provenance/attestation
consumption; signed tags/releases with checksums; deployment rollback, runtime-test fidelity
and reproducible release verification; official reference discovery via `llms.txt`/
`llms-full.txt`.

Excluded controls (owned elsewhere): scanning, SBOM, advisory triage and remediation SLAs
(`secod-vulnerability-management`); secret values, rotation, history (`secod-secrets-config`);
container internals/runtime hardening (`secod-container-runtime`); deployed-platform
identity/networking (cloud families, Pages/Workers adapters); code-path authorization
(`secod-identity-access`); launch verdicts (`secod-ship-check`).

Direct dependencies (from `secod/catalog.json`): `secod-core`.

Conditional routes: none owned. Consumers route INTO this skill: `secod-cloudflare-pages`
(build identity/install-script policy and image digest/provenance expectations).

## Required inputs

Repository inputs: manifests and committed lockfiles for every workspace; `.npmrc`,
`.yarnrc.yml`, `pnpm-workspace.yaml`; CI workflows (`.github/workflows/*.yml`) including
reusable workflows and checked-out actions; Dockerfiles/base-image refs; release scripts;
IaC files; git tag/signature state (`git tag -v`). Environment-variable **names** only.

Commonly unavailable repository-only (request as supplied evidence, else `Not verified`):
CI logs proving token scope applied; protected-environment reviewer settings; artifact-registry
immutability policy; registry provenance/attestation records; signing-service key state;
advisory-feed status per dependency; rollback drill logs. Human-supplied: read-only exports of
Actions permissions/environments, registry settings, update-bot results, latest attestation
bundle.

## Applicability and discovery

Always applicable to any project that ships software.

Signal groups:

- Package/SDK: manifests, lockfiles, vendored deps, monorepo workspaces.
- Environment variables (names only): `NODE_AUTH_TOKEN`, `GITHUB_TOKEN` scope overrides,
  registry/publish credentials referenced by workflows.
- Routes/webhooks: none owned; CI triggers/deploy events are delivery signals, not app routes.
- Configuration: workflow YAML, action.yml, `.npmrc`/yarn config, Dependabot/Renovate config,
  Dockerfile, release/tag scripts, IaC pipelines.
- Deployment/provider evidence: published packages/images, registry attestations, deployment
  logs, environment-protection exports.

Classification:

- `Candidate`: lockfile absent but manifest present; example workflow only; dormant release
  script; weak signal alone.
- `Likely`: workflows/config exist and correlate with use, but CI runtime, registry or
  environment state is unverified.
- `Active`: repository behavior correlates with CI logs, registry evidence, attestations,
  environment-protection exports or provider evidence.

Maintain separate inventories for development, preview, staging and production pipelines and
registries. Conflicting signals (shared publish token across environments, prod/preview on one
mutable tag) force affected controls to `Not verified`.

## Review workflow

1. Inventory environments and trust boundaries: every pipeline that can publish/deploy, its
   trigger source (push/PR/fork/schedule/manual), target environment and registry. Read-only;
   parallelizable per workflow file.
2. Correlate active flows: which workflows build, test, publish, deploy; which packages/images
   ship; which tags are release channels. Parallelizable after step 1.
3. Verify applicable controls against repository plus supplied evidence.
4. Run safe negative tests: local/read-only only (lockfile-vs-manifest diff, pin-format grep,
   permissions parse). Never push tags, publish packages, mutate registries or re-run
   workflows.
5. Classify evidence, emit findings, route findings, hand applicability inventory to
   `secod-ship-check`.

Steps 1–2 parallelizable when strictly read-only; steps 3–5 sequential.

## Control requirements

Catalog defines no stable control IDs for this skill yet; identifiers below are
`PROVISIONAL-packages-N` and require catalog approval before promotion.

### `PROVISIONAL-packages-1` — Frozen lockfiles and reproducible installs

**Applicability:** Any JS/TS, Python, Go, Rust or other manifest+lockfile ecosystem shipping
from this repo. Protects against upstream drift silently changing what builds and ships.

**Inspect and verify:** Lockfile committed and current vs manifest (run frozen install in a
scratch copy: `npm ci`, `pnpm install --frozen-lockfile`, `yarn --immutable`, pinned/hash
requirements file, `go mod verify`). No `^`/`~`-only resolution at build time; lockfile updated
through reviewed commits, not ad-hoc regeneration during release. CI uses the frozen mode,
never bare `install`/`update`. Record lockfile path, hash and redacted command output.

**Unsafe evidence:** Missing/uncommitted/stale lockfile; CI running non-frozen install;
manifest edited without lockfile update; different lockfiles per pipeline stage.

**Required negative test:** Locally modify a manifest version range and confirm frozen-install
command fails rather than resolving anew. Documentation-only execution acceptable when no
scratch checkout exists.

**Passing / Not verified:** Pass requires current lockfile + frozen CI install evidence +
negative-test outcome. Missing lockfile, untestable CI claim or conflicting per-stage
installers is `Not verified`.

**Related skill routing:** Scanner/advisory depth stays with `secod-vulnerability-management`.

### `PROVISIONAL-packages-2` — Dependency maturity, supported-version policy and advisory monitoring

**Applicability:** Every direct and transitive runtime dependency. Protects against shipping
unmaintained or known-vulnerable versions without an upgrade path.

**Inspect and verify:** Supported-version policy documented (supported majors/lines, upgrade
cadence); monitoring evidenced — Dependabot/Renovate config present with recent alerts/PRs;
framework/runtime versions within vendor support windows (check official docs via `llms.txt`
discovery per `PROVISIONAL-packages-12`). Patch/upgrade evidence: recent security upgrades
merged or dated exception. Advisory triage depth routes to `secod-vulnerability-management`;
here require only policy + monitoring + upgrade evidence.

**Unsafe evidence:** No monitoring config; EOL runtime/framework major; no upgrade activity
with no exception record; policy absent.

**Required negative test:** Pick one pinned dependency with a known past advisory; confirm the
repo shows the fix commit or an accepted-risk record. If neither, control fails.

**Passing / Not verified:** Pass needs policy + monitoring evidence + upgrade-or-exception
evidence. Package presence proves nothing; inaccessible alert state or stale feed is
`Not verified`.

**Related skill routing:** `secod-vulnerability-management` owns scan/triage/remediation SLA.

### `PROVISIONAL-packages-3` — Install-script policy and registry trust (anti-confusion)

**Applicability:** Ecosystems with lifecycle install scripts and scoped registries. Protects
against postinstall code execution and dependency-confusion/name-squatting substitution.

**Inspect and verify:** Registry config pinned (project `.npmrc`/`.yarnrc.yml` sets exact
registry URLs; internal scopes mapped to private registry; no reliance on developer-default
registry in CI). Namespace ownership confirmed for first-party names (publisher/org match on
public registry page or registry API export). Install-script policy explicit: allowlist of
packages permitted to run scripts (`pnpm.onlyBuiltDependencies`, documented `ignore-scripts`
trade-off) or equivalent transitive-script review. No wildcard proxy resolving unknown names
externally before internal.

**Unsafe evidence:** Default registry with no scope mapping while private names could resolve
publicly; scripts unrestricted in a fresh clone; namespace ownership unconfirmed for published
first-party names.

**Required negative test:** From a clean checkout, attempt resolution of an internal-only name
and confirm it cannot silently fetch a public squatter (read-only: `npm view <internal-name>`
must fail or return your own publisher).

**Passing / Not verified:** Pass requires pinned registry config + ownership confirmation +
script-policy evidence. Registry-side settings unavailable is `Not verified`.

**Related skill routing:** Publishing credentials/secrets values route to
`secod-secrets-config`.

### `PROVISIONAL-packages-4` — Minimal CI tokens and permissions

**Applicability:** Every workflow and pipeline. Protects against compromised job reading repo
or cloud credentials beyond need.

**Inspect and verify:** Top-level `permissions: {}` (or `contents: read`) per workflow;
per-job elevation only where required; token never exported into artifacts/logs; cloud auth
via short-lived OIDC (`id-token: write` + role assumption) instead of stored long-lived keys;
publish/deploy tokens scoped to one environment/registry, referenced not echoed.

**Unsafe evidence:** Workflow-wide `write-all`/missing permissions block; long-lived cloud
keys in env; token printed in logs or passed into build context.

**Required negative test:** Parse workflow YAML locally: assert top-level permissions deny-all
and list every elevated job with justification. Forked-PR runs must show no secret access
(see `PROVISIONAL-packages-5`).

**Passing / Not verified:** Pass requires parsed permissions for every active workflow + OIDC
or minimal-token evidence for deploys. Runtime enforcement (what the token could actually do)
unverifiable from YAML alone: mark limitation; without supplied CI-export evidence status is
`Not verified`.

**Related skill routing:** Secret storage hygiene: `secod-secrets-config`. Cloud role
definitions: owning cloud adapter.

### `PROVISIONAL-packages-5` — Full-SHA Action pinning and fork/`pull_request_target` safety

**Applicability:** Every `uses:` reference to third-party actions and every workflow triggered
by forks or `pull_request_target`. Protects against mutable-tag action replacement and
privileged-context abuse.

**Inspect and verify:** Third-party actions pinned to full 40-hex commit SHA (not tag,
branch or short SHA); first-party/local actions may use relative refs; each SHA target
reviewed once with review date. `pull_request_target`, `workflow_run` or privileged checkout
of PR head must not execute PR-supplied code with secrets/write access — split: untrusted PR
code runs restricted, merge then trusted pipeline. Fork PRs get no secrets.

**Unsafe evidence:** Tag-pinned third-party actions (`@v4`) without compensating digest check;
PR head code executing under `pull_request_target` with secrets; auto-merge of untrusted
workflows into privileged runs.

**Required negative test:** Local grep: every third-party `uses:` matches full-SHA pattern;
list exceptions with justification. Craft a hypothetical privileged-PR flow description and
confirm workflow graph denies it (static analysis, no execution).

**Passing / Not verified:** Pass = all third-party pins full-SHA + no unsafe
`pull_request_target` data flow. Unreviewed SHAs or ambiguous flow is `Not verified`.**Related skill routing:** Injection inside workflow scripts: `secod-runtime-execution`.

### `PROVISIONAL-packages-6` — Build isolation and hermetic inputs

**Applicability:** Build/publish jobs producing shippable artifacts. Protects against
network-fetched or cache-poisoned build inputs altering the artifact.

**Inspect and verify:** Builds fetch dependencies only from pinned registries/lockfile; no
`curl | sh`, no unpinned remote scripts/binaries at build time; base images pinned by digest;
caches keyed to lockfile hash, isolated per branch; least-privilege build containers;
reproducible-build practices where practical (fixed locale/TZ, no embedded timestamps,
deterministic ordering).

**Unsafe evidence:** Network script fetch in Dockerfile/workflow; `latest` base image; shared
cache across branches carrying compiled output.

**Required negative test:** Static review of Dockerfile + workflow steps listing every
network fetch with its pin. Any unpinned fetch is a finding.

**Passing / Not verified:** Pass requires all build-time fetches pinned + cache isolation
evidence. "Practical" reproducibility gaps documented as limitations, not failures, when
inputs still pinned. Unverifiable runner behavior is `Not verified`.

**Related skill routing:** Container runtime details: `secod-container-runtime`.

### `PROVISIONAL-packages-7` — Protected environments, gated deployments and IaC review

**Applicability:** Pipelines deploying to staging/production; IaC-managed infrastructure.
Protects against unauthorized or accidental production change.

**Inspect and verify:** Production deploys gated by protected environment (required
reviewers, deployment-branch allowlist) — request dashboard/export evidence; branch protection
blocks direct release-branch pushes; IaC changes reviewed with plan output (`terraform plan`
attached to PR, apply only from approved pipeline, restricted state backend); no manual
console/kubectl mutation bypassing pipeline.

**Unsafe evidence:** Anyone-with-write can deploy prod; apply runs from unreviewed plan; state
bucket publicly writable.

**Required negative test:** Attempt (read-only inspection, not execution) to trace a path from
an ordinary feature-branch push to production deploy; expected result: blocked without review
approval. Document the trace.

**Passing / Not verified:** Pass requires environment-protection export + branch-protection
evidence + IaC plan-review evidence. Protection settings inaccessible is `Not verified`.**Related skill routing:** Platform-specific deployment surfaces: owning cloud/Pages adapter.

### `PROVISIONAL-packages-8` — Immutable artifacts and candidate promotion

**Applicability:** Published images/packages/bundles promoted between environments. Protects
against same-tag-different-bytes drift and unreviewed promotion.

**Inspect and verify:** Artifacts content-addressed (digest, immutable tag scheme, published
checksums); promotion moves by digest/reference, never rebuilds "the same" version;
candidate→staging→production promotion recorded (approver, digest); `latest` never a
production deploy reference.

**Unsafe evidence:** Prod deploy referencing `latest`; promotion re-running build instead of
reusing digest; no checksum publication.

**Required negative test:** Trace one released version end-to-end: manifest version → build
log → digest → deployed ref. Mismatch or missing link is a finding.

**Passing / Not verified:** Pass requires digest-stable chain for at least the latest release.
Registry immutability setting unverifiable is `Not verified`.

**Related skill routing:** Registry/platform specifics: owning cloud adapter.

### `PROVISIONAL-packages-9` — Provenance/attestation consumption

**Applicability:** Consumed third-party artifacts with provenance offers, and own artifacts
where attestations generated. Protects against consuming artifacts without verifiable origin.

**Inspect and verify:** Own builds: attestations generated (SLSA-style, e.g. GitHub artifact
attestations) AND consumers VERIFY them — verification step in the deploy pipeline (`gh
attestation verify`, cosign/Sigstore, registry policy), not generation alone. Consumed critical
dependencies/actions: provenance checked where published. Verification failure blocks deploy
(fail-closed wiring visible in pipeline).

**Unsafe evidence:** Attestation generated but never verified anywhere; verification step with
`|| true` semantics; no policy on consumed-artifact trust.

**Required negative test:** Locate the verify call in the deploy workflow; confirm failure
path halts deployment (reads as `set -e`, native action failure propagation, or explicit exit).

**Passing / Not verified:** Pass requires generation + enforced verification evidence.
Attestation records inaccessible is `Not verified`.

**Related skill routing:** Key/signature material handling: `secod-crypto-data-protection`,
`secod-secrets-config`.

### `PROVISIONAL-packages-10` — Signed tags and releases with checksums

**Applicability:** Repos publishing releases/tags. Protects release-channel integrity.

**Inspect and verify:** Release tags signed or covered by verified workflow-run provenance;
checksum files published and themselves signed/attested; release notes tie commit SHA +
artifact digest; signing material held in protected secret or key service with a named
rotation owner (values never in repo).

**Unsafe evidence:** Unsigned tags with no provenance alternative; checksums absent or
unsigned; signing key committed or shared across environments.

**Required negative test:** Verify latest release locally: `git tag -v <tag>` or attestation
check + checksum recomputation on a downloaded artifact. Never upload/publish anything.

**Passing / Not verified:** Pass requires verifiable signature/provenance + checksum chain on
the latest release. Signing-service state inaccessible is `Not verified`.

**Related skill routing:** `secod-crypto-data-protection` for algorithm/key choices.

### `PROVISIONAL-packages-11` — Rollback capability, runtime-test fidelity and release verification

**Applicability:** Every deployable artifact. Protects against unrecoverable bad releases and
tests passing in an environment unlike production.

**Inspect and verify:** Documented, exercised rollback procedure per artifact type
(previous-digest redeploy, package deprecation/repoint; migration down-paths owned by data
skills); last drill or real rollback recorded with date/outcome; runtime tests run against
production-like build (same build output and runtime target, not dev-mode bundling); release
verification reproducible — rebuilding the tagged commit matches the published artifact or has
a documented delta.

**Unsafe evidence:** No rollback path; tests only ever run in dev-mode bundling; release
cannot be rebuilt from source.

**Required negative test:** Dry-run trace: given the previous release digest, name the exact
commands/settings that restore it. Missing answer is a finding.

**Passing / Not verified:** Pass requires documented rollback + fidelity evidence +
reproducible-release check. Drill history unavailable is `Not verified`.

**Related skill routing:** Data migration safety: `secod-data-files`, owning data adapters.

### `PROVISIONAL-packages-12` — Official reference discovery and drift control

**Applicability:** Every security-critical conclusion about a dependency/framework/provider
version. Protects against snapshot-rot and invented defaults.

**Inspect and verify:** Use official `llms.txt`/`llms-full.txt` indexes for discovery; verify
each retained security-critical claim against the directly linked official primary doc
(vendor docs, standards bodies, government guidance); record in `references/sources.md` with
review date and expiry/refresh trigger; claims without live-source support stay out of
findings or downgrade the control to `Not verified`. Discovery mechanics owned by
`secod-core`; this skill owns delivery-domain source freshness.

**Unsafe evidence:** Conclusions from memory, blog posts, training knowledge or stale
snapshots; expired register entries still cited.

**Required negative test:** Pick one finding's decisive claim; locate its primary-source line
in the registered URL. Unlocatable claim forces `Not verified`.

**Passing / Not verified:** Pass requires a live registered official source per decisive
claim used in findings.

## Exceptional and failure conditions

Fail closed in every case; a failed checker or incomplete test never counts as success.

- Timeout/tool failure: frozen-install check, registry lookup or attestation verify errors —
  affected control `Not verified` with failing command named. No retries against production
  systems.
- Partial operations: interrupted build/promotion leaves orphan artifacts — require cleanup/
  reconciliation evidence (digest ledger or registry listing) before any pass.
- Retry/cancellation: cancelled mid-promotion deploy must leave prior release serving;
  promotion must be transactional (switch-once-to-digest) or control is `Not verified`.
- Revocation: rotated signing key or revoked token mid-release — pipeline fails closed;
  post-revocation signatures must not verify against old key material.
- Webhooks: not owned here; duplicate/replay/redelivery of deploy-trigger webhooks route to
  `secod-abuse-limits` and the owning integration skill.
- Never assume vendor retry schedules, feed guarantees or uptime promises without a registered
  official source stating them.

## Dependency and routing rules

Direct dependencies copied exactly from `secod/catalog.json`: `secod-core`.

If `secod-core` is missing, malformed or cannot be invoked: mark every affected control
`Not verified`, name `secod-core` as the missing owner, never substitute another skill, never
issue launch readiness.

Conditional routes: none outbound. Inbound consumer (`secod-cloudflare-pages`) relies on this
skill's findings for build identity, install-script
policy and artifact integrity; report findings precisely so they can consume them.

## Evidence and status rules

Statuses only: `Do not ship`, `Fix before launch`, `Recommended hardening`,
`Passed with evidence`, `Not verified`.

- `Do not ship`: actively malicious or trivially exploitable delivery path (unpinned
  third-party action with secrets access; PR-head code executing privileged; signing key in
  repo).
- `Fix before launch`: requirement unmet with concrete insecure evidence (no lockfile, no
  permissions block, unsigned releases feeding production, no rollback path).
- `Recommended hardening`: minimum met but weak practice (short-SHA pins with digest
  compensation, manual promotion steps, undocumented drill history).
- `Passed with evidence`: every Inspect-and-verify item satisfied with cited repository or
  supplied-provider evidence plus required negative test.
- `Not verified`: evidence missing, stale, conflicting, inaccessible, unsupported, or test
  failed/incomplete.

Never pass from package presence, inferred config, documentation snapshot alone, or failed
tooling.

## Required output

One finding per applicable control:

`control_id`, `title`, `status`, `scope` (environments/artifacts covered), `evidence`
(paths, lines, redacted command outputs), `impact`, `recommended_fix`, `verification` (how to
re-check), `limitations`, `source_refs` (sources.md IDs), `routed_skills`.

End of report includes:

- Applicability inventory: pipelines, artifacts, registries, environments classified
  Candidate/Likely/Active.
- Test results: each executed negative test with outcome; each skipped test named.
- Requested external evidence: exact exports needed (environment protection, registry
  immutability, CI logs, attestation bundles).
- `Not verified` items with the missing evidence named.
- Launch blockers list.

Route overall launch readiness verdict to `secod-ship-check`; this skill contributes findings
only.

## Negative fixtures and tests

Run executable, provider-neutral fixtures from `secod/`:

`python tests/insecure-fixtures/secod-packages-delivery/run_fixtures.py`

| Fixture | Location | Controls exercised |
| --- | --- | --- |
| Trigger case | `secod/tests/trigger-cases/secod-packages-delivery.md` | applicability gate |
| Executable fixture harness | `secod/tests/insecure-fixtures/secod-packages-delivery/` | all 12 provisional controls |
| Expected result | `secod/tests/expected-results/secod-packages-delivery.md` | exact statuses and runner JSON |

Harness reproduces secure and unsafe patterns, source expiry, failed negative tests and missing
repository/provider evidence. Its clean case is synthetic contract coverage only. Real controls
remain `Not verified` until review-time repository and external evidence satisfy every required
item; fixture success never pre-passes a project or production environment.

Preserve runner JSON as local test evidence. Safe local review commands only:
frozen-install dry runs, YAML/grep parsing, `git tag -v`, checksum recomputation, `npm view`.
Never run destructive, production-changing, publish-capable, tag-pushing or account-changing
tests without explicit authorization.

## References

- [`references/sources.md`](references/sources.md) — source register with IDs, URLs, owners,
  review dates, expiry and control mappings.
