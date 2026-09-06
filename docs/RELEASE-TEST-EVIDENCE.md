# v0.1.0 installation test evidence

This 2026-09-07 run tested the merged SECOD release candidate from public
`main` at commit `e550cc218992cff67990fcc862a53e7214b3dc0d`. The skill tree
was unchanged by the subsequent release-document-only changes.

- Test date: 2026-09-07
- Operating system: Microsoft Windows 11 Home 10.0.26200 (AMD64)
- Node version: v24.11.1
- Skills CLI version: 1.5.23
- Public source: `iamruzaini/secod` `main` at `e550cc218992cff67990fcc862a53e7214b3dc0d`
- Temporary test root: `C:\Users\justf\AppData\Local\Temp\secod-v0.1.0-final-install-b7590d5a2b4f45819e171366aa929a11`

Every full-agent test ran in a separate fresh Git repository under the
temporary test root.

| Test date | Operating system | Node version | Skills CLI version | Agent target | Command | Expected skill count | Actual skill count | Result |
|---|---|---|---|---|---|---:|---:|---|
| 2026-09-07 | Windows 11 Home 10.0.26200 AMD64 | v24.11.1 | 1.5.23 | Public discovery | `npx skills add iamruzaini/secod --list` | 60 | 60 | PASS |
| 2026-09-07 | Windows 11 Home 10.0.26200 AMD64 | v24.11.1 | 1.5.23 | Codex | `npx skills add iamruzaini/secod --skill '*' --agent codex --yes` | 60 | 60 | PASS |
| 2026-09-07 | Windows 11 Home 10.0.26200 AMD64 | v24.11.1 | 1.5.23 | Claude Code | `npx skills add iamruzaini/secod --skill '*' --agent claude-code --yes` | 60 | 60 | PASS |
| 2026-09-07 | Windows 11 Home 10.0.26200 AMD64 | v24.11.1 | 1.5.23 | Cursor | `npx skills add iamruzaini/secod --skill '*' --agent cursor --yes` | 60 | 60 | PASS |
| 2026-09-07 | Windows 11 Home 10.0.26200 AMD64 | v24.11.1 | 1.5.23 | Codex selective | `npx skills add iamruzaini/secod --skill secod-core --agent codex --yes` | 1 | 1 | PASS |
| 2026-09-07 | Windows 11 Home 10.0.26200 AMD64 | v24.11.1 | 1.5.23 | Codex update | `npx skills update --yes` | 60 refreshed | 60 refreshed | PASS |
| 2026-09-07 | Windows 11 Home 10.0.26200 AMD64 | v24.11.1 | 1.5.23 | Codex repeat install | `npx skills add iamruzaini/secod --skill secod-core --agent codex --yes` (second run) | 1 | 1 | PASS |
| 2026-09-07 | Windows 11 Home 10.0.26200 AMD64 | v24.11.1 | 1.5.23 | Project-scope removal | `npx skills remove --skill secod-core --yes` | 1 unrelated skill | 1 unrelated skill | PASS |

## Verification details

- Public discovery reported 60 skills. Full installs had 60 unique names and
  included `secod-core`, generalized coverage such as
  `secod-identity-access`, and provider coverage such as `secod-firebase`.
- Each full install contained 60 skill directories, 60 `SKILL.md` files, and
  zero broken relative resource links.
- Codex, Claude Code, and Cursor were tested in separate clean repositories;
  one agent installation did not mask another.
- The update command completed with `Updated 60 skill(s)` and exit code 0.
- Selective installation contained only `secod-core`.
- Reinstalling `secod-core` kept one directory and did not create duplicates.
- Project-scope removal deleted `secod-core`; an unrelated
  `secod-ai-api-integrations` skill remained present and its SHA-256 hash was
  unchanged.

These tests verify public discovery, installation, resource copying, update
behavior, repeat-install behavior, and CLI cleanup. They do not prove that an
agent executes every skill correctly inside a real application, nor do they
certify any application's security or provider deployment. The `v0.1.0` tag
and GitHub release were created only after the repository and workflow gates
passed.
