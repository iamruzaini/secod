# Trigger case: secod-nextjs

## Should trigger

```text
Create a Next.js App Router Server Action that updates a tenant document.
```

Expected: resolve Next.js version/router, keep privileged modules server-only, authenticate and
authorize inside the action, validate input, scope cache invalidation, and add action tests.

## Should not trigger

```text
Update a Vite-only static site with no Next.js dependency or convention.
```

Expected: Next.js skill excluded.
