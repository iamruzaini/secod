# SECOD Skill Authoring Templates

These templates turn the product direction in [`docs/PRD.md`](../docs/PRD.md) into a repeatable authoring system for SECOD skills.

SECOD skills are implementation guidance for AI coding agents. They should help an agent make secure design choices, write secure code, add meaningful tests, and follow official provider documentation while a feature is being built. They are not scanner rules, certification checklists, or mandatory finding reports.

## Template index

| Template | Use for |
|---|---|
| [`BASE-SKILL-TEMPLATE.md`](BASE-SKILL-TEMPLATE.md) | Shared structure and minimum contract for every SECOD skill |
| [`CORE-ROUTER-SKILL-TEMPLATE.md`](CORE-ROUTER-SKILL-TEMPLATE.md) | `secod-core`, which discovers task context and selects applicable skills |
| [`GENERALIZED-SKILL-TEMPLATE.md`](GENERALIZED-SKILL-TEMPLATE.md) | Portable security practices that apply across providers and frameworks |
| [`FRAMEWORK-SKILL-TEMPLATE.md`](FRAMEWORK-SKILL-TEMPLATE.md) | Framework-specific secure implementation guidance |
| [`PROVIDER-FAMILY-SKILL-TEMPLATE.md`](PROVIDER-FAMILY-SKILL-TEMPLATE.md) | Broad provider families that route to feature-specific adapters |
| [`PROVIDER-FEATURE-SKILL-TEMPLATE.md`](PROVIDER-FEATURE-SKILL-TEMPLATE.md) | A specific provider product, API, SDK, or integration |
| [`MOBILE-SKILL-TEMPLATE.md`](MOBILE-SKILL-TEMPLATE.md) | Mobile, React Native/Expo, Flutter, and device/backend boundaries |
| [`TASK-COMPLETION-SKILL-TEMPLATE.md`](TASK-COMPLETION-SKILL-TEMPLATE.md) | A scoped pre-completion check for the feature changed in the current task |
| [`IMPLEMENTATION-RECIPE-TEMPLATE.md`](IMPLEMENTATION-RECIPE-TEMPLATE.md) | Detailed language-, framework-, or provider-specific recipe under `references/` |
| [`SOURCE-REGISTER-TEMPLATE.md`](SOURCE-REGISTER-TEMPLATE.md) | Official source register under `references/sources.md` |
| [`BEHAVIOR-EVALUATION-TEMPLATE.md`](BEHAVIOR-EVALUATION-TEMPLATE.md) | Trigger, routing, implementation, and safety-boundary evaluation cases |
| [`SKILL-TEMPLATE-MATRIX.md`](SKILL-TEMPLATE-MATRIX.md) | Migration assignment for every current and planned SECOD skill |

None of these files is named `SKILL.md`. This prevents the Skills CLI from discovering the authoring templates as installable skills.

## Authoring sequence

1. Find the skill in `SKILL-TEMPLATE-MATRIX.md`.
2. Copy its assigned template to `skills/<skill-name>/SKILL.md`.
3. Replace every bracketed authoring placeholder and remove scaffold comments.
4. Add only the recipes needed for the skill. Put detailed conditional material in `references/`.
5. Populate `references/sources.md` with official documentation actually used to form the guidance.
6. Add behavior evaluations and, where practical, executable insecure/secure fixtures.
7. Run repository validation and confirm the Skills CLI still discovers only release-visible skills.

## Originality and source policy

These are original SECOD templates written from SECOD's PRD and the [Agent Skills specification](https://agentskills.io/specification). Their implementation-first structure is intentionally different from scanner- or audit-oriented templates.

General authoring ideas such as clear activation criteria, unsafe/safe examples, focused verification, and progressive disclosure are common techniques and have been expressed here in original SECOD wording. Do not paste substantial text from third-party templates into SECOD without preserving the applicable license notice and recording the source.

## Frontmatter rules

- Keep `name` and `description` valid under the Agent Skills specification.
- Put SECOD-specific fields inside `metadata`; do not invent unsupported top-level fields.
- Set `metadata.secod-format` to `implementation-v1` only after the skill satisfies the implementation-first contract. Skills without this field remain legacy during migration.
- Set `metadata.secod-category` to one of `router`, `generalized`, `framework`, `provider-family`, `provider-feature`, `mobile`, or `task-completion`.
- Set `metadata.secod-maturity` to `draft`, `provisional`, or `stable`.
- Add `compatibility` only when the skill has a real environment requirement.
- Add `allowed-tools` only when necessary, using a space-separated value supported by the target agent.
- Make the description state both the implementation outcome and the situations that should activate the skill.

## Writing boundary

Each skill should answer: “What should the coding agent implement now, and how should it prove the implementation behaves safely?”

It should not default to:

- a repository-wide audit;
- a list of findings or severity labels;
- a dashboard inspection unrelated to the coding task;
- a claim that the application passed, is secure, or is certified;
- `Not verified` as routine output.

When an implementation genuinely depends on inaccessible deployment state, state the exact unobserved setting and give the user a concrete verification step. Do not turn that caveat into the skill's main workflow.
