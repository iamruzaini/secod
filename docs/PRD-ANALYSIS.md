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

They should receive independent Git remotes when the owner decision is made.
The website may project the skill catalog for discovery, but it must not become
the source of truth for skill metadata or releases.

## Core architectural decisions from the PRD

- Preserve the complete 57-skill catalog from the start. Do not represent an
  incomplete subset as SECOD v1.0.
- Keep the foundation, universal, and provider layers separate so each skill
  remains small, portable, and independently testable.
- Treat SECOD Core as a routing and planning skill, not as an implicit
  cross-skill executor.
- Keep agent-facing security instructions free of marketing, sponsors,
  credentials, and unrelated tutorial material.
- Make the Ship Check the only cross-project pre-launch decision surface.
- Preserve Not verified whenever a configuration or evidence source is absent.

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

The install configurator currently models the required inputs and output. It
deliberately displays an OWNER placeholder and a release warning until the
repository owner and agent adapter support are verified.

## Risks to resolve before implementation proceeds

1. GitHub organization, final repository URL, domain, hosting, and sponsor
   inventory remain open decisions.
2. Provider references must be based on current official documentation and
   carry a source URL plus reviewed date.
3. Marketplace metadata is only structurally present because the final
   repository location and supported distribution workflow are not chosen.
4. Scripts must remain read-only by default and must never transmit project
   content or credentials without explicit user approval.
5. The release gate requires real insecure fixtures, not only frontmatter
   validation or happy-path tests.
