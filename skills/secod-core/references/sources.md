# Source register: secod-core

Use official documentation indexes for discovery only. Verify security-critical claims against
the direct primary source and refresh this register before its review-expiry date.

| Source ID | Title | Direct official URL | Owner | Reviewed | Expiry / refresh trigger | Status | Control IDs | Assumptions |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S1 | File-system conventions: proxy.js (middleware renamed to Proxy in v16, Node runtime default) | https://nextjs.org/docs/app/api-reference/file-conventions/proxy | Vercel / Next.js team | 2026-08-24 | Refresh on Next.js major release or page change | Reviewed | PROVISIONAL-core-2, PROVISIONAL-core-3 | See register assumptions below. |
| S2 | Renaming Middleware to Proxy (migration guidance and codemod) | https://nextjs.org/docs/messages/middleware-to-proxy | Vercel / Next.js team | 2026-08-24 | Refresh on Next.js major release | Reviewed | PROVISIONAL-core-2 | See register assumptions below. |

Provider-specific documentation indexes (`llms.txt`/`llms-full.txt`) and their primary pages are
registered in each routed skill's own `references/sources.md`, not here; this skill treats those
indexes as discovery inputs only and never as proof of current provider behavior.

Assumptions: S1/S2 reflect Next.js 16.x conventions; repositories on older supported versions
may legitimately use legacy `middleware.ts`. No plan/tier/region assumptions apply to this skill.
