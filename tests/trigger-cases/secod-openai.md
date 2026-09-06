# Trigger case: secod-openai

## Should trigger

```text
Add an OpenAI Responses API assistant that can call a refund tool and return structured JSON.
```

Expected: keep credentials server-side, constrain input/output, use a strict schema, map tool names
to server functions, authorize each call, require confirmation for consequential actions, and test
prompt injection and malformed arguments.

## Should not trigger

```text
Add deterministic local search with no model, OpenAI SDK, endpoint, or credential.
```

Expected: OpenAI excluded.
