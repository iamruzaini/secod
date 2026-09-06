# Expected result: secod-openai

The agent uses the installed OpenAI SDK's documented interfaces, holds API keys on the server,
minimizes transmitted data, validates structured output, treats model-selected tools/arguments as
untrusted, and independently authorizes tool execution. Tests cover unknown tools, invalid schema,
cross-tenant identifiers, prompt injection, timeout, and confirmation denial.
