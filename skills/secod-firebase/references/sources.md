# Official source register

| Source ID | Title | Source type | Direct official URL | Owner | Reviewed date | Refresh trigger | Status | Recipes or decisions supported | Assumptions/notes |
|---|---|---|---|---|---|---|---|---|---|
| FIREBASE-SRC-001 | Firebase Security Rules | Direct implementation guide | https://firebase.google.com/docs/rules | Google Firebase | 2026-09-06 | Rules or product change | Reviewed | firestore-rules.md; storage-rules.md | Exact products require product Rules syntax. |
| FIREBASE-SRC-002 | Build Security Rules unit tests | Direct testing guide | https://firebase.google.com/docs/rules/unit-tests | Google Firebase | 2026-09-06 | Emulator/testing API change | Reviewed | emulator-tests.md | Use supported rules-unit-testing version. |
| FIREBASE-SRC-003 | Add Firebase Admin SDK to server | Direct implementation guide | https://firebase.google.com/docs/admin/setup | Google Firebase | 2026-09-06 | Admin SDK setup change | Reviewed | admin-sdk-boundary.md | Managed runtimes may initialize differently. |
| FIREBASE-SRC-004 | Enable App Check enforcement | Direct deployment guide | https://firebase.google.com/docs/app-check/enable-enforcement | Google Firebase | 2026-09-06 | Product support or rollout change | Reviewed | auth-sessions.md; admin-sdk-boundary.md | App Check does not replace authorization. |
| FIREBASE-SRC-005 | Firebase documentation index | Official llms.txt | https://firebase.google.com/docs/llms.txt | Google Firebase |  | Index change | Pending review | Documentation discovery only | Index is not sole support for code. |
