# Source register: secod-ai-api-integrations

Use official documentation indexes (`llms.txt` / `llms-full.txt` where published) for discovery
only. Verify security-critical claims against the direct primary source and refresh this register
before its review-expiry date.

| Source ID | Title | Direct URL | Owner | Reviewed | Expiry / refresh trigger | Status | Control IDs | Version / assumptions |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OWASP-LLM01-2025 | LLM01:2025 Prompt Injection (OWASP Top 10 for LLM Applications) | https://genai.owasp.org/llmrisk/llm01-prompt-injection/ | OWASP GenAI Security Project | 2026-08-26 | 12 months, or on new Top 10 edition | Reviewed | PROVISIONAL-AI-04, -05 | Edition 2025; direct/indirect injection, mitigation is application-side input handling, privilege restriction |
| OWASP-LLM05-2025 | LLM05:2025 Improper Output Handling (OWASP Top 10 for LLM Applications) | https://genai.owasp.org/llmrisk/llm052025-improper-output-handling/ | OWASP GenAI Security Project | 2026-08-26 | 12 months, or on new Top 10 edition | Reviewed | PROVISIONAL-AI-04, -07 | Edition 2025; output treated as trusted content leads to XSS/privilege paths; validation before downstream use |
| OWASP-LLM06-2025 | LLM06:2025 Excessive Agency (OWASP Top 10 for LLM Applications) | https://genai.owasp.org/llmrisk/llm062025-excessive-agency/ | OWASP GenAI Security Project | 2026-08-26 | 12 months, or on new Top 10 edition | Reviewed | PROVISIONAL-AI-03, -04 | Edition 2025; minimize tool scope/permissions; authorization stays outside the model |
| OWASP-LLM08-2025 | LLM08:2025 Vector and Embedding Weaknesses (OWASP Top 10 for LLM Applications) | https://genai.owasp.org/llmrisk/llm082025-vector-and-embedding-weaknesses/ | OWASP GenAI Security Project | 2026-08-26 | 12 months, or on new Top 10 edition | Reviewed | PROVISIONAL-AI-05, -06 | Edition 2025; retrieval authorization, access control on vector/RAG stores, retention of embeddings |
| OWASP-LLM10-2025 | LLM10:2025 Unbounded Consumption (OWASP Top 10 for LLM Applications) | https://genai.owasp.org/llmrisk/llm102025-unbounded-consumption/ | OWASP GenAI Security Project | 2026-08-26 | 12 months, or on new Top 10 edition | Reviewed | PROVISIONAL-AI-02 | Edition 2025; rate limiting, queue bounds, token/cost budgets, per-user quotas |

For every retained source, record version/SDK version, reviewed date, review expiry,
hash/ETag when obtainable, owner, plan/tier, region, feature maturity, and linked control IDs.

Review-time evidence boundaries:

- No single provider retained: this is a general baseline skill; provider-specific claims belong
  to `secod-openai`, `secod-anthropic`, `secod-google-genai`, `secod-xai-grok`, `secod-vercel-ai`
  and related provider skills with their own registers.
- Provider retention/training/ZDR/telemetry settings, spend ceilings, deletion-completion proof:
  repository evidence cannot prove reviewed-account state. Require current direct official
  documentation for provider capability plus matching Dashboard/Management API evidence for the
  exact project, environment, endpoint and feature. Keep AI-02, AI-06, AI-09 and/or AI-11 `Not
  verified` as mapped in `SKILL.md` until supplied at review time.
- Any short-lived client-token mechanism cited in AI-01 requires review-time verification against
  the exact provider feature's current direct official documentation and matching implementation/
  configuration evidence. Record the URL, reviewed date, SDK/API version where stated, minting
  authority, expiry, use/replay limits, scope/audience and configurable session constraints; record
  `not documented` for unspecified properties. No blanket cross-provider claim is recorded here.
- Source-register entries alone never prove Dashboard configuration or deletion completion.
