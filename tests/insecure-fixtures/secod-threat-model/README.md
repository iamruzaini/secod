# Insecure fixture plan: secod-threat-model

Minimal reproducible unsafe cases, one per control family. Documentation-only plan; no
executable code is maintained in this repository.

## F1 — Undocumented admin export (assets/data classes)

`/admin/export` streams a database dump; contents undocumented. Expected: data class `Unknown`,
conservative handling forced, downstream scoping blocked until resolved.

## F2 — Debug route omitted from model (surface enumeration)

Inventory contains `/_debug/queries` mock endpoint; model's surface list omits it. Expected:
reconciliation failure — surface list must match inventory 1:1; omission is a model defect
routed to `secod-inputs-apis`.

## F3 — Tenant edge without enforcement point (trust boundaries)

Model draws browser→API tenant boundary but tenant ID originates from a client header with no
server verification noted. Expected: `Fix before launch` for the model element; route to
`secod-identity-access`.

## F4 — Checkout without abuse coverage (abuse cases)

Payment flow modeled with happy path only: no replay, out-of-order, price-tampering,
cross-tenant purchase, or refund-abuse cases. Expected: model defect; route to
`secod-payments-billing` and `secod-abuse-limits`.

## F5 — Webhook without partial-failure handling (failure states)

Stripe webhook modeled as "process event" with no duplicate-delivery, out-of-order, or
rollback behavior for entitlement grants. Expected: model defect routed to
`secod-payments-billing`; fail-open risk flagged per OWASP A10:2025.

## F6 — RAG without tenant filter (AI flows)

RAG feature queries a shared vector store; no pre-retrieval tenant metadata filter recorded;
fallback provider assumed to satisfy the same data policy without evidence. Expected: flow
blocked; policy comparison marked unverified pending provider documentation.

## F7 — AI endpoint absent from cost model (spend abuse)

AI generation endpoint detected in inventory but missing from high-cost operations list.
Expected: model defect; route to `secod-abuse-limits`.

## F8 — Ownerless accepted risk (register)

Residual-risk register entry: "preview environment exposure accepted" with no accepter name and
no review date. Expected: entry `Not verified`; register fails validation.
