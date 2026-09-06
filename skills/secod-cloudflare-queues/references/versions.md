# Cloudflare Queues: supported versions

Supported: Wrangler and Workers compatibility date resolved from configuration; Queues limits and delivery behavior matched to current docs. Exact version must be resolved from lockfile, runtime configuration, or versioned API header and must still be documented by direct official source reviewed on 2026-09-06. Unpinned, prerelease, end-of-life, or undocumented versions are unsupported until a version-specific source and tests are added.

## Resolution checklist

- Read package manager lockfile, runtime configuration, and versioned API headers.
- Match implementation to direct official documentation in [sources.md](sources.md).
- Reject undocumented methods, copied examples from another major version, and assumed dashboard capabilities.
