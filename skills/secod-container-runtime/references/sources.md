# Source register: secod-container-runtime

Official documentation indexes are discovery snapshots only. Security-critical claims must be
verified against the direct primary source; refresh each entry before its review-expiry date.

| ID | Title | Direct URL | Owner | Reviewed | Expiry / refresh trigger | Status | Controls | Assumptions |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S1 | Kubernetes Security Checklist | https://kubernetes.io/docs/concepts/security/security-checklist/ | Kubernetes (CNCF) | 2026-08-26 | 2026-11-26 or page change | Reviewed | CRT-01, 02, 04, 05, 06, 07, 09, 10 | Self-managed or managed Kubernetes; checklist is version-current guidance, not a version guarantee |
| S2 | Docker build secrets | https://docs.docker.com/build/building/secrets/ | Docker Inc | 2026-08-26 | 2026-11-26 or page change | Reviewed | CRT-03, 08 | BuildKit-enabled builds; secret/SSH mount syntax current at review date |
| S3 | Pod Security Standards | https://kubernetes.io/docs/concepts/security/pod-security-standards/ | Kubernetes (CNCF) | 2026-08-26 | 2026-11-26 or page change | Reviewed | CRT-04, 05, 09 | `restricted` profile field rules (runAsNonRoot, allowPrivilegeEscalation, seccompProfile, capabilities) as of review date |
| S4 | Docker `llms-full.txt` | https://docs.docker.com/llms-full.txt | Docker Inc | — | On use | Pending review | discovery only | Snapshot for documentation discovery; never sole evidence for any control |

Verified claims at review: build args and environment variables persist in the final image and
are inappropriate for secrets (S2); secret mounts (`--mount=type=secret[,target=|env=]`) and
SSH mounts are the supported alternatives (S2); restricted-profile fields for
`allowPrivilegeEscalation`, `runAsNonRoot`, `seccompProfile` (`RuntimeDefault`/`Localhost`,
never `Unconfined`) and capability adds (S3); Pod Security admission enforce/warn/audit modes,
`RuntimeDefault` default seccomp since Kubernetes 1.27, `automountServiceAccountToken: false`
guidance, RBAC granularity limits, NetworkPolicy provider dependency (S1).

Mark affected controls **Not verified** when required source evidence is missing, stale,
contradictory, inaccessible, snapshot-only, or unsupported. Record version, ETag/hash where
obtainable on next refresh.
