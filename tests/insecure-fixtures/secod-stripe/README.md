# Implementation fixture plan: secod-stripe

Replace browser-supplied amounts, redirect-based entitlement, and an unsigned webhook with trusted
server pricing, idempotent creation, raw-body signature verification, durable event deduplication,
and reconciliation tests. This plan does not assert that a Stripe dashboard was inspected.
