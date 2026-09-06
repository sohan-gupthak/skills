# Agent Skills

[![skills.sh](https://skills.sh/b/sohan-gupthak/skills)](https://skills.sh/sohan-gupthak/skills)

Reusable skills for coding agents.

This repository currently provides the **`evidence-gated-agent`** skill, an evidence-first workflow for consequential repository changes and completion claims. It now also includes an **Evidence Ledger** for persistent operational state on medium and high-risk work, and explicit **Evidence Freshness and Invalidation rules** so that persisted evidence can be re-evaluated when material changes affect the conditions on which it depended, without becoming permanently valid merely because it was once collected.

## Available Skills

### `evidence-gated-agent`

Use this skill when a coding agent is about to:

- make a consequential repository change; or
- declare a consequential repository change complete.

The workflow covers risk classification, claim-specific evidence contracts, pre-change baselines, scope control, human approval checkpoints for high-risk actions, static vs runtime evidence, verification integrity, completion gates, and evidence freshness and invalidation rules. Evidence carries a current validity state (`VALID`, `STALE`, `INVALIDATED`, `RE-VERIFIED`) and must be re-evaluated when a material change affects the conditions on which it depended. A completion claim must not rely on evidence whose current validity is `STALE` or `INVALIDATED` when that evidence supports a mandatory claim or verification requirement.

For medium and high-risk work, the agent should also maintain an **Evidence Ledger** at `.evidence-gated/active/<change-id>.md`. The ledger is the persistent operational record; the agent re-reads it before each material step and finalizes it at a terminal disposition. It is a record of evidence, not evidence itself: every claim still needs its own provenance chain.

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
        ├── high-risk-domains.md
        └── evidence-ledger.md
```

- `SKILL.md` contains the universal evidence-gating workflow, including the Evidence Ledger policy.
- `references/high-risk-domains.md` provides additional evidence requirements for public API/contract changes, authentication and authorization, payments/financial operations, and schema migrations/destructive operations.
- `references/evidence-ledger.md` is the Evidence Ledger reference: lifecycle, template, when the ledger is required, source-of-truth hierarchy, and the completion gate as it applies inside a ledger.

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
8. **Evidence is not permanently valid.** Persisted evidence carries a current validity state (`VALID`, `STALE`, `INVALIDATED`, `RE-VERIFIED`). Material changes to the conditions on which an evidence record depended require re-evaluation, and stale or invalidated evidence cannot support a mandatory completion claim. Historical records are preserved.

## Documentation for Coding Agents

Repository-specific agent guidance is maintained in [`AGENTS.md`](AGENTS.md).

For Claude Code, [`CLAUDE.md`](CLAUDE.md) intentionally contains only a pointer to `AGENTS.md`; the repository's instructions live in one authoritative location.

## Repository

GitHub: https://github.com/sohan-gupthak/skills
