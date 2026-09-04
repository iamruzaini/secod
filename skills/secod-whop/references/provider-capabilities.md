# Whop provider capability matrix

Use this matrix to avoid borrowing behavior from another payment provider. It describes only the local Whop snapshot, not current production configuration.

| Capability | Local snapshot signal | Required application evidence | If absent or conflicting |
| --- | --- | --- | --- |
| Signature | Standard Webhooks `webhook-signature`; SDK unwrap or HMAC over ID, timestamp, raw body | raw-body route test, deployed verifier config, redacted current delivery | `Not verified`; forged fulfillment blocks launch |
| Freshness | `webhook-timestamp`; five-minute rejection | stale/future tests, reliable clock, current SDK/provider policy | `Not verified`; missing freshness is `Fix before launch` |
| Delivery identity | `webhook-id`, mirrored by body `id` in example | persistent unique ledger and concurrent duplicate test | `Not verified`; in-memory dedupe is insufficient |
| Acknowledgement | 2xx under five seconds after verify and durable handoff | deployed-equivalent timing and queue-failure tests | `Not verified`; acknowledge-before-durability is unsafe |
| Delivery mode | at least once, same ID on retries, order not guaranteed | duplicate/out-of-order fixtures and current-state retrieval | `Not verified` |
| Retry | 12 retries over approximately three days (about 71 hours) in snapshot | current delivery history/contract and bounded app retries | snapshot guides tests only; live behavior `Not verified` |
| Disablement | warning after 24 hours; disable after 72 hours plus at least 10 failures in snapshot | enabled-state monitor, alert, delivery evidence, re-enable/reconcile runbook | `Not verified`; no recovery blocks launch |
| Missed-event recovery | events during disablement are not resent; API read required | reconciliation with durable cursor and tests | `Not verified` |
| REST version | dated `Api-Version-Date` or key stored pin | deployed pin, locked SDK, migration fixture | `Not verified` |
| Webhook version | `api_version` and `api_version_date` | current webhook export and matching schema fixtures | `Not verified` |
| Outbound POST idempotency | authenticated POST accepts `Idempotency-Key`; 24-hour replay record in snapshot | durable logical-operation key and retry tests | `Not verified`; duplicate writes block launch |
| Environment | separate production/sandbox endpoints and keys/webhooks | per-environment references, IDs, products, URLs, provider export | `Not verified`; mixed environments block launch |
| Membership authority | native resource statuses/methods and lifecycle events | version-matched state table, provider reads, entitlement reconciliation | `Not verified`; unknown status must fail safely |
| Pause | stops renewal; current-period access remains; no activation/deactivation event | post-action provider retrieval and policy test | `Not verified` |
| Cancel | period-end and immediate cancellation differ | both transition tests and provider state | `Not verified` |
| Terminate | no distinct action located | current provider evidence or approved catalog clarification | always `Not verified` until resolved |
| Refund/dispute | relevant events/resources documented; lost dispute differs from refund | fixtures, periodic retrieval, ledger/entitlement correction | `Not verified` |
| Embedded identity | short-lived iframe JWT and server-created access token | supported mint/verify path, expiry evidence, cross-scope tests | `Not verified` |

Interpret every row with [sources.md](sources.md). Do not treat approximate retry periods, examples, default versions, or local mtimes as current live guarantees.
