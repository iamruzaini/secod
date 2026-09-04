# Executable payments-billing fixtures

Run from `secod/`:

```text
python tests/insecure-fixtures/secod-payments-billing/run_fixtures.py
```

Runner uses Python standard library only, writes no files, makes no network calls and emits JSON.
Exit `0` means all fixture expectations were reproduced. It does not prove an inspected application,
provider adapter, Dashboard configuration or production environment is secure.

Cases cover PB-1 through PB-10: clean secure flow; client price and tenant tampering; raw card
collection; duplicate outbound writes and missing session expiry; unexpected API version; client-paid
entitlement; forged, stale and duplicate webhook delivery; out-of-order delivery, retry exhaustion,
disabled endpoint detection and reconciliation; partial atomic mapping and tenant binding; append-only
lifecycle correction; credential exposure and test/live separation; unbacked capability rows, missing
adapters and missing provider evidence.

Webhook format is a synthetic provider-neutral envelope driven by a capability row. It is not evidence
for any real provider envelope. Provider-specific fixtures and direct sources remain required.
