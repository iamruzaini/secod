# Next.js App Router boundary recipe

Confirm installed Next.js version. Keep privileged data access in server-only module:

```ts
// lib/projects.server.ts
import "server-only";

export async function renameProject(userId: string, tenantId: string, id: string, name: string) {
  await requireTenantPermission(userId, tenantId, "project:update");
  const project = await db.project.findFirst({ where: { id, tenantId } });
  if (!project) throw new NotFoundError();
  const updated = await db.project.update({ where: { id }, data: { name } });
  return { id: updated.id, name: updated.name };
}
```

```ts
// app/projects/actions.ts
"use server";
const Rename = z.object({ tenantId: z.string().uuid(), id: z.string().uuid(), name: z.string().trim().min(1).max(120) });

export async function renameProjectAction(value: unknown) {
  const input = Rename.parse(value);
  const session = await requireSession();
  return renameProject(session.userId, input.tenantId, input.id, input.name);
}
```

Treat action as public POST entry. Proxy/Middleware may reject early but cannot replace authorization.
Avoid shared caching for permission-dependent data. Test direct invocation, wrong tenant, malformed
input, minimized return value, and that server-only module cannot enter client graph.
