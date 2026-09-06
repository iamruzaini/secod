# Expected result: secod-email-messaging

Generate purpose-bound tokens, store verifiers safely, prevent enumeration, constrain redirects, rate-limit, and test replay.

Missing context: Provider, identity binding, expiry, redirect policy, or delivery behavior is unclear; inspect before choosing SDK calls.

Rejected behavior: Never use reusable codes, caller-controlled recipients, or sensitive URL/template data.
