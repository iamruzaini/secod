# Dependency-routing behavior cases

These cases exercise checked-in catalog graph. They are deterministic routing tests, not proof that
an agent host detected every signal correctly. For missing context, inspect repository or ask a
narrow question before selecting provider APIs.

| Case | Signals present | Required route | Must not route |
|---|---|---|---|
| Generic web application | Web/API application; no named provider, AI, payment, container or messaging integration | Applicable generalized skills and `secod-core` | Every provider/framework adapter |
| Next.js without provider | Next.js files; no provider integration | Applicable generalized skills plus `secod-nextjs` | Unused cloud, payment, and AI providers |
| Native mobile without named framework | Android/iOS feature and mobile boundaries | `secod-mobile-app-security` plus applicable generalized skills | React Native/Expo, Flutter, and provider adapters |
| React Native/Expo | Expo or React Native package/config plus native feature | `secod-react-native-expo`, mobile baseline, and applicable generalized skills | Flutter and unused providers |
| Flutter mobile | Flutter project plus Android/iOS target | `secod-flutter`, mobile baseline, and applicable generalized skills | React Native/Expo and unused providers |
| Supabase Auth | Supabase SDK/config plus Auth signals | `secod-supabase`, `secod-supabase-auth`, and auth router | Other providers |
| AWS S3/CloudFront | AWS plus S3/CloudFront resources | `secod-aws-web` and `secod-aws-s3-cloudfront` | Other cloud providers |
| Google Cloud without Firebase | Google Cloud project/service identity; no Firebase signal | `secod-google-cloud-web` | `secod-firebase` |
| Static Cloudflare Pages | Pages deployment; no Functions or Workers binding | `secod-cloudflare` and `secod-cloudflare-pages` | Workers and unused providers |
| Cloudflare Workers AI | Workers plus Workers AI binding | Cloudflare, Workers, Workers AI, and AI baseline | Unused AI/cloud providers |
| Vercel without AI | Vercel deployment; no AI SDK or model call | `secod-vercel-platform` | `secod-vercel-ai` |
| Stripe and OpenAI | Stripe billing plus OpenAI calls | payment/AI baselines, Stripe, and OpenAI | Other payment/AI providers |

`python scripts/test_dependency_routing.py` exercises every catalog entry as a route root. It
checks unknown dependencies, cycles, transitive closure, core inclusion, and exact provider
selection for representative stacks. It also asserts every provider/framework adapter remains
unselected when only generalized skills are routed. It does not inspect application security or
prove that an agent host detected every stack signal correctly.
