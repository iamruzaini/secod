# Expected result: secod-inputs-apis

The agent defines schemas at the trust boundary, rejects unknown or oversized input, authorizes
server-side, avoids shell/string interpolation, and constrains URL scheme, host, resolved address,
redirects, timeout, and response size. Negative tests prove malformed, unauthorized, and private
network requests are rejected. No post-hoc finding report replaces implementation.
