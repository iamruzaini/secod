# Server authorization recipe

Use with project's verified session adapter. Example TypeScript service boundary:

```ts
const input = UpdateProject.parse(await request.json());
const session = await requireSession(request);
const membership = await db.membership.findUnique({
  where: { tenantId_userId: { tenantId: input.tenantId, userId: session.userId } },
});
if (!membership || !membership.permissions.includes("project:update")) {
  return new Response("Forbidden", { status: 403 });
}
const project = await db.project.findFirst({
  where: { id: input.projectId, tenantId: membership.tenantId },
});
if (!project) return new Response("Not found", { status: 404 });
await db.project.update({ where: { id: project.id }, data: { name: input.name } });
```

Never accept role, owner, or authoritative tenant from body. Validate provider session before this
service and rotate/revoke it through provider-supported APIs. Tests: owner success, no session,
wrong tenant, wrong permission, unknown resource, forbidden fields, expired/revoked session.
