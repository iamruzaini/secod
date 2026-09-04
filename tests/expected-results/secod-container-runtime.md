# Expected result: secod-container-runtime

The skill emits one finding per applicable control, redacts secret values, distinguishes repository
intent from admitted and running state, and correlates evidence by environment, workload,
deployment revision, and exact image digest.

Cluster-enforced admission, effective RBAC, NetworkPolicy enforcement, registry scan results,
deployed digests, and signature-policy activity remain `Not verified` without current scoped
external evidence. Policy objects alone do not prove enforcement, tag-keyed scans do not prove
digest coverage, and one admission event does not prove complete namespace coverage.

Baked build/runtime secrets or a production workload combining root execution with effective
`cluster-admin` produce `Do not ship`. Other findings follow documented thresholds. Output lists
blockers and routes final launch readiness to `secod-ship-check`; it never issues a launch verdict.
