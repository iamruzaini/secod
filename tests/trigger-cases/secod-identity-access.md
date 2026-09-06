# Trigger case: secod-identity-access

## Should trigger

```text
Add tenant-scoped invoice access and an admin role to this authenticated API.
```

Expected: inspect the identity and tenancy model, enforce authorization at the backend, and add
same-tenant, cross-tenant, unauthenticated, and insufficient-role tests.

## Should not trigger

```text
Change the public landing-page heading.
```

Expected: no identity skill because no identity or privileged boundary changes.
