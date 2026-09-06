# Stripe server and webhook recipe

Use installed Stripe server SDK; do not hardcode an API version unsupported by it.

```ts
const stripe = new Stripe(requireEnv("STRIPE_RESTRICTED_KEY"));
const price = await catalog.requirePurchasablePrice(input.productId);
const session = await stripe.checkout.sessions.create({
  mode: "payment",
  customer: appUser.stripeCustomerId,
  line_items: [{ price: price.stripePriceId, quantity: 1 }],
  success_url: `${origin}/billing/return?session_id={CHECKOUT_SESSION_ID}`,
  cancel_url: `${origin}/billing`,
  metadata: { appUserId: appUser.id },
}, { idempotencyKey: operation.id });
```

Webhook handler must read raw bytes before JSON parsing:

```ts
const raw = await request.text();
const signature = request.headers.get("stripe-signature");
if (!signature) return new Response("Bad request", { status: 400 });
const event = stripe.webhooks.constructEvent(raw, signature, requireEnv("STRIPE_WEBHOOK_SECRET"));
await processStripeEventOnce(event.id, event.type, event.data.object);
return new Response(null, { status: 204 });
```

`processStripeEventOnce` stores event ID uniquely and updates entitlement transactionally from verified
provider state. Return quickly; move slow idempotent work to queue. Test invalid signature, duplicate and
out-of-order events, retries, client price tampering, refunds/disputes, and sandbox/live separation.
