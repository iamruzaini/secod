# Official source register

| Source ID | Title | Source type | Direct official URL | Owner | Reviewed date | Refresh trigger | Status | Recipes or decisions supported | Assumptions/notes |
|---|---|---|---|---|---|---|---|---|---|
| STRIPE-SRC-001 | API keys | Direct security guide | https://docs.stripe.com/keys | Stripe | 2026-09-06 | Key model change | Reviewed | stripe-server-webhooks.md: publishable/restricted/secret and sandbox/live boundaries | Prefer restricted key when supported. |
| STRIPE-SRC-002 | Receive webhook events | Direct implementation guide | https://docs.stripe.com/webhooks | Stripe | 2026-09-06 | Webhook API or delivery change | Reviewed | stripe-server-webhooks.md: raw-body verification, events, local testing | Endpoint-specific secret required. |
| STRIPE-SRC-003 | Idempotent requests | API reference | https://docs.stripe.com/api/idempotent_requests | Stripe | 2026-09-06 | API-version behavior change | Reviewed | stripe-server-webhooks.md: stable idempotency key and retry behavior | Confirm SDK request-options shape. |
| STRIPE-SRC-004 | Stripe documentation index | Official llms.txt | https://docs.stripe.com/llms.txt | Stripe | 2026-09-06 | Index change | Reviewed | stripe-server-webhooks.md: current direct-page discovery | Index is not sole support for code. |
