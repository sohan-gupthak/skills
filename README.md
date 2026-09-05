# Agent Skills

[![skills.sh](https://skills.sh/b/sohan-gupthak/skills)](https://skills.sh/sohan-gupthak/skills)

Reusable skills for coding agents.

This repository currently provides the **`evidence-gated-agent`** skill, an evidence-first workflow for consequential repository changes and completion claims.

## Available Skills

### `evidence-gated-agent`

Use this skill when a coding agent is about to:

- make a consequential repository change; or
- declare a consequential repository change complete.

The workflow covers risk classification, claim-specific evidence contracts, pre-change baselines, scope control, human approval checkpoints for high-risk actions, static vs runtime evidence, verification integrity, and completion gates.

## Installation

### Install all skills

```bash
npx skills add https://github.com/sohan-gupthak/skills
```

### Install only `evidence-gated-agent`

```bash
npx skills add https://github.com/sohan-gupthak/skills --skill evidence-gated-agent
```

## Skill Structure

```text
skills/
└── evidence-gated-agent/
    ├── SKILL.md
    └── references/
        └── high-risk-domains.md
```

- `SKILL.md` contains the universal evidence-gating workflow.
- `references/high-risk-domains.md` provides additional evidence requirements for public API/contract changes, authentication and authorization, payments/financial operations, and schema migrations/destructive operations.

## Evidence-Gating Model

The skill uses these principal dispositions:

- `ALLOW`
- `ALLOW_WITH_VERIFICATION`
- `CHECKPOINT`
- `BLOCKED_EVIDENCE`
- `BLOCKED_CLARIFICATION`

Verification results are explicitly classified as:

- `PASS`
- `FAIL`
- `UNVERIFIED`
- `PREEXISTING_FAILURE`
- `BLOCKED_EVIDENCE`

`COMPLETE` is reserved for cases where the completion gate has actually been satisfied.

## Key Principles

1. **Evidence before completion claims.** Implementation intent is not proof of behavior.
2. **Static and runtime evidence are different.** Source inspection cannot establish runtime behavior.
3. **Baseline before change.** Potentially pre-existing verification failures must be captured before modification.
4. **No silent scope expansion.** Related functionality is not automatically part of the requested change.
5. **High-risk actions require explicit checkpoints.** Approval must authorize the exact stated scope and verification plan.
6. **Failed mandatory verification remains failed.** Targeted or alternative checks do not replace a required repository-wide or runtime verification.
7. **Unverified claims cannot become completion claims.**

## Documentation for Coding Agents

Repository-specific agent guidance is maintained in [`AGENTS.md`](AGENTS.md).

For Claude Code, [`CLAUDE.md`](CLAUDE.md) intentionally contains only a pointer to `AGENTS.md`; the repository's instructions live in one authoritative location.

## Repository

GitHub: https://github.com/sohan-gupthak/skills
