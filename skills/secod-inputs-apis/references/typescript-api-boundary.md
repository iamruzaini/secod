# TypeScript API boundary recipe

Use existing schema library and auth adapter. Validate before effects; project response explicitly.

```ts
const CreateWidget = z.object({
  tenantId: z.string().uuid(),
  name: z.string().trim().min(1).max(120),
}).strict();

export async function createWidget(request: Request) {
  if (Number(request.headers.get("content-length") ?? 0) > 32_768) {
    return new Response("Payload too large", { status: 413 });
  }
  const parsed = CreateWidget.safeParse(await request.json().catch(() => null));
  if (!parsed.success) return Response.json({ error: "Invalid request" }, { status: 400 });
  const session = await requireSession(request);
  await requireTenantPermission(session.userId, parsed.data.tenantId, "widget:create");
  const widget = await db.widget.create({ data: parsed.data });
  return Response.json({ id: widget.id, name: widget.name }, { status: 201 });
}
```

Use parameterized database APIs. For user URLs, allowlist scheme/host, resolve DNS, reject loopback,
private/link-local/metadata ranges, disable or revalidate redirects, and enforce timeout/size limits.
For webhooks, use provider recipe: preserve raw bytes, verify first, parse second, deduplicate event,
then transact effects. Tests must make unsafe variants fail.
