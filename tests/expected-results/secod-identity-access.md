# Expected result: secod-identity-access

The agent implements a reusable server authorization boundary that derives identity from a
verified session, loads resource ownership from trusted storage, denies by default, and does not
trust browser-supplied roles or tenant identifiers. Tests cover authorized and denied paths.

If the identity provider, tenancy model, or session library version is missing, the agent asks for
or inspects that context before choosing provider APIs. It does not emit a scanner report or claim
that deployed identity settings were checked.
