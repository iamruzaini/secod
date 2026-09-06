# Implementation fixture plan: secod-failure-safety

Given an implementation that violates this skill's portable invariants, replace unsafe boundary with pattern in `references/secure-patterns.md` and add successful, rejected, boundary, retry, and failure tests where applicable.

Expected: Fail authorization closed, bound timeouts/retries, preserve invariants with transaction/compensation, and test injected failures.

This documentation plan is not scanner execution or proof of deployed behavior.
