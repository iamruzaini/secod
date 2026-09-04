# Source register: secod-payments-billing

This register supports provider-neutral controls only. Provider envelope fields, retry schedules,
key models, API versions, endpoint disablement and other provider behavior belong to
`secod-stripe`, `secod-polar`, `secod-lemonsqueezy`, `secod-dodo-payments` or `secod-whop`.
Every capability-matrix row must cite a `Reviewed` direct-primary row in the applicable adapter's
`references/sources.md`; this baseline register cannot substitute for that evidence.

Review date: 2026-08-27. Review expiry: 2027-02-27. Owner: SECOD maintainers. Refresh earlier
when a pinned edition changes, a living page changes, or an adapter adds a provider-specific claim.

| ID | Direct primary source | Official index | Version | Integrity evidence | Status | Control IDs | Assumptions |
| --- | --- | --- | --- | --- | --- | --- | --- |
| PB-S1 | [OWASP ASVS V2: Validation and Business Logic](https://raw.githubusercontent.com/OWASP/ASVS/v5.0.0/5.0/en/0x11-V2-Validation-and-Business-Logic.md) | [ASVS 5.0.0 release](https://github.com/OWASP/ASVS/releases/tag/v5.0.0_release) | 5.0.0 | SHA-256 `70ad0f68df22ddd825c2837e74999fa026851e75a3128372307685e2bb526969`; ETag `c8972182b072e4edf4e0c061c0d974316b75f6cbb8a3a86aebe2b9293d6c4aa1` | Reviewed | PB-1, PB-3, PB-8 | Global; no plan, region or SDK dependency |
| PB-S2 | [OWASP ASVS V8: Authorization](https://raw.githubusercontent.com/OWASP/ASVS/v5.0.0/5.0/en/0x17-V8-Authorization.md) | [ASVS 5.0.0 release](https://github.com/OWASP/ASVS/releases/tag/v5.0.0_release) | 5.0.0 | SHA-256 `60c188b1703cab2086841d8f1b4adc0ededf66ed38c676a11bb92347646b5330`; ETag `ea5034f2067ffbe6fd39b5283585920682d7f74d055123e4d0813cc5a6c79732` | Reviewed | PB-1, PB-5, PB-9 | Global; no plan, region or SDK dependency |
| PB-S3 | [OWASP Third Party Payment Gateway Integration Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Third_Party_Payment_Gateway_Integration_Cheat_Sheet.html) | [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/) | Living document reviewed 2026-08-27 | SHA-256 `6e3a2c20ce94fb25d8adbe37dba9f3574abaec4af69b461f40202e9ecc8d45ee`; Last-Modified `2026-08-25` | Reviewed | PB-1, PB-3, PB-5, PB-6, PB-7, PB-9 | Generic gateway guidance; provider contract still controls exact capabilities |
| PB-S4 | [OWASP Top 10:2025 A10 Mishandling of Exceptional Conditions](https://owasp.org/Top10/2025/A10_2025-Mishandling_of_Exceptional_Conditions/) | [OWASP Top 10:2025](https://owasp.org/Top10/2025/) | 2025 | SHA-256 `5796fc32df8efb1adae316dca9c7c4852ecff82b0ebc1c5ae45b4c9ac52549be`; Last-Modified `2026-08-05` | Reviewed | PB-3, PB-7, PB-8, PB-9; exceptional conditions | Global; no plan, region or SDK dependency |
| PB-S5 | [PCI SSC FAQ: SAQ A versus SAQ A-EP payment-page origin](https://www.pcisecuritystandards.org/faqs/if-a-merchant-s-e-commerce-implementation-meets-the-criteria-that-all-elements-of-payment-pages-originate-from-a-pci-dss-compliant-service-provider-is-the-merchant-eligible-to-complete-saq-a-or-saq-a-ep/) | [PCI SSC FAQ library](https://www.pcisecuritystandards.org/faqs/) | Current FAQ reviewed 2026-08-27 | SHA-256 `049221769a3d5ec8f849f7ef87aee70de1a5ab9110caa4f3369152d50e7420d9` | Reviewed | PB-2 | Scope guidance only; not a compliance determination |
| PB-S6 | [OWASP ASVS V13: Configuration](https://raw.githubusercontent.com/OWASP/ASVS/v5.0.0/5.0/en/0x22-V13-Configuration.md) | [ASVS 5.0.0 release](https://github.com/OWASP/ASVS/releases/tag/v5.0.0_release) | 5.0.0 | SHA-256 `f66ef1306eba07e04fcd0f23b52d082747f1b4fba0a19934167fb35507afba6d`; ETag `f4472565c0648b7c19eb4440a32cb394bcd818f2ef734f57917799ad324a369a` | Reviewed | PB-10 | Global; provider key restrictions still require adapter evidence |

## Portable mappings

| Control | Version-qualified mapping | Baseline source refs | Provider evidence still required |
| --- | --- | --- | --- |
| PB-1 | `v5.0.0-2.2.2`, `v5.0.0-8.3.1` | PB-S1, PB-S2, PB-S3 | Product, price and checkout contract |
| PB-2 | Explicitly unmapped to ASVS; PCI scope depends on actual payment-page design | PB-S5 | Approved component and integration mode |
| PB-3 | `v5.0.0-2.3.3` | PB-S1, PB-S3, PB-S4 | Idempotency and session-expiry support |
| PB-4 | Explicitly provider-contract-specific; no portable ASVS mapping claimed | None | API and webhook version fields |
| PB-5 | `v5.0.0-8.3.1` | PB-S2, PB-S3 | Authoritative retrieval and event state |
| PB-6 | Explicitly provider-contract-specific beyond generic callback authenticity and replay guidance | PB-S3 | Every capability-matrix field and compensating control |
| PB-7 | `OWASP-Top10-2025-A10` | PB-S3, PB-S4 | Retry, endpoint-disablement and delivery behavior |
| PB-8 | `v5.0.0-2.3.3`, `OWASP-Top10-2025-A10` | PB-S1, PB-S4 | Provider resource and event identity |
| PB-9 | `v5.0.0-8.3.2`, `OWASP-Top10-2025-A10` | PB-S2, PB-S3, PB-S4 | Enabled lifecycle events and reconciliation APIs |
| PB-10 | `v5.0.0-13.3.1`, `v5.0.0-13.3.2`, `v5.0.0-13.3.4` | PB-S6 | Key types, restrictions and live/test model |

New provider-specific claims cannot pass until their adapter register contains a current direct
primary-source row. `llms.txt`, `llms-full.txt`, cached excerpts and this baseline register are
discovery aids only for provider behavior.
