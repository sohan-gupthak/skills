# Agent Instructions

## Repository

This repository contains reusable agent skills. The current skill is **`evidence-gated-agent`**, a coding-agent workflow for consequential repository changes and repository completion claims.

Repository: https://github.com/sohan-gupthak/skills
Default branch: `main`

## Skill Location

```text
skills/evidence-gated-agent/
├── SKILL.md
└── references/
    └── high-risk-domains.md
```

## Installation

Install all skills from this repository:

```bash
npx skills add https://github.com/sohan-gupthak/skills
```

Install only the `evidence-gated-agent` skill:

```bash
npx skills add https://github.com/sohan-gupthak/skills --skill evidence-gated-agent
```

## Purpose

`evidence-gated-agent` is an evidence-first control process for consequential coding-agent work. It separates requested actions from assumptions, classifies risk, defines evidence for decision-relevant claims, gathers proportional evidence, establishes the pre-change state, controls scope, and requires claim-appropriate verification before a change can be reported as complete.

The skill should be used when a coding agent is about to make a consequential repository change or declare a repository change complete.

## Core Workflow

For consequential repository changes or completion claims, follow these stages in order.

### 1. Separate the requested action from assumptions

Identify the requested action and all material assumptions.

If ambiguity could change behavior, scope, safety, or the solution, stop with:

```text
BLOCKED_CLARIFICATION
```

Unblock only with the smallest authoritative clarification that resolves the ambiguity.

### 2. Classify risk

Classify the action as `low`, `medium`, or `high` risk using the discovered context.

Consider:

- public/shared surface;
- behavioral impact;
- data impact;
- security impact;
- financial impact;
- production impact;
- reversibility;
- dependencies;
- observability.

### 3. Build a claim-specific evidence contract

Define:

- current scope;
- decision-relevant claims;
- evidence required for each claim;
- consequence if a claim is unsupported;
- whether each mandatory verification requires `static` or `runtime` evidence.

For public API/contract changes, authentication/authorization, payments/financial operations, schema migrations, or destructive operations, consult:

```text
skills/evidence-gated-agent/references/high-risk-domains.md
```

### 4. Gather proportional evidence

Prefer repository artifacts and executable observations.

Record provenance in this form:

```text
claim -> observed fact -> artifact or command result -> method -> limitation
```

For every mandatory verification that may already be failing, capture a baseline before making any change.

### 5. Resolve the pre-change state

Use one of these dispositions:

- `BLOCKED_EVIDENCE` — required factual evidence is absent, conflicting, or unavailable.
- `ALLOW` — a supported low-risk action may proceed.
- `ALLOW_WITH_VERIFICATION` — a supported medium-risk action may proceed, with the stated verification required before completion.
- `CHECKPOINT` — a supported high-risk action requires explicit human approval before execution.

A mandatory verification that is already known to be impossible must not remain both mandatory and knowingly impossible.

Either:

- obtain authorization to expand scope and reclassify; or
- explicitly redefine the verification contract so the gate is no longer mandatory and record the limitation.

### 6. Execute only the authorized scope

Do not expand scope merely because adjacent components, transports, dependencies, or subsystems are related.

Distinguish:

1. functionality explicitly requested for removal;
2. functionality technically required by the removed feature;
3. functionality merely adjacent to or historically associated with the removed feature.

Only remove adjacent functionality when repository evidence shows it is unused, incompatible with the authorized change, or explicitly included in scope.

If related functionality can remain operational without the removed feature, preserve it unless its removal is authorized.

If the user changes an approved or checkpointed plan, re-evaluate dependent claims, evidence, risks, destructive consequences, and verification requirements instead of simply editing the existing plan.

Do not modify unrelated pre-existing code merely to make a required verification pass. Report the unrelated failure, explain why it is pre-existing, explain why fixing it would expand scope, and state what verification remains possible.

### 7. Run the post-change evidence gate

`COMPLETE` is only valid when mandatory verification has passed and the required post-change claims are supported.

A pre-existing failure can remain outside the authorized scope, but it is never a passing verification.

## Checkpoints and Human Approval

For a `CHECKPOINT`, use exactly this approval record shape:

```text
CHECKPOINT APPROVAL REQUIRED

Approval covers:
- <concrete action 1>
- <concrete action 2>
- ...

Irreversible consequences:
- <concrete consequence that cannot be undone>
- <concrete consequence that cannot be undone>
- ...

Required verification:
- <observation or command result that must hold before completion>
- <observation or command result that must hold before completion>
- ...

Reply APPROVE to authorize exactly the actions above.
```

Generic phrases such as `go ahead`, `your call`, `do what's best`, or `use your judgment` are not sufficient authorization.

Approval applies only to the exact stated scope. It does not authorize scope changes, relaxed evidence requirements, or unsupported completion claims.

## Verification Status Taxonomy

Use these statuses consistently:

| Status | Meaning |
|---|---|
| `PASS` | Required evidence succeeded. |
| `FAIL` | Verification was executed and failed. |
| `UNVERIFIED` | Verification could not establish the claim. |
| `PREEXISTING_FAILURE` | The same mandatory verification still fails with the exact pre-change failure set and no new failures. |
| `BLOCKED_EVIDENCE` | Required evidence is missing, conflicting, or unavailable. |
| `BLOCKED_CLARIFICATION` | User intent is materially ambiguous. |
| `CHECKPOINT` | High-risk action is supported but requires explicit human approval. |
| `COMPLETE` | All completion-gate requirements are satisfied. |

`COMPLETE` must never be assigned while a mandatory verification is `UNVERIFIED`, `FAIL`, or otherwise unresolved.

## Static vs Runtime Evidence

`static` evidence includes source inspection, grep, type checking, and configuration inspection.

Static evidence can establish facts about source or configuration, but it cannot prove runtime behavior.

`runtime` evidence requires actually executing the relevant application or path and observing the behavior.

Runtime claims must therefore be supported by runtime observations. If runtime verification cannot be performed, report the claim as `UNVERIFIED`, not `PASS` or `COMPLETE`.

## Baseline-vs-Post-Change Rule

For every mandatory verification that may already be failing:

1. Run it before the change and capture the baseline verbatim, including the exact failures and exit code.
2. Run the same command after the change.
3. Compare the failure sets.
4. Use `PASS` only when the verification succeeds.
5. Use `PREEXISTING_FAILURE` only when the post-change failures are demonstrably identical to the baseline and no new failures were introduced.
6. Use `FAIL` / `BLOCKED_EVIDENCE` when new or different failures appear.
7. Use `UNVERIFIED` / `BLOCKED_EVIDENCE` when the baseline or comparison cannot be established reliably.

Do not claim “zero new errors” without before/after evidence.

Example:

```text
Baseline: frontend tsc -b -> 8 errors in ContactRequests.tsx
Post-change: frontend tsc -b -> same 8 errors in ContactRequests.tsx
Result: PREEXISTING_FAILURE
```

If post-change introduces a ninth error, the verification is `FAIL` / `BLOCKED_EVIDENCE`.

## Verification Integrity

Evaluate every required verification exactly as defined in the active evidence contract.

Do not replace, weaken, narrow, reinterpret, or downgrade a failed required verification after execution.

Examples:

- Repository-wide `tsc` failing is not satisfied by compiling only edited files.
- A failing production build is not satisfied by source inspection.
- An unexecuted runtime smoke test is not satisfied by static analysis.

Alternative or targeted checks may be reported as supplementary evidence, but they do not replace a failed or unverified mandatory gate.

## Impossible Mandatory Gates

Before execution, inspect every mandatory verification.

If one can only be passed through an out-of-scope change, do not knowingly proceed while keeping it mandatory.

Either:

- obtain authorization to expand scope and reclassify; or
- explicitly redefine the verification contract so the gate is no longer mandatory and record the limitation.

Never call a plan `COMPLETE` when it knowingly contains an impossible mandatory verification.

## Unrelated Failures and Scope Control

If an unrelated pre-existing compile/test/build failure prevents verification, do not modify unrelated code merely to make the verification pass.

Report:

- the unrelated failure;
- why it is pre-existing;
- why fixing it would expand scope;
- what verification remains possible without fixing it.

## High-Risk Domains

The repository's `references/high-risk-domains.md` supplements the universal protocol for selected high-risk changes.

### Public API / contract changes

Establish:

- the current contract;
- known consumers;
- compatibility policy;
- tests covering the changed surface.

A handler unit test alone does not establish that no consumer depends on a removed field.

### Authentication and authorization

Establish:

- the current authentication/session flow;
- authorization boundary;
- invalid, expired, and missing-credential behavior;
- token/session invalidation semantics when relevant;
- privilege-escalation surface.

### Payments and financial operations

Establish:

- transaction flow;
- provider semantics for idempotency;
- retry behavior;
- webhook delivery behavior;
- duplicate-charge/double-processing prevention;
- failed or partial-operation recovery behavior.

### Schema migrations and destructive operations

Establish:

- rollback reversibility with an exercised rollback path;
- data-loss and recovery surface;
- partial-failure safety;
- blast radius for other systems using the resource.

## Postconditions and Completion

Every material postcondition explicitly authorized by a checkpoint must be demonstrated by post-change evidence or reported as unverified.

Implementation intent, source-code presence, or an unexecuted code path is not proof of a runtime postcondition.

`COMPLETE` is allowed only when:

- the authorized change was actually executed;
- every mandatory post-change claim has sufficient evidence and provenance;
- every mandatory verification is `PASS` or a properly evidenced `PREEXISTING_FAILURE`;
- no evidence contradiction remains;
- no required claim is merely assumed;
- no unauthorized scope expansion occurred.

If any mandatory verification is `UNVERIFIED`, `FAIL`, or otherwise unresolved, or if the baseline comparison required for `PREEXISTING_FAILURE` is missing, the final disposition is `BLOCKED_EVIDENCE`.

## Final Reporting

The terminal report should state:

1. action;
2. scope and risk;
3. disposition/state;
4. claims with provenance;
5. limitations and missing/conflicting evidence;
6. authorized next action;
7. required verification.

The final report is the terminal disposition of the authorized action and does not silently restart the evidence-gate cycle.

## Repository Change Guidance

When modifying this repository itself:

- preserve the existing `skills/evidence-gated-agent/` structure unless the requested change explicitly requires otherwise;
- keep the universal workflow in `SKILL.md` and domain-specific evidence requirements in `references/high-risk-domains.md`;
- do not add claims about the skill that are not supported by the skill source or repository contents;
- verify documentation and repository state before declaring documentation work complete.
