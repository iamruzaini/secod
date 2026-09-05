# Dependency-routing behavior cases

These cases exercise the checked-in catalog graph. They are deterministic
routing-contract tests, not proof that an LLM or agent host detected every
signal correctly. A real review must recompute the closure from the detected
repository and preserve missing or ambiguous detection as `Not verified`.

| Case | Signals present | Required route | Must not route |
| --- | --- | --- | --- |
| Generic web application | Web/API application; no named provider, AI, payment, container or messaging integration | Common applicable baseline and `secod-core` | Every provider/framework adapter; payment and AI provider profiles |
| Next.js without provider | Next.js/React files; no provider integration | Common applicable baseline plus `secod-nextjs` | AWS, Google Cloud, Firebase, Supabase, Cloudflare, Vercel AI and payment adapters |
| Supabase Auth | Supabase SDK/configuration plus Auth/OAuth/JWT/MFA signals | Common applicable baseline plus `secod-supabase`, `secod-supabase-auth` and `secod-auth-provider-integrations` | AWS, Google Cloud/Firebase, Cloudflare, Vercel, Stripe and AI provider adapters |
| AWS S3/CloudFront | AWS account/configuration plus S3/CloudFront resources | Common applicable baseline plus `secod-aws-web` and `secod-aws-s3-cloudfront` | Google Cloud/Firebase, Supabase, Cloudflare, Vercel and payment/AI provider adapters |
| Google Cloud without Firebase | Google Cloud project/IAM/service-account signals; no Firebase or Firestore Native signal | Common applicable baseline plus `secod-google-cloud-web` | `secod-firebase` and every other unused provider |
| Static Cloudflare Pages | Pages project/deployment signals; no Pages Functions or Workers bindings | Common applicable baseline plus `secod-cloudflare` and `secod-cloudflare-pages` | `secod-cloudflare-workers` and all other unused providers |
| Cloudflare Workers AI | Workers runtime/binding plus Workers AI/model signals | Common applicable baseline plus Cloudflare, Workers, Workers AI and AI baseline | AWS, Google Cloud/Firebase, Supabase, Vercel and unrelated AI providers |
| Vercel without AI | Vercel project/deployment signals; no AI SDK, gateway or model call | Common applicable baseline plus `secod-vercel-platform` | `secod-vercel-ai` and every unrelated provider |
| Stripe and OpenAI | Stripe billing/webhooks plus OpenAI API/model signals | Common applicable baseline plus payments, AI baseline, Stripe and OpenAI | Other payment/AI providers and unused cloud providers |

The executable gate is `python scripts/test_dependency_routing.py`. It checks
unknown dependencies, cycles, transitive closure, core inclusion and provider
isolation for every case above. It does not issue a security verdict.
