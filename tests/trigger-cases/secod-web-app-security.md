# Trigger case: secod-web-app-security

## Should trigger

```text
Add a rich-text form using authenticated cookies.
```

Expected: Use safe rendering, server authorization, appropriate CSRF protection, narrow origins, and browser-boundary tests.

## Should not trigger

```text
Change server-only database indexing.
```

Expected: skill excluded.
