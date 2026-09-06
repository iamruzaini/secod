# Executable implementation fixtures: secod-openai

Run:

```text
python tests/insecure-fixtures/secod-openai/run_fixtures.py
```

The fixture models server-only API credentials, tool allowlisting, argument validation, trusted
resource reload, tenant authorization, and unauthenticated denial. It uses local callbacks instead
of the OpenAI API; provider retention, spend, and project settings are not inspected.
