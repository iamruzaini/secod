# OpenAI server, structured output, and tool recipe

Use current installed OpenAI SDK and model supporting chosen feature. Keep client server-side:

```ts
const client = new OpenAI({ apiKey: requireEnv("OPENAI_API_KEY") });
await requireTenantPermission(user.id, tenant.id, "ai:generate");
const response = await client.responses.create({
  model: allowedModel,
  input: minimizePrompt(userInput, tenantContext),
  max_output_tokens: 800,
});
```

When application consumes structured fields, use official Structured Outputs API supported by installed
SDK/model and validate again with local schema before persistence. Treat refusals, truncation, and missing
fields explicitly.

For tool calls:

```ts
const args = ToolArgs.parse(toolCall.arguments);
await requireTenantPermission(user.id, tenant.id, toolPermission(toolCall.name));
const result = await executeAllowlistedTool(toolCall.name, args, {
  tenantId: tenant.id,
  idempotencyKey: toolCall.call_id,
});
```

Never let model choose unrestricted SQL, shell commands, URLs, recipients, prices, roles, or tenant IDs.
Allowlist tools and resources, constrain arguments, reauthorize each call, use timeouts and idempotency,
and minimize returned data. Verify webhooks using official SDK helper before parsing effects. Tests cover
schema-invalid output, prompt injection, cross-tenant resource IDs, duplicate tool calls, timeouts, invalid
webhook signatures, secrets in prompts/logs, and disallowed models/tools.
