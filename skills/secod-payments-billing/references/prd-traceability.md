# PRD traceability: secod-payments-billing

## PRD section 8.4

| Requirement | Controls and sections |
| --- | --- |
| Server resolves product, price, currency, quantity, discount, tenant and entitlement | PB-1; tenant authorization routes to `secod-web-app-security` |
| Provider-hosted checkout or approved components; avoid raw card handling | PB-2 |
| Verified webhook or provider retrieval is authoritative; never trust client paid state | PB-5 |
| Verify raw body and every authenticity/replay capability actually supplied | PB-4, PB-6 |
| Maintain sourced capability matrix; deduplicate and handle delivery disorder | PB-6, PB-7 |
| Atomically map provider events to user, tenant and entitlement | PB-8 |
| Fail closed and preserve recoverability on partial operations | PB-3, PB-7, PB-8; `Exceptional and failure conditions`; route general failure taxonomy to `secod-failure-safety` |
| Correct access for refund, dispute, chargeback, cancellation, expiration and renewal failure | PB-9 |
| Use restricted server-only test/live-separated credentials and reconcile provider state | PB-7, PB-9, PB-10 |

## PRD section 14.2 payment fixtures

| Required fixture behavior | Executable cases | Controls |
| --- | --- | --- |
| Real documented webhook envelope and capability matrix | Synthetic baseline envelope driven by a sourced capability row; real envelopes remain adapter fixtures | PB-4, PB-6 |
| Signature, supported freshness and delivery/event ID; compensating replay controls | `test_07_webhook_authenticity_freshness_and_replay`, `test_12_capability_source_and_adapter_blockers` | PB-6 |
| Duplicate and out-of-order events | `test_08_delivery_order_retry_disablement_and_reconciliation` | PB-6, PB-7 |
| Retry exhaustion and disabled endpoints | `test_08_delivery_order_retry_disablement_and_reconciliation` | PB-7 |
| Partial transaction recovery | `test_09_atomic_mapping_and_tenant_binding` | PB-8 |
| Tenant mapping | `test_01_clean_integration`, `test_09_atomic_mapping_and_tenant_binding` | PB-1, PB-8 |
| Entitlement revocation | `test_10_lifecycle_correction_and_append_only_ledger` | PB-9 |
| Reconciliation | `test_08_delivery_order_retry_disablement_and_reconciliation`, `test_10_lifecycle_correction_and_append_only_ledger` | PB-7, PB-9 |

Baseline fixtures are executable and provider-neutral. They never prove a provider adapter's real
envelope. Each detected provider still needs its adapter's reviewed primary sources and executable
provider fixture before release.

## PRD section 14.3 payment release gate

`secod-ship-check` `PROVISIONAL-ship-4` requires current passing evidence from both
`secod-payments-billing` and every detected payment adapter. `PROVISIONAL-ship-5` rejects stale or
missing direct provider sources and unreviewed fixture outcomes. Therefore any missing adapter,
unbacked capability row, documentation-only provider fixture or failed executable fixture remains
`Not verified` and blocks launch readiness.
