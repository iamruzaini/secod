# Implementation fixture plan: secod-workos

Start from an intentionally unsafe WorkOS boundary. Replace client-trusted authority and unbounded provider calls with version-matched secure implementation from references/sessions-callbacks.md.

Test success, unauthorized/cross-tenant access, malformed input, replay/retry where applicable, provider failure, and secret redaction. This plan is not a scanner execution.
