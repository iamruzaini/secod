# Implementation fixture plan: secod-cloudflare-hyperdrive

Start from an intentionally unsafe Cloudflare Hyperdrive boundary. Replace client-trusted authority and unbounded provider calls with version-matched secure implementation from references/data-access.md.

Test success, unauthorized/cross-tenant access, malformed input, replay/retry where applicable, provider failure, and secret redaction. This plan is not a scanner execution.
