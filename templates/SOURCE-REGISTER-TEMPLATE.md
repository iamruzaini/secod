# Official source register

This register records the official material used to author implementation guidance. A source status describes the documentation review state; it is not a verdict on a user's application.

## Status meanings

- `Reviewed`: the source content was read and mapped to named recipes or implementation decisions.
- `Pending review`: an official source is known, but its content has not yet been mapped sufficiently for release guidance.
- `Unavailable`: the expected official source could not be accessed or no longer provides sufficient evidence. Record the limitation and do not rely on it.

An HTTP success response alone is not a review.

## Sources

| Source ID | Title | Source type | Direct official URL | Owner | Reviewed date | Refresh trigger | Status | Recipes or decisions supported | Assumptions/notes |
|---|---|---|---|---|---|---|---|---|---|
| SRC-<SKILL>-001 | <Exact page title> | Direct implementation page | https://<official-direct-page> | <Official owner> | YYYY-MM-DD | Documentation, SDK, API, or supported-version change | Reviewed | `<recipe-file>`: <decision> | <Version/scope note> |
| SRC-<SKILL>-002 | <Provider/framework documentation> | Documentation homepage | https://<official-docs-home> | <Official owner> | YYYY-MM-DD | Documentation structure change | Reviewed | Documentation discovery | Index only; not sole support for a recipe |
| SRC-<SKILL>-003 | <Official LLM documentation index> | `llms.txt` or `llms-full.txt` | https://<official-llms-endpoint> | <Official owner> | YYYY-MM-DD | Endpoint or index change | Reviewed | Documentation discovery | Index only; direct pages remain required |

## Source rules

- Use `https://` official domains and direct pages supporting exact implementation decisions.
- Prefer primary provider, framework, standards-body, or project-maintainer documentation.
- Record the official docs homepage and official LLM-readable index when one is published.
- Do not invent an `llms.txt` endpoint. If none is officially published, omit that row.
- Do not use a docs homepage, search page, or `llms.txt` index as the only support for version-sensitive code.
- Map every `Reviewed` source to at least one recipe or decision.
- Do not publish placeholder URLs, dates, statuses, or mappings.
- Refresh sources when relevant APIs, SDK majors, security guidance, or supported versions change.
