# <Recipe title>

Use this recipe when <exact framework/provider/runtime/feature context>. Do not use it for <important exclusion>.

## Support and assumptions

| Item | Supported or assumed value |
|---|---|
| Language/runtime | <value and version range> |
| Framework | <value and version range, or not applicable> |
| Provider SDK/API | <package/API and version range, or not applicable> |
| Execution boundary | <server, worker, edge, mobile device, browser, etc.> |
| Identity model | <session, JWT, workload identity, etc.> |
| Tenant/ownership model | <model or explicit assumption> |

If the repository falls outside these bounds, confirm current official documentation before adapting the recipe.

## Security properties

- <Testable property>.
- <Testable property>.
- <Testable property>.

## Packages and imports

```<language>
<minimal imports or dependency configuration>
```

Explain why each security-relevant dependency is used. Prefer existing repository dependencies when they provide the same invariant.

## Trust boundary and data flow

1. <Untrusted input or caller> sends <data>.
2. <Trusted component> authenticates, authorizes, and validates it.
3. <Provider/database/effect> receives only <minimized data>.
4. <Response/event> returns through <safe serialization or verification boundary>.

Never place a privileged decision in a client merely because the client initiates the flow.

## Secure implementation

```<language>
<complete focused implementation or precise patch pattern>
```

The implementation must make these decisions visible:

- authentication and tenant/resource authorization;
- input schema, normalization, and size constraints;
- secret/credential source and runtime boundary;
- data minimization and persistence behavior;
- timeouts, retries, concurrency, and idempotency as applicable;
- safe errors and logging;
- cleanup, rollback, revocation, or reconciliation as applicable.

## Unsafe alternative

```<language>
<small unsafe example only when it materially clarifies the boundary>
```

This is unsafe because <specific exploit or failure path>. Do not include a copy-ready insecure implementation longer than needed to teach the distinction.

## Tests

```<language>
<positive and negative test examples>
```

Cover:

- expected authorized success;
- missing/invalid identity;
- insufficient role, ownership, or tenant mismatch;
- malformed, oversized, tampered, stale, or replayed data as applicable;
- timeout, retry, duplicate, concurrent, and partial failure as applicable;
- sensitive-data absence from responses and logs;
- cleanup/reconciliation behavior.

## Provider or deployment action

Include only if repository code cannot complete the setup.

| Action | Secure value | Why required | How to verify |
|---|---|---|---|
| <exact action/path> | <value> | <dependency> | <CLI/API/console procedure> |

State whether the action was actually performed. If it was not, instruct the user without implying verification.

## Official sources

| Decision supported | Direct official URL | Version/date note |
|---|---|---|
| <decision> | https://<official-direct-page> | <version or reviewed date> |

The matching entries must also appear in `sources.md`.
