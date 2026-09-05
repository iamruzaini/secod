# SECOD v0.1.0 Installation Test Evidence

Test date: 2026-09-05  
Operating system: Microsoft Windows 11 Home 10.0.26200 (AMD64)  
Node version: v24.11.1  
Skills CLI version: 1.5.23  
Public source: `iamruzaini/secod` `main` at `659cdc41e48cc30ff81ba9742dc2df170f909abf`  
Temporary test root: `C:\Users\justf\AppData\Local\Temp\secod-v0.1.0-install-test`

All agent tests ran in separate fresh Git repositories under the temporary test root.

| Test date | Operating system | Node version | Skills CLI version | Agent target | Command | Expected skill count | Actual skill count | Result |
|---|---|---|---|---|---|---:|---:|---|
| 2026-09-05 | Windows 11 Home 10.0.26200 AMD64 | v24.11.1 | 1.5.23 | Public discovery | `npx skills add iamruzaini/secod --list` | 57 | 57 | PASS |
| 2026-09-05 | Windows 11 Home 10.0.26200 AMD64 | v24.11.1 | 1.5.23 | Codex | `npx skills add iamruzaini/secod --skill '*' --agent codex --yes` | 57 | 57 | PASS |
| 2026-09-05 | Windows 11 Home 10.0.26200 AMD64 | v24.11.1 | 1.5.23 | Claude Code | `npx skills add iamruzaini/secod --skill '*' --agent claude-code --yes` | 57 | 57 | PASS |
| 2026-09-05 | Windows 11 Home 10.0.26200 AMD64 | v24.11.1 | 1.5.23 | Cursor | `npx skills add iamruzaini/secod --skill '*' --agent cursor --yes` | 57 | 57 | PASS |
| 2026-09-05 | Windows 11 Home 10.0.26200 AMD64 | v24.11.1 | 1.5.23 | Codex selective | `npx skills add iamruzaini/secod --skill secod-core --agent codex --yes` | 1 | 1 | PASS |
| 2026-09-05 | Windows 11 Home 10.0.26200 AMD64 | v24.11.1 | 1.5.23 | Codex update | `npx skills update` | 57 refreshed | 57 refreshed | PASS |
| 2026-09-05 | Windows 11 Home 10.0.26200 AMD64 | v24.11.1 | 1.5.23 | Codex repeat install | `npx skills add iamruzaini/secod --skill secod-core --agent codex --yes` (second run) | 1 | 1 | PASS |
| 2026-09-05 | Windows 11 Home 10.0.26200 AMD64 | v24.11.1 | 1.5.23 | Codex removal | `npx skills remove --skill secod-core --yes` | 1 unrelated skill | 1 unrelated skill | PASS |

## Verification details

- Discovery listed 57 names; all 57 names were unique; `secod-core` was present; generalized and provider-specific entries were both present.
- Each full install contained 57 skill directories and 57 `SKILL.md` files.
- Each full install contained all 216 tracked skill files with zero missing resources.
- CLI project listings returned 57 skills for Codex, Claude Code and Cursor.
- Internal Markdown links resolved successfully in the source catalog and all three installed catalogs: zero broken links.
- Selective installation contained only `secod-core`.
- Reinstalling `secod-core` kept one directory and did not create duplicates.
- `secod-ai-api-integrations` was installed as an unrelated skill. After removing `secod-core`, it remained present and its `SKILL.md` SHA-256 hash was unchanged.
- The unattended update verification used `npx skills update -y` to complete the same project update without prompting; it finished with `Updated 57 skill(s)` and exit code 0.
- For complete project removal, omit `--agent`; an agent-scoped removal can leave the shared project copy under `.agents/skills`.

These tests verify discovery, installation, resource copying, update behavior and CLI cleanup. They do not prove that every agent executes every skill correctly inside an application review. No `v0.1.0` tag or GitHub release was created during testing.
