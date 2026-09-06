# Implementation fixture plan: secod-lemonsqueezy

Start from an intentionally unsafe Lemon Squeezy boundary. Replace client-trusted authority and unbounded provider calls with version-matched secure implementation from references/checkout-webhooks.md.

Test success, unauthorized/cross-tenant access, malformed input, replay/retry where applicable, provider failure, and secret redaction. This plan is not a scanner execution.
