# Expected result: secod-nextjs

The agent treats Server Actions and Route Handlers as directly callable server endpoints, validates
and authorizes within them, uses `server-only` for privileged modules, and prevents cross-user cache
leakage. It inspects the lockfile before relying on version-specific APIs and does not invent config
keys when version context is missing.
