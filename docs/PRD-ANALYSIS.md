# PRD analysis

## Product shape

SECOD is two related but separate deployable products:

1. The canonical skills repository, which owns skill metadata, references,
   release tags, testing, and distribution contracts.
2. The website, which handles discovery, guided installation, education,
   sponsors, and user-facing release information.

The products therefore use separate repositories:

- secod is the standalone canonical skills repository.
- The Bun-managed Next.js website imports versioned catalog data from a SECOD
  release.

They have independent ownership boundaries: `iamruzaini/secod` is the public
canonical skills repository, while the separate website repository imports
immutable SECOD releases.
The website may project the skill catalog for discovery, but it must not become
the source of truth for skill metadata or releases.

## Core architectural decisions from the PRD

- Preserve the original 57-skill migration inventory. The current catalog has
  60 `implementation-v1` skills after adding mobile, React Native/Expo, and
  Flutter coverage; the published count must come from the generated catalog.
- Keep the foundation, universal, and provider layers separate so each skill
  remains small, portable, and independently testable.
- Treat SECOD Core as a routing and planning skill, not as an implicit
  cross-skill executor.
- Keep agent-facing security instructions free of marketing, sponsors,
  credentials, and unrelated tutorial material.
- Make the Ship Check the only cross-project pre-launch decision surface.
- Continue repository-owned implementation when external configuration is absent; name exact
  uninspected setting and verification step without inventing its state.

## Website information architecture

The Next.js App Router scaffold includes all PRD-required routes:

- /
- /install
- /skills
- /skills/[skill]
- /providers/[provider]
- /methodology
- /docs
- /security
- /changelog
- /sponsor

The install configurator models the required inputs and output. The website
imports the generated 60-skill catalog and uses `iamruzaini/secod`; release
status must remain pre-release until supported agent installation is verified.

## Risks to resolve before implementation proceeds

1. Website domain, hosting, and sponsor inventory remain open decisions.
2. Provider references must be based on current official documentation and
   carry a source URL plus reviewed date.
3. Marketplace metadata is only structurally present; supported-agent release
   verification and final marketplace entries remain incomplete.
4. Scripts must remain read-only by default and must never transmit project
   content or credentials without explicit user approval.
5. The release gate requires real insecure fixtures, not only frontmatter
   validation or happy-path tests.
