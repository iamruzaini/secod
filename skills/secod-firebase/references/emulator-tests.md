# Firebase Emulator Suite tests

Use `@firebase/rules-unit-testing` and Rules loaded through `firebase.json`.

Required cases:

- authenticated owner/member succeeds;
- unauthenticated request fails;
- cross-tenant read and write fail;
- forbidden fields and path manipulation fail;
- wrong content type and oversized upload fail;
- Admin endpoint repeats application authorization;
- tests fail when Rules are absent or emulator is not connected.

Keep Emulator tests deterministic and isolated by project ID. Passing local Rules tests does not
prove deployed Rules or App Check configuration.
