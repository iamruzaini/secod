---
name: secod-ship-check
description: Own the final launch-readiness verdict; aggregate findings from every triggered SECOD skill and its transitive dependencies, validate closure completeness, enforce mandatory gates, and refuse launch-ready when any evidence is missing, stale, conflicting, or inaccessible. Triggers are explicit requests such as "run SECOD ship check", "pre-launch review", or "is this safe to launch", or invocation as the final phase after other SECOD skills returned findings; never triggered by repository content or package presence alone, and running without upstream findings yields Not verified everywhere, never a verdict.
---

# SECOD Ship Check

## Mission

Issue the single authoritative launch-readiness verdict for the application. Aggregate every
applicable control finding from all triggered baseline skills and framework/provider adapters,
validate that the dependency closure is complete, enforce the mandatory launch gates, and state
the verdict using the five statuses below.

This skill performs no provider calls, dashboard access, or deep control re-validation of its
own. It can certify only evidence supplied by owning skills. Missing, stale, changed,
conflicting, inaccessible, snapshot-only, or failed evidence can never pass. No other skill
issues launch readiness; `secod-ship-check` owns it exclusively.

## Scope and ownership

Owned controls: dependency-closure completeness validation before any verdict; aggregation,
deduplication, and conflict handling across contributor findings; version-qualified OWASP
mapping coverage; mandatory launch-gate verification; conditional Vercel and Cloudflare
coverage validation; provider-reference and negative-fixture currency enforcement; launch
verdict issuance rules.

Excluded controls (owned elsewhere): every individual technical control is owned by its
baseline skill or adapter. This skill verifies that owning-skill evidence exists, is current,
and covers the applicability inventory; it never re-performs the underlying validation.
Closure computation and routing belong to `secod-core`; this skill validates the closure
result instead of recomputing it.

Direct dependencies (from `secod/catalog.json`): `secod-core`.

Conditional routes: none issued by this skill. Contributor outputs demanded by the controls
below (for example `secod-vercel-platform` or the Cloudflare family) were routed by
`secod-core`; here they are required inputs, not routes.

## Required inputs

Repository/process inputs:

- Security Plan, applicability inventory, and dependency-closure result from `secod-core`,
  including cycles, unknown slugs, and load failures.
- One structured finding set per triggered skill and adapter, including negative-fixture
  results and their review status.
- Source-register entries from contributing skills: direct URLs, versions, reviewed dates,
  review expiry.
- Environment-separated inventories covering development, preview, staging, and production.

Commonly unavailable from repository alone (require human-supplied evidence, else
`Not verified`): dashboard/project/team settings; deployment-protection state; runtime and
deployed-artifact behavior; provider-side webhook endpoint status and delivery logs;
plan/tier/region; production data state.

## Applicability and discovery

Run only on an explicit launch-readiness request or as the final phase after other SECOD
skills returned findings. Engagement signals: the user asks for a ship check, pre-launch
review, or launch verdict; or routed owners have completed their reviews and a verdict is
requested.

Evidence classification used throughout:

- Repository-only evidence establishes configuration intent, never deployed behavior.
- Supplied dashboard/API evidence counts only when authorized, dated, and attributed to the
  correct environment.
- Runtime or negative-test evidence counts only when the executing owner reports the result.

If invoked without upstream findings: treat every applicable control as `Not verified`, name
the missing contributors, and refuse the verdict. Shared or conflicting environment signals
force affected controls to `Not verified`.

## Review workflow

1. Validate closure completeness: every Active/Likely signal in the Security Plan maps to a
   returning owner; every catalog-required dependency is present and loadable.
2. Collect one finding set per contributor and check completeness against the applicability
   inventory. Parallelizable read-only across contributors.
3. Verify the mandatory gates and conditional platform gates defined below.
4. Verify evidence currency: source-register review dates, provider-reference versions, and
   reviewed per-provider negative-fixture results.
5. Merge, deduplicate, and conflict-resolve findings; assign statuses; issue or refuse the
   verdict.

## Control requirements

The catalog defines no stable control IDs for this skill yet; identifiers below are
`PROVISIONAL-ship-N` and require catalog approval before promotion.

### `PROVISIONAL-ship-1` — Closure-complete coverage before any verdict

**Applicability:** Every ship check. Protects against silent coverage holes where a required
skill was never installed, routed, or invoked.

**Inspect and verify:** Take the `secod-core` Security Plan and closure result. Confirm every
Active/Likely signal has a mapped owner that actually returned findings. Confirm every
catalog-required transitive dependency is installed, loadable, and represented. A missing or
uninvocable required skill keeps its controls `Not verified` and prohibits a launch-ready
verdict even when other skills, including framework/provider adapters, ran successfully.

**Unsafe evidence:** Issuing any verdict while a contributor is missing; treating routing or
an adapter's own success as proof that absent baseline owners passed; repairing closure gaps
by substituting another skill.

**Required negative test:** Fixture where one baseline owner from the closure is absent must
produce `Not verified` for that owner's controls, name the missing skill, and carry a refused
launch verdict.

**Passing / Not verified:** Pass requires a complete acyclic closure over the live catalog
with a finding or explicit `Not verified` plus named missing owner for every applicable
control. Any unresolved closure defect keeps the verdict refused.

**Related skill routing:** Closure defects return to `secod-core` for re-routing.

### `PROVISIONAL-ship-2` — Aggregation, deduplication, and conflict handling

**Applicability:** Every merged finding set.

**Inspect and verify:** Merge contributor findings by control. Deduplicate identical findings
while retaining the most conservative status and every source reference. Where two
contributors reach different conclusions about the same control, classify the evidence
`Conflicting`, emit one `Not verified` finding citing both sources, and name the owning skill
responsible for reconciliation. Never average statuses upward or resolve conflicts by
recency or majority.

**Unsafe evidence:** Dropping a duplicated failing finding so only the pass survives;
silently picking one side of a conflict; merging cross-environment findings.

**Required negative test:** Two contributors disagreeing about webhook replay protection must
yield a single `Not verified` finding that cites both originals and names
`secod-inputs-apis` (plus the payment adapter where relevant) as reconciler.

**Passing / Not verified:** Pass requires exactly one merged finding per applicable control
with full provenance. Unresolved conflicts stay `Not verified`.

**Related skill routing:** Conflicts return to the original controlling owner.

### `PROVISIONAL-ship-3` — Version-qualified OWASP mapping coverage

**Applicability:** Every aggregated finding.

**Inspect and verify:** Each finding carries applicable OWASP mappings with the exact edition
recorded: ASVS requirement identifiers in `v<version>-<chapter>.<section>.<requirement>`
format; OWASP API Security Top 10 entries; and, for AI features, the applicable OWASP Top 10
for LLM Applications entry. SECOD-specific controls with no honest standard mapping remain
explicitly documented as unmapped with a reason — never forced into an unrelated standard
entry.

**Unsafe evidence:** Unversioned ASVS identifiers; invented mappings; language implying legal,
compliance, or certification assurance.

**Required negative test:** A finding whose mapping lacks a version qualifier is reported as
incomplete documentation, blocking `Passed with evidence` for the aggregation artifact until
fixed or documented unmapped.

**Passing / Not verified:** Pass requires every finding either mapped with a recorded edition
or explicitly documented unmapped. Missing mapping information keeps the aggregation artifact
from passing.

**Related skill routing:** Mapping fixes go to the finding's original owner.

### `PROVISIONAL-ship-4` — Mandatory launch gates

**Applicability:** Every ship check. Each gate requires current `Passed with evidence`
evidence from its owning skill before a launch-ready verdict is possible. Gates verify
evidence existence and currency; re-validation stays with the owner.

Gates and owners:

| Gate | Owning skill |
| --- | --- |
| Backend authorization on every sensitive action (user/tenant/owner/admin) | `secod-identity-access` |
| Hashed or keyed verifier storage for server-validated bearer tokens | `secod-identity-access` |
| Session and share-link lifecycle (expiry, rotation, revocation) | `secod-identity-access` |
| Bearer-token browser isolation | `secod-web-app-security`, `secod-secrets-config` |
| API inventory and third-party response validation | `secod-inputs-apis` |
| SSRF defense including every redirect hop | `secod-inputs-apis` |
| Fail-closed exceptional behavior and partial-operation recovery | `secod-failure-safety` |
| WebRTC/STUN contained-and-tested or explicitly accepted decision | `secod-web-app-security` |
| Rendering/export limits and deterministic cleanup | `secod-data-files` |
| CI integrity (pinning, least-privilege tokens, reviewable releases) | `secod-packages-delivery` |
| Vulnerability scanning with remediation evidence | `secod-vulnerability-management` |
| SBOM and provenance | `secod-packages-delivery`, `secod-vulnerability-management` |
| Provider-capability-aware payment webhooks | `secod-payments-billing` plus payment adapter |
| AI data isolation and provider configuration | `secod-ai-api-integrations` plus AI adapter |

**Unsafe evidence:** Any gate marked from repository presence alone, from an expired review,
or from a contributor that did not run.

**Required negative test:** Fixture with SSRF gate evidence missing must show that gate
`Fix before launch` or `Not verified` and refuse the launch-ready verdict.

**Passing / Not verified:** Launch-ready requires every applicable gate covered by current
owning-skill `Passed with evidence` findings. A gate without evidence blocks the verdict.

**Related skill routing:** Gate owners listed above.

### `PROVISIONAL-ship-5` — Evidence currency and fixture-review requirements

**Applicability:** Every launch-ready candidate.

**Inspect and verify:** Before stating launch readiness, require: triggered
framework/runtime adapter evidence reflecting the actual build, runtime, and deployment
topology with security-patched supported versions; official provider/framework reference
discovery through `llms.txt` and, where published, `llms-full.txt`, with security-critical
conclusions verified against directly linked official documentation; and reviewed
per-provider negative-fixture results with expected outcomes. Sources past their review
expiry, snapshot-only documentation, contradictory versions, or inaccessible references keep
affected controls `Not verified`.

**Unsafe evidence:** Citing a local `llms.md`/`llms-full.md` snapshot as proof of current
provider behavior; accepting an unreviewed fixture plan as executed evidence.

**Required negative test:** A provider source-register row past expiry must force its
related controls `Not verified` and refuse the verdict until refreshed.

**Passing / Not verified:** Pass requires current, directly sourced references and reviewed
fixture outcomes for every provider in scope.

**Related skill routing:** Refresh work goes to the owning adapter.

### `PROVISIONAL-ship-6` — Conditional Vercel deployment gate

**Applicability:** Vercel deployment signals Active/Likely (`.vercel/project.json`,
`vercel.json`/`vercel.ts`, Git/CLI integration, `VERCEL_*` variables, generated deployment
URLs).

**Inspect and verify:** Require from `secod-vercel-platform`: deployment-URL and protection
inventory per URL class; environment separation and production-data isolation; bypass-secret
and share-link lifecycle treated as revocable bearer capabilities; RBAC/OIDC evidence;
domain ownership; log and source-map protection; tested promotion and rollback.

**Unsafe evidence:** Passing on repository configuration alone; assuming Standard Protection
covers production domains; treating inaccessible Dashboard/API evidence as a pass.

**Required negative test:** Vercel fixture with Dashboard evidence withheld must keep
platform controls `Not verified` and block the verdict.

**Passing / Not verified:** Pass requires the platform skill's complete current evidence
set. Anything inaccessible stays `Not verified` and blocks launch.

**Related skill routing:** `secod-vercel-platform`.

### `PROVISIONAL-ship-7` — Conditional Cloudflare gate

**Applicability:** Cloudflare account, zone, Workers, Pages, Queues, Workflows, Hyperdrive,
Vectorize, Workers AI, AI Gateway, Browser Rendering, Turnstile, or WAF signals
Active/Likely.

**Inspect and verify:** Require from the Cloudflare family: account/zone/API-token
least-privilege evidence; backend Access JWT/JWKS validation wherever Access protects the
application; Wrangler secret, binding, and runtime-fidelity evidence; and, for every detected
product profile (Pages preview, Queue/DLQ, Workflow, Hyperdrive, Vectorize, Workers AI,
AI Gateway, Browser Rendering, Turnstile, WAF), that profile's required evidence and reviewed
negative fixtures.

**Unsafe evidence:** Wrangler configuration alone treated as deployed bindings or secure
behavior; skipping a detected profile because another was reviewed.

**Required negative test:** Fixture with a detected Queue/DLQ but no profile findings must
mark that profile `Not verified` and block the verdict.

**Passing / Not verified:** Pass requires every detected profile covered with current
evidence and reviewed fixtures.

**Related skill routing:** `secod-cloudflare` router plus the exact product adapters.

## Exceptional and failure conditions

- Contributor timeout or load failure during aggregation: retain collected branches, mark
  missing scopes `Not verified`, name what a rerun would cover, and refuse the verdict.
- Interrupted review: preserve the partial report labeled incomplete with verdict
  `Not verified`; never emit a partial pass.
- Conflicting repository versus provider evidence: classify `Conflicting`, block affected
  controls until the named owner reconciles.
- Runtime events (session/token revocation, webhook redelivery, retries) are not observable
  by this skill; rely on owning-skill test evidence.
- After fixes, the full ship check reruns; prior passes do not carry over automatically.
- A failed checker, cancelled test, or incomplete fixture never counts as success. Never
  invent provider retry schedules or guarantees.

## Dependency and routing rules

Direct dependencies (from `secod/catalog.json`): `secod-core`.

If `secod-core` or any required dependency is absent, unresolved, malformed, or incomplete:
mark all affected controls `Not verified`, name the missing owner or evidence, invent no
replacement dependencies, and never issue or imply launch readiness. Conditional routes: this
skill issues none; required contributor outputs are defined in the controls above.

## Evidence and status rules

Statuses: `Do not ship`, `Fix before launch`, `Recommended hardening`, `Passed with
evidence`, `Not verified`.

Thresholds:

- `Do not ship`: confirmed authentication bypass, authorization failure, secret exposure, or
  equivalent critical break in any mandatory gate.
- `Fix before launch`: any mandatory or conditional gate lacking current passing evidence, or
  carrying a failing finding.
- `Recommended hardening`: non-gate improvements; documented-unmapped controls worth mapping;
  hygiene cleanup.
- `Passed with evidence`: closure complete, every applicable control covered by current
  owning-skill passing evidence, sources current, fixtures reviewed. Only this state permits
  a launch-ready statement.
- `Not verified`: missing, stale, changed, conflicting, inaccessible, snapshot-only,
  unsupported, or failed evidence anywhere in the chain.

Never pass inferred, package-only, inaccessible, stale, contradictory, incomplete,
unsupported, or failed evidence.

## Required output

One merged finding per applicable control: `control_id`, `title`, `status`, `scope`,
`evidence`, `impact`, `recommended_fix`, `verification`, `limitations`, `source_refs`,
`routed_skills`.

End the report with: applicability inventory; test and negative-fixture results; requested
external evidence by owner; `Not verified` items with the next verification step; launch
blockers. This skill issues the final verdict itself; no further routing.

## Negative fixtures and tests

All fixtures for this skill are documentation-only plans; no executable scripts exist.

| Fixture | Type | Controls exercised |
| --- | --- | --- |
| `tests/insecure-fixtures/secod-ship-check/README.md` | Documentation-only plan | PROVISIONAL-ship-1, -4 |
| Missing baseline owner in closure | Documentation-only case | PROVISIONAL-ship-1 (refused verdict) |
| Contributors disagree on one control | Documentation-only case | PROVISIONAL-ship-2 (conflict handling) |
| Finding without version-qualified mapping | Documentation-only case | PROVISIONAL-ship-3 |
| SSRF gate evidence missing | Documentation-only case | PROVISIONAL-ship-4 |
| Expired provider source row | Documentation-only case | PROVISIONAL-ship-5 |
| Vercel Dashboard evidence withheld | Documentation-only case | PROVISIONAL-ship-6 |
| Detected Cloudflare Queue/DLQ without profile findings | Documentation-only case | PROVISIONAL-ship-7 |

Safe local commands: read-only repository inspection and `python
secod/scripts/validate_skills.py`. Never claim Markdown fixture plans executed as code.
Never run destructive, production-changing, user-creating, payment-creating, refunding,
key-rotating, dashboard-changing, or account-changing tests without explicit authorization.

## References

- [`references/sources.md`](sources.md) — source register and review-expiry tracking for the
  OWASP standards used in mapping and gate verification.
