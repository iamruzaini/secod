# Official source register

This register records official material used to design `secod-core`. Source status describes
documentation review, not security status of a user's application.

## Status meanings

- `Reviewed`: content was read and mapped to named implementation recipes.
- `Pending review`: official source is known, but mapping is incomplete.
- `Unavailable`: expected official source is inaccessible or insufficient and is not relied on.

URL reachability alone does not establish review.

## Sources

| Source ID | Title | Source type | Direct official URL | Owner | Reviewed date | Refresh trigger | Status | Recipes or decisions supported | Assumptions/notes |
|---|---|---|---|---|---|---|---|---|---|
| CORE-SRC-001 | Agent Skills specification | Direct specification | https://agentskills.io/specification | Agent Skills project | 2026-09-06 | Specification, metadata, discovery, validation, or progressive-disclosure change | Reviewed | discovery-routing.md: skill discovery and progressive loading; task-context.md: concise routed context | Applies to current published Agent Skills specification. |

## Local product authority

[`../../../docs/PRD.md`](../../../docs/PRD.md) defines SECOD product positioning and routing
requirements. It is repository product policy rather than an external technical source.
