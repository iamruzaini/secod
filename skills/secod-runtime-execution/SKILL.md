---
name: secod-runtime-execution
description: Review server-side execution boundaries for OS command injection, argument injection and server-side template injection when code spawns processes, evaluates dynamic input or renders templates — trigger on exec/spawn/system/shell usage, subprocess wrappers, eval/new Function/exec/pickle.loads-class evaluation, template engines rendering user-influenced source, LDAP/XPath/XQuery query construction, or job/CLI tooling invoked from request paths. Package presence alone is Candidate, never evidence of exposure or safety.
---

# Runtime Execution Security

## Mission

Prevent OS command injection, argument injection and server-side template injection at every
server-side execution boundary: avoid shells, use safe argv-array process APIs and run
spawned work in least-privilege contexts.

Repository-only review can prove how code constructs commands, arguments, evaluated code and
template source. It cannot prove the deployed runtime identity, working directory, environment
scrubbing, egress policy, or host-level sandboxing of spawned processes without deployment or
provider evidence. `secod-ship-check` owns final launch readiness; this skill never issues it.

## Scope and ownership

Owned controls:

- Avoiding direct OS commands in favor of library/platform APIs with hardcoded executables.
- Argv-array process invocation with no shell string parsing.
- Command allowlists and positive per-argument validation.
- End-of-options delimiter handling against option/argument injection.
- Least-privilege execution context for spawned processes.
- Prohibition of dynamic code evaluation on untrusted data.
- Server-side template injection prevention and sandbox hardening.
- LDAP filter and XPath/XQuery injection escaping.

Excluded controls and adjacent owners:

- Inventorying and authorizing API boundaries that feed these sinks: `secod-inputs-apis`
  (it inventories command/template execution boundaries and routes them here).
- HTTP-layer request validation and canonicalization: `secod-inputs-apis`.
- Container/Kubernetes privilege isolation of the worker itself: `secod-container-runtime`.
- Secret storage and environment hygiene at rest: `secod-secrets-config`.
- General timeout/retry/cleanup policy beyond spawned-process behavior:
  `secod-failure-safety`.
- File content validation before a tool processes uploaded files: `secod-data-files`.
- Application-wide resource limits: `secod-abuse-limits`.
- Launch verdict: `secod-ship-check`.

Direct dependencies (copied exactly from `secod/catalog.json`): none.

Conditional routes: none declared in `secod/catalog.json`.

## Required inputs

- Repository code, configuration, tests, CI definitions and deployment manifests touching
  process spawning, dynamic evaluation, template rendering, LDAP/XPath/XQuery construction.
- Language/runtime versions and installed packages relevant to discovered sinks.
- Deployment/runtime evidence for each environment: service identity running workers,
  effective working directory, child-process environment, filesystem permissions, network
  egress rules. **Commonly unavailable repository-only** — label as such and mark affected
  controls **Not verified** until supplied by the operator.
- Human-supplied evidence when required: confirmation of which environments run each job,
  provider/host sandbox settings (seccomp, AppArmor, container user) not visible in the repo.

## Applicability and discovery

Inventory separately for development, preview, staging and production. Conflicting or shared
environment signals across those environments are **Not verified**.

Signals grouped:

- Package/SDK: image/video/document/PDF processing libraries (`sharp`, ImageMagick bindings,
  FFmpeg wrappers, LibreOffice/pandoc wrappers), git clients, archive tools, CLI SDKs.
  Presence alone is only a weak signal.
- Environment variables: tool paths, `PATH` overrides, `TMPDIR`, shell preference variables,
  feature flags enabling conversion jobs.
- Routes/webhooks/job queues: endpoints or workers accepting filenames, URLs, expressions,
  formulas, templates, spreadsheet data, import/export jobs that flow toward an execution sink.
- Configuration: template engine setup (autoescape off, sandbox disabled), task runners
  (cron, queue consumers), build hooks executing at runtime, `shell:` options set truthy.
- Deployment/provider evidence: worker service accounts, egress policies, host sandboxes,
  Dashboard/API settings for managed runtimes.

Classification:

- `Candidate`: execution-related package, example variable, dormant file or other weak signal
  only; no reachable invocation found.
- `Likely`: reachable code/configuration exists, but deployed runtime identity, environment,
  or isolation state is unverified.
- `Active`: repository behavior correlates with deployed, runtime, Dashboard, Management API
  or operator-supplied provider evidence confirming the boundary runs outside development.

## Review workflow

1. Inventory environments and trust boundaries: enumerate every process spawn, dynamic
   evaluation site, template render call, LDAP/XPath/XQuery query builder; map each to its
   environments (dev/preview/staging/production) and to the trust boundary whose data reaches it.
2. Correlate active features and flows: trace user-, webhook-, file- and queue-controlled data
   from entry points to each sink; discard unreachable `Candidate` sites after documenting them.
3. Verify applicable controls below against concrete code paths and configuration.
4. Run safe negative tests locally where fixtures permit; never mutate production, provider
   dashboards, accounts, keys, or data.
5. Classify evidence per control, record findings, route shared-surface findings to their
   owning skills.

Steps 1 and 2 are parallelizable across independent codebases/environments because they read
state only. Steps 3–5 depend on earlier outputs.

## Control requirements

No stable catalog control IDs exist for this skill; provisional IDs below require catalog
approval before promotion.

### `PROVISIONAL-runtime-execution-1` — Prefer library APIs over direct OS commands

**Applicability:** Any server-side code invoking OS commands. Protected property: user input
never selects which program runs or what it does.

**Inspect and verify:** Grep for `exec`/`spawn`/`system`/`popen`/`Process.Start`/
`Runtime.exec`/`os.system` families and wrapper modules. For each call site, confirm a
built-in library or platform API (image codec, PDF library, native module) could replace the
subprocess, and the executable plus required flags are hardcoded constants. Secure decision:
library API preferred; if subprocess unavoidable, control passes to `-2`.

**Unsafe evidence:** User-controlled values choosing the executable, subcommand, or flags;
string-built commands.

**Required negative test:** Feed a crafted operand (`; id`, `` `id` ``, `$(id)`,
newline-delimited second command) through the feature path in a local fixture; expected secure
result: value treated as inert data or rejected by validation, no extra command executed.

**Passing / Not verified:** Passed requires all call sites inventoried with hardcoded
executables or replaced by library APIs, plus the negative test. Missing any call-site audit,
stale or conflicting inventory is **Not verified**.

**Related skill routing:** Boundary discovery and authorization upstream → `secod-inputs-apis`.

### `PROVISIONAL-runtime-execution-2` — Argv-array invocation without shell parsing

**Applicability:** Every unavoidable subprocess. Protected property: no string is parsed by a
shell interpreter.

**Inspect and verify:** Confirm structured argv APIs with shell disabled: Java
`ProcessBuilder` argument list, Node `child_process.execFile`/`spawn` with `shell: false`,
.NET `ProcessStartInfo` argument list, Python `subprocess.run` sequence form with default
`shell=False`. Never concatenate user input into a command string. OS-specific escaping
(`escapeshellarg()` class) only where parameterization is impossible, documented as not
preventing argument injection. Fully qualified executable paths preferred over `PATH` search.
On Windows treat `.bat`/`.cmd` targets as shell-parsed regardless of API.

**Unsafe evidence:** Template-literal or `+`-concatenated command strings; `exec()`;
`shell: true`; `system()`/`passthru()` with interpolated input; batch-file targets with
untrusted arguments.

**Required negative test:** Local fixture passing a metacharacter payload through the argv
path; expected result: payload arrives as one literal argument, no shell interpretation.

**Passing / Not verified:** Passed requires every spawn site using argv arrays with shell
disabled and no concatenation, evidenced by code inspection plus negative test. Unverifiable
runtime shell configuration (wrappers, aliases) is **Not verified**.

**Related skill routing:** Deeper input validation at HTTP layer → `secod-inputs-apis`.

### `PROVISIONAL-runtime-execution-3` — Command allowlists and positive argument validation

**Applicability:** Every subprocess accepting external influence. Protected property: only
allowlisted commands with positively validated arguments execute.

**Inspect and verify:** Enumerate permitted executables into an explicit allowlist; validate
every externally influenced argument against anchored allowlist regexes excluding shell
metacharacters and whitespace, with bounded length. Confirm validators reject rather than
sanitize. Check filename-derived operands against extension/charset allowlists.

**Unsafe evidence:** Free-form strings flowing into argv; denylist-only filtering; unbounded
argument length; validators applied client-side only.

**Required negative test:** Submit rejected classes (`--config=`, `|`, `&`, `$(`, backtick,
space-bearing, oversize) through local validation logic; expected result: rejection before any
process creation.

**Passing / Not verified:** Passed requires allowlist plus validator code reviewed in place and
negative test exercised. Validators present but unreachable evidence of enforcement in all
environments is **Not verified**.

**Related skill routing:** Request-schema validation ownership → `secod-inputs-apis`.

### `PROVISIONAL-runtime-execution-4` — End-of-options delimiter for external operands

**Applicability:** Every subprocess where an externally influenced value lands in an operand
position of a tool parsing options (POSIX-family CLIs). Protected property: attacker cannot
inject option flags (`--output`, `-o`, `--checkpoint-action`) via operand position.

**Inspect and verify:** Locate each user-controlled argv element; confirm it follows the
POSIX `--` end-of-options delimiter, or the tool's documented equivalent, or accepts the value
via stdin/config file instead of argv. Confirm the specific binary documents `--` support.

**Unsafe evidence:** User-controlled array element placed before any `--`; URL/path values
passed directly to tools like `curl`/`tar`/`find` without termination.

**Required negative test:** Fixture submitting `--output /tmp/pwn https://example` style input
to the wrapped tool; expected result: value consumed as positional operand or rejected, no file
written outside intent.

**Passing / Not verified:** Passed requires every external operand delimited or stdin-fed plus
negative test. Tool lacking documented `--` support leaves the control **Not verified**
(replace tool or route value via stdin).

**Related skill routing:** None beyond `secod-inputs-apis` boundary routing.

### `PROVISIONAL-runtime-execution-5` — Least-privilege execution context

**Applicability:** Every spawned process. Protected property: blast radius of any single
compromised child is minimal.

**Inspect and verify:** Dedicated low-privilege service identity per task category, never
root; restricted working directory; explicitly constructed child environment (scrubbed of
secrets and parent-specific variables); bounded timeout on every invocation; streamed/capped
stdout+stderr; filesystem write scope limited to dedicated directories; network egress denied
or allowlisted where feasible. Repository proves code-level items (cwd, env, timeout, caps);
identity, egress and sandbox need deployment/operator evidence.

**Unsafe evidence:** Default environment inheritance carrying credentials; missing timeout or
uncapped output capture; root/service-account overlap between unrelated tasks; no egress
restriction on internet-facing conversion jobs.

**Required negative test:** Local fixture spawning a long-running dummy command confirms
timeout fires, output cap truncates, cancellation kills the child and removes partial files.
Identity/egress assertions rely on supplied deployment evidence, never inference.

**Passing / Not verified:** Passed with evidence requires code-level items verified plus
operator-confirmed runtime identity and egress policy. Any of identity, cwd, env scrubbing,
timeout, output cap or egress unverifiable is **Not verified** for this control.

**Related skill routing:** Container/user isolation depth → `secod-container-runtime`; secret
storage hygiene → `secod-secrets-config`; cleanup semantics → `secod-failure-safety`.

### `PROVISIONAL-runtime-execution-6` — No dynamic code evaluation on untrusted data

**Applicability:** Every server endpoint or worker evaluating dynamically constructed code.
Protected property: untrusted data never becomes executed code.

**Inspect and verify:** Search for `eval`, `new Function`, `exec`/`eval` builtins,
`pickle.loads` and equivalent deserialized-code-object loaders, formula engines compiling to
code (`FormulaParser`, spreadsheet macro execution), expression evaluators fed request data.
Confirm inputs are parsed by restricted AST/data interpreters instead. Where evaluation is
unavoidable, require documented sandbox review: engine-level restriction, isolated worker, and
operator-confirmed host isolation.

**Unsafe evidence:** Any reachable path where request/webhook/file/queue content reaches an
evaluator as code; deserialization of untrusted pickle/marshal blobs; sandbox claimed but
worker sharing process space with secrets.

**Required negative test:** Fixture submitting an expression like `__import__('os').system('id')`
or JS IIFE payload to the evaluation path; expected result: parsed as inert data, rejected, or
executed in an isolated sandbox producing no side effects.

**Passing / Not verified:** Passed requires zero unevaluated untrusted-input-to-evaluator paths
or a completed sandbox review with operator evidence. Sandbox existence inferred from package
presence is **Not verified**.

**Related skill routing:** Unsafe deserialization at API layer → `secod-inputs-apis`.

### `PROVISIONAL-runtime-execution-7` — Server-side template injection prevention

**Applicability:** Every server-side template render whose source or fragments derive from
users, tenants, uploads, or third parties. Protected property: template source is trusted code;
user data enters only as context variables.

**Inspect and verify:** Identify engines (Jinja2, Twig, FreeMarker, ERB, Thymeleaf, Mustache
variants, email/marketing template features). Confirm render calls take fixed, versioned
template files; user values passed as context. Where user-authored templates are unavoidable:
logic-less engines, or hardened sandboxes — Jinja2 `SandboxedEnvironment`-class with attribute
policy review, Twig `sandbox` tag with explicit tags/filters/functions allowlists, FreeMarker
`SAFER_RESOLVER` with `api` builtin disabled — plus rendering in an isolated worker. Verify
autoescape enabled for HTML surfaces.

**Unsafe evidence:** `render_template_string(user_input)`-class calls; template text stored
per-user and rendered with full engine; sandbox configured without explicit allowlists;
rendering inline with the main application process holding credentials.

**Required negative test:** Fixture submitting classic SSTI probes (`{{7*7}}`,
`${7*7}`, `<%= 7*7 %>`) through the feature; expected result: literal text stored/rendered as
data or numeric result proving evaluation is absent; no object graph access.

**Passing / Not verified:** Passed requires all render sites audited, fixed-source or hardened
sandbox confirmed, and probe test clean. Sandbox effectiveness without operator-confirmed
worker isolation is **Not verified**.

**Related skill routing:** Email template delivery surface → `secod-email-messaging` (when
present in scope).

### `PROVISIONAL-runtime-execution-8` — LDAP filter and XPath/XQuery escaping

**Applicability:** Every directory query or XML query constructing expressions from external
input. Protected property: metacharacters cannot alter query logic.

**Inspect and verify:** Locate LDAP filter builders and XPath/XQuery evaluations. Require
parameterized APIs or escaping of filter-special characters (`* ( ) \ NUL` for LDAP; quote and
axis handling for XPath/XQuery). Confirm query results still enforce application authorization
separately.

**Unsafe evidence:** String-formatted filters/queries with user values; absence of escaping
helpers where parameterization is unavailable.

**Required negative test:** Fixture injecting `*)(uid=*))(`-style or XPath predicate payloads;
expected result: literal match failure, no expanded result set.

**Passing / Not verified:** Passed requires every query site escaped/parameterized plus
negative test. Directory endpoints discovered but unreachable for inspection are
**Not verified**.

**Related skill routing:** Query-boundary inventory → `secod-inputs-apis`.

## Exceptional and failure conditions

Covered flows: spawned-process timeouts and dependency failures; partial operations and
cleanup; retry and cancellation. Webhook authenticity/dedup and token/session revocation are
not owned here (see `secod-inputs-apis`, `secod-identity-access`).

Fail-closed requirements:

- Timeout expiry kills the child, releases pipes, and marks the job failed; partial output is
  quarantined or deleted, never treated as success.
- Output-size cap overflow aborts processing deterministically; no silent truncation feeding
  downstream decisions.
- Cancellation or retry storms must not orphan children: track process groups, reap on
  shutdown, remove temporary artifacts idempotently.
- A failed checker, crashed test, or incomplete negative test never counts as success; record
  **Not verified** with next verification step.
- Never assume provider or OS retry schedules; observe actual configured behavior or mark
  **Not verified**.

## Dependency and routing rules

Direct dependencies copied exactly from `secod/catalog.json`: none.

If a referenced routing target is missing, unresolved, malformed, or incomplete: mark affected
controls **Not verified**, name the missing owner/evidence, never invent replacement
dependencies, never issue launch readiness. Route overall launch readiness exclusively to
`secod-ship-check`.

## Evidence and status rules

Statuses only: `Do not ship`, `Fix before launch`, `Recommended hardening`,
`Passed with evidence`, `Not verified`.

Thresholds:

- `Do not ship`: reachable shell-concatenated command injection; user-authored full-engine
  template rendering; untrusted data reaching dynamic evaluation; spawned processes running as
  root with user-influenced arguments.
- `Fix before launch`: missing end-of-options delimiters; missing allowlists/validation on
  active paths; missing timeout/output caps; unsandboxed user-template path; unescaped
  LDAP/XPath queries.
- `Recommended hardening`: defense-in-depth gaps — escaping-only paths, shared service
  identities across tasks, absent egress restrictions where feasible, non-isolated rendering
  workers already behind hardened sandboxes.
- `Passed with evidence`: control verified with the combined evidence named in its section.
- `Never` pass from package presence, inaccessible dashboards, stale snapshots, contradictory,
  incomplete, unsupported, or failed evidence: classify **Not verified**.

## Required output

One finding per applicable control:

`control_id`, `title`, `status`, `scope`, `evidence`, `impact`, `recommended_fix`,
`verification`, `limitations`, `source_refs`, `routed_skills`.

End of report includes:

- Applicability inventory per environment (dev/preview/staging/production) with
  Candidate/Likely/Active classification.
- Test results including skipped/unavailable negative tests.
- Requested external evidence (operator/deployment items).
- All `Not verified` items with exact missing evidence.
- Launch blockers.

Route overall launch readiness to `secod-ship-check`; this skill issues none.

## Negative fixtures and tests

Fixture plan lives at `tests/insecure-fixtures/secod-runtime-execution/README.md`
(documentation-only; no executable fixture code maintained):

| Fixture | Case | Controls | Executable |
| --- | --- | --- | --- |
| F1 | Shell string concatenation | -1, -2 | Documentation-only plan |
| F2 | Argument injection, no `--` | -4 | Documentation-only plan |
| F3 | User-authored template rendering | -7 | Documentation-only plan |
| F4 | Dynamic evaluation on untrusted data | -6 | Documentation-only plan |
| F5 | Missing runtime/evidence case | -5 | Documentation-only plan |
| F6 | No timeout/output cap, hung child | -5 | Documentation-only plan |

Missing-evidence and applicable-failure cases map to F5/F6. No safe executable commands are
maintained in-repository; reviewers construct local equivalents. Never claim a Markdown
fixture plan was executed as code.

Never run destructive, production-changing, user-creating, payment-creating, refunding,
key-rotating, dashboard-changing, or account-changing tests without explicit authorization.

## References

- Source register: [references/sources.md](references/sources.md)
