# Trigger case: secod-inputs-apis

## Should trigger

```text
Add a webhook endpoint and an API that fetches a user-submitted preview URL.
```

Expected: validate raw webhook authenticity, parse against schemas, constrain outbound targets and
redirects, authorize the operation, and add malformed-input and SSRF tests.

## Should not trigger

```text
Rename a local TypeScript variable without changing behavior.
```

Expected: no API-boundary skill.
