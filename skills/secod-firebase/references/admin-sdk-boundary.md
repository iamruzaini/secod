# Firebase Admin SDK boundary

Initialize Admin SDK only in trusted server or Function runtime. Prefer Application Default
Credentials on managed infrastructure:

```ts
import { applicationDefault, getApps, initializeApp } from "firebase-admin/app";

export const adminApp =
  getApps()[0] ?? initializeApp({ credential: applicationDefault() });
```

Admin SDK bypasses Security Rules. Before every Admin read or write, verify caller identity and
authorize tenant, resource, and action against server-owned state. Never bundle service-account
credentials into web or mobile code.
