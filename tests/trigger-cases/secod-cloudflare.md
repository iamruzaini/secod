# Trigger case: secod-cloudflare

## Should trigger

```text
Add a Cloudflare Worker using Queues and Hyperdrive.
```

Expected: Select Workers, Queues, and Hyperdrive adapters with shared token/environment defaults and required generalized dependencies.

## Should not trigger

```text
Deploy an AWS Lambda with no Cloudflare signals.
```

Expected: family router excluded unless stated provider-family routing is required.
