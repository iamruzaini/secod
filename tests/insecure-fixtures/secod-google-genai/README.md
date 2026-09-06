# Implementation fixture plan: secod-google-genai

Start from an intentionally unsafe Google GenAI boundary. Replace client-trusted authority and unbounded provider calls with version-matched secure implementation from references/model-tools-data.md.

Test success, unauthorized/cross-tenant access, malformed input, replay/retry where applicable, provider failure, and secret redaction. This plan is not a scanner execution.
