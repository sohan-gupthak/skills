---
name: evidence-gated-agent
description: Use when a coding agent is about to make a consequential repository change or declare a repository change complete.
---

# Evidence-Gated Agent

For a consequential repository change or completion claim, use this sequence:

1. Separate the requested action from material assumptions. If ambiguity could change behavior, scope, safety, or solution, issue `BLOCKED_CLARIFICATION`; it is unblocked by the smallest authoritative clarification that resolves it.
2. Classify the action in its discovered context as low, medium, or high risk. Consider public/shared surface, behavioral, data, security, financial, and production impact, reversibility, dependencies, and observability.
3. Create a claim-specific evidence contract: current scope, decision-relevant claims, evidence needed for each claim, and the consequence if a claim is unsupported. For public API, auth/authorization, payments, migrations, or destructive operations, use [high-risk domains](references/high-risk-domains.md) while building that contract. For every mandatory verification, classify the evidence as `static` (source inspection, grep, type checking, configuration inspection) or `runtime` (actually executing the application and observing behavior). A source-level check is not proof of runtime behavior; a runtime claim must be supported by an actual executed observation. When a work item is required or chosen to be tracked by an Evidence Ledger under the risk-tiered policy in [references/evidence-ledger.md](references/evidence-ledger.md), record the contract in the active ledger so it survives context loss.
4. Gather proportional evidence. Prefer repository artifacts and executable observations; use deterministic analysis where appropriate. Record provenance as `claim -> observed fact -> artifact or command result -> method -> limitation`. For mandatory verifications, capture a baseline run before any change so a later pre-existing failure can be compared against it instead of assumed. Baseline and evidence records live in the active Evidence Ledger whenever a ledger is in use for this change.
5. Resolve the pre-change state:
   - `BLOCKED_EVIDENCE` when required factual evidence is absent, conflicting, or unavailable. It is unblocked by the required factual evidence, investigation/remediation that resolves the conflict, or an authorized narrower action. If a mandatory gate is already known to be impossible to pass without an out-of-scope change, do not proceed while declaring that gate mandatory: either obtain authorization to expand scope and reclassify, or explicitly redefine the verification contract so the gate is no longer mandatory, with the limitation recorded.
   - `ALLOW` when a supported low-risk action may proceed.
   - `ALLOW_WITH_VERIFICATION` when a supported medium-risk action may proceed with its stated verification required before completion.
   - `CHECKPOINT` when a supported high-risk action needs explicit human approval of the planned action, evidence, limitations, and verification plan. `CHECKPOINT` is not permission to act; explicit approval is required. For every `CHECKPOINT`, present the action as a written approval record the human signs. Use exactly this shape and the section labels `Approval covers`, `Irreversible consequences`, and `Required verification`; do not omit any of them. A "Reply APPROVE" or "your call" answer that does not match this record line-for-line is not authorization for the action; re-present the record or return `BLOCKED_CLARIFICATION`. Approval authorizes execution of the stated scope; it does not authorize changing the scope, relaxing evidence requirements, or accepting unsupported post-change claims.

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

6. Make only the authorized scoped change. If scope expands, reclassify risk, revise the evidence contract, and return to the pre-change state. When a user modifies an approved or checkpointed plan, do not merely update the plan. Re-evaluate all dependent claims, evidence, risks, destructive consequences, and verification requirements affected by the modification. Do not convert an absence of deletion into a claim that retained data remains usable or readable. Preservation of bytes is not preservation of semantics.

   Do not expand the requested scope merely because a component, transport, dependency, or subsystem is related to the changed behavior. Distinguish: functionality explicitly requested for removal; functionality technically required by the removed feature; functionality merely adjacent to or historically associated with the removed feature. Only remove adjacent functionality when repository evidence establishes that it is unused, incompatible with the authorized change, or explicitly included in the requested scope. When functionality can remain operational without the removed feature, preserve it unless the user authorizes its removal.

   If an unrelated pre-existing compile/test/build failure prevents verification, do not modify unrelated code merely to make the verification pass. Instead, report: the unrelated failure, why it is pre-existing, why fixing it would expand scope, and what verification remains possible without fixing it.
7. Verify claims proportionally to the action and observed behavior. Run the post-change evidence gate: `COMPLETE` follows only when mandatory verification passed and the required post-change claims are supported.
A pre-existing failure may be excluded from scope, but it cannot be represented as a passing verification. Report the verification as `UNVERIFIABLE` / `BLOCKED_EVIDENCE` and distinguish targeted checks from repository-wide verification.

Missing required factual evidence remains `BLOCKED_EVIDENCE`. An inability to execute a required verification is also insufficient evidence for `COMPLETE`; report the verification as `UNVERIFIED` or `FAILED` and keep the overall disposition `BLOCKED_EVIDENCE` when that verification is mandatory.
Generic approval phrases ("go ahead", "your call", "do what's best", "use your judgment", or similar) are not authorization for a `CHECKPOINT` action. Explicit approval must name the specific action, evidence, limitations, and verification plan. If authorization remains ambiguous, return `BLOCKED_CLARIFICATION` with the smallest authoritative question that resolves it.
When no applicable policy requires the absent property, a human can choose a narrower action or accept an established adverse risk; approval never makes an unsupported factual claim true. A verification contradiction or an unverified required post-change claim returns to `BLOCKED_EVIDENCE` for investigation/remediation.

## Evidence Ledger for persistent state

For medium and high-risk work, the operational state of an active change must persist beyond conversation context. The Evidence Ledger is the persistent record. It is the same Markdown reference, the same status taxonomy, the same provenance chain, and the same completion gate as the rest of this skill, applied to a per-change document.

### The ledger is a record, not evidence

Writing a claim in a ledger does not make it true. A ledger entry must preserve provenance, exactly as the rest of this skill does. `PASS` in a ledger means a recorded observation that, on its own terms, supports the claim; the record is not stronger than the observation. A bare assertion with no observation, artifact, method, or limitation is `UNVERIFIED`, no matter where it is written.

### When a ledger is required

Use the existing risk classification:

- `LOW` risk: ledger is optional. A local variable rename, isolated typo fix, or non-consequential documentation correction does not need one.
- `MEDIUM` risk: ledger is recommended when the change involves meaningful evidence tracking, multiple verification steps, or work that may span multiple investigation or execution phases.
- `HIGH` risk: ledger is mandatory. Public API or contract changes, authentication, authorization, payments, financial operations, schema migrations, destructive operations, irreversible actions, and significant production impact all require one.

### Where a ledger lives

Default location: `.evidence-gated/active/<change-id>.md`, with completed ledgers moved to `.evidence-gated/archive/<change-id>.md`. The default is a working-state directory, not part of the published repository: add `.evidence-gated/active/` to `.gitignore` for new projects unless the user or repository conventions say otherwise. repository conventions and explicit user instructions take precedence; the agent must not silently modify `.gitignore` merely because the skill uses a ledger, and must not commit an active ledger without authorization.
If the change is particularly high-risk, the user explicitly requests an audit trail, or repository conventions require persistent documentation, the ledger may be committed intentionally and named accordingly (for example, `docs/evidence-gated/<change-id>.md`).

### Ledger lifecycle

1. Determine whether a ledger is required based on the risk classification above.
2. Locate an existing active ledger before creating a new one; do not create multiple ledgers for the same active change.
3. Read the active ledger before continuing. Re-read it before: a new investigation phase, a significant change execution, requesting checkpoint approval, acting on an approval, any scope change, any verification requirement change, and any completion claim. The re-read must confirm the current requested action, authorized scope, risk, active assumptions, mandatory claims, mandatory verification, checkpoint state, approval state, known limitations, and current disposition. Do not rely on memory for any of these.
4. Update the ledger when material facts change: risk, scope, assumptions, evidence, verification requirements, baseline, checkpoint state, approval state, execution state, verification results, final disposition.
5. Finalize the ledger at a terminal disposition: `COMPLETE`, `BLOCKED_EVIDENCE`, or `BLOCKED_CLARIFICATION`. A ledger implying `COMPLETE` while mandatory claims remain unresolved is invalid and must be rewritten or returned to the appropriate unblock condition.

### Required content

The active ledger must contain at minimum: change id and current status, requested action, authorized scope, explicitly out-of-scope items, scope limitations and unknowns, risk classification with reasons, material assumptions with status and supporting evidence or limitation, the evidence contract (one entry per decision-relevant claim with required evidence, evidence type, consequence if unsupported, and status), evidence records (one per significant item, preserving `claim -> observed fact -> artifact or command result -> method -> limitation -> status`), baseline verification, checkpoint state, execution log for material state transitions, verification record for every mandatory verification, and a limitations/missing/conflicting/unresolved section.

### Phases and dispositions

The ledger header carries two distinct fields. Do not conflate them.

**Operational Phase** describes what the agent is currently doing with the change, in the order work proceeds. The phases are `DRAFT` (ledger created, contract not yet written), `INVESTIGATING` (gathering evidence, capturing baseline, resolving assumptions), `EXECUTING` (authorized scoped change in progress), `VERIFYING` (post-change verification and finalization). Phases are bookkeeping. They do not authorize anything; they do not block anything; they do not count as evidence. A phase transition without the corresponding disposition change is not a change in authorization.

**Disposition** is the gate-level decision from the universal protocol. The dispositions are exactly the six canonical states of this skill: `BLOCKED_CLARIFICATION`, `BLOCKED_EVIDENCE`, `ALLOW`, `ALLOW_WITH_VERIFICATION`, `CHECKPOINT`, `COMPLETE`. The disposition is what authorizes execution, gates verification, and finalizes the change. At finalization, the ledger disposition must be one of these six. Intermediate phases are not a substitute for a disposition.

The same change can be in `EXECUTING` phase and `ALLOW_WITH_VERIFICATION` disposition at the same time. The same change can be in `INVESTIGATING` phase and `BLOCKED_EVIDENCE` disposition at the same time. Conflating them makes authorization unclear and hides the gate; do not do it.

### Approval and scope rules apply inside the ledger

Generic approval phrases ("go ahead", "your call", "do what's best", "use your judgment") are not authorization when recorded in a ledger any more than they are in conversation. Approval in the ledger must be tied to the same `CHECKPOINT APPROVAL REQUIRED` record used by the rest of this skill. Discovering that another component is related to the change is not new authorization. A new evidence finding is not a new scope. When scope materially changes: record the proposed change, identify affected claims and verifications, re-evaluate risk, determine whether new authorization is required, update the ledger, and do not execute unauthorized expanded scope.

### Source of truth hierarchy

Authority depends on what is being established. The skill is fundamentally about evidence-gated factual claims, so a user assertion about a factual matter is not a substitute for that evidence. The hierarchy is two-axis:

For intent, authorization, desired scope, and acceptable tradeoffs:

1. Explicit user instruction or approval.

For factual repository state, runtime behavior, and verification results:

1. Direct repository and runtime evidence, including command output for executed verification.
2. Recorded Evidence Ledger, as a record of that evidence.
3. Agent memory or conversation context.

The Evidence Ledger never overrides its underlying source evidence, and user assertions about factual matters are not promoted to fact by being recorded. If the ledger conflicts with current repository evidence or explicit user instructions: identify the contradiction, do not silently choose one, update the ledger only after resolving or explicitly recording the conflict.


## Evidence freshness and invalidation

Evidence establishes a claim only relative to the state, assumptions, artifacts, and conditions under which it was obtained. Persisted evidence is not permanently valid: when a material change affects the conditions on which an evidence record depended, the affected evidence must be re-evaluated before being relied upon for a consequential decision or completion claim. Freshness is primarily about state dependency, not about age or wall-clock time; an inspection performed moments ago can already be stale, and an inspection performed earlier can still be `VALID` if the relevant state has not changed.

A material change is one with a reasonable connection to the conditions required for an evidence record to support its claim. Examples include changes to relevant source code, schemas, configuration, contracts, migrations, or infrastructure definitions; changes to assumptions such as consumer, data, authorization, or environment assumptions; scope expansion that brings previously out-of-scope components into relevance; relevant dependency or contract changes; verification-condition changes such as environment, fixture, or relevant configuration changes; and new evidence that contradicts prior evidence. Do not require a re-evaluation for changes with no reasonable connection to any active evidence record; an unrelated typo fix must not invalidate unrelated API compatibility evidence.

Evidence validity in this skill follows four states. `VALID` means the evidence is currently applicable to its claim based on known state. `STALE` means something relevant has changed but the effect has not yet been fully determined; re-evaluation is required before relying on this evidence. `INVALIDATED` means a known change directly undermines the conditions under which the evidence was obtained; the evidence can no longer be relied upon for its claim. `RE-VERIFIED` means evidence that was `STALE` or `INVALIDATED` has been re-established against the current state, with its own provenance recorded. `RE-VERIFIED` does not retroactively erase the prior `STALE` or `INVALIDATED` state; the chain must be preserved.

When a potentially material change occurs, the agent must identify which existing claims depend on what changed, identify the supporting evidence for each affected claim, classify the evidence as `VALID`, `STALE`, or `INVALIDATED`, record the reason (what changed, why it affects this evidence, which claim is affected), determine whether re-verification is mandatory based on risk level, consequence of relying on stale evidence, and whether the evidence supports a mandatory gate or completion claim, gather new evidence against the current state when required, and preserve history. Historical evidence must not be silently deleted or overwritten.

A completion claim must not rely on evidence known to be `STALE` or `INVALIDATED` when that evidence supports a mandatory claim or verification requirement. Historical baseline evidence is preserved as a record of the pre-change state; it does not become invalid merely because time passed, and it is distinct from current post-change verification evidence. Static and runtime evidence remain distinct kinds: fresh static evidence does not substitute for required fresh runtime evidence.

Freshness does not silently invalidate user authorization. A technical verification becoming stale is not the same as the approved scope no longer covering the new action. When a material change invalidates a critical assumption behind an approval such that the understood consequences have materially changed, the agent must record the new fact, reassess scope and consequences, determine whether the existing approval still covers the action, and request a new checkpoint if necessary.

Detailed validity state definitions, dependency tracking, material-change detection, re-evaluation procedure, and the ledger template fields for freshness tracking live in [references/evidence-ledger.md](references/evidence-ledger.md).

## Verification status taxonomy


Use these terms consistently and never silently convert one into another:

- `PASS` — required evidence succeeded.
- `FAIL` — verification was executed and failed.
- `UNVERIFIED` — verification could not establish the claim (e.g., unable to run, environment missing, observation not made).
- `PREEXISTING_FAILURE` — verification fails due to an independently captured baseline failure, with no new failures introduced. The baseline must be captured before the change; the post-change run must be the same command, and the failure set must be demonstrably identical.
- `BLOCKED_EVIDENCE` — required evidence is missing, conflicting, or unavailable.
- `BLOCKED_CLARIFICATION` — user intent is materially ambiguous.
- `CHECKPOINT` — high-risk action is sufficiently supported but explicit human approval is still required.
- `COMPLETE` — only after the completion gate succeeds; never assigned when any mandatory verification is `UNVERIFIED`, `FAIL`, or otherwise unresolved.

## Static vs runtime evidence

A claim is only as strong as its evidence kind. `static` evidence (source inspection, grep, type checking, configuration inspection) can establish that code is present, removed, or shaped in a particular way; it cannot establish that a runtime behavior occurred. `runtime` evidence (actually executing the application or its relevant path and observing the result) is required to establish runtime claims such as "the relevant storage keys are absent after the cleanup path runs" or "the API returns the documented payload under load." A source-level check is not a substitute for a required runtime observation; if runtime verification cannot be performed, the claim is `UNVERIFIED`, not `PASS` or `COMPLETE`.

## Baseline-vs-post-change rule for pre-existing failures

For every mandatory verification that may already be failing before the requested change:

1. Before making changes, run the verification and capture the baseline result verbatim, including the exact set of failures (file paths, error codes, exit code).
2. After the change, run the same verification with the same command and capture the post-change result.
3. Compare the post-change failures to the baseline. The agent may claim:
   - `PASS` only when the verification succeeds.
   - `PREEXISTING_FAILURE` only when the command still fails, the exact failures are demonstrably identical to the captured baseline, and no new failures were introduced.
   - `FAIL` / `BLOCKED_EVIDENCE` when the post-change result introduces new failures or otherwise differs from the baseline in failure set or exit code.
   - `UNVERIFIED` / `BLOCKED_EVIDENCE` when the baseline cannot be established or the comparison cannot reliably be made.
4. Do not allow statements such as "zero new errors" merely because an error was previously described as pre-existing. Before/after evidence is required.

Example:

> Baseline: `frontend tsc -b` → 8 errors in `ContactRequests.tsx`.
> Post-change: `frontend tsc -b` → same 8 errors in `ContactRequests.tsx`.
> Result: `PREEXISTING_FAILURE`, not `PASS`.
> If post-change produces 9 errors, including one caused by the requested work: `FAIL` / `BLOCKED_EVIDENCE`.

## Verification integrity

A required verification must be evaluated exactly as defined in the active evidence contract. The agent must not replace, weaken, narrow, reinterpret, or downgrade a failed required verification with a different verification after execution. If repository-wide `tsc` is required and fails, targeted compilation of edited files does not satisfy that requirement. If a production build is required and fails, source-level checks do not satisfy that requirement. If a runtime smoke test is required and cannot be executed, static inspection does not satisfy that requirement. Targeted or alternative verification may be reported as supplementary evidence, but the original required verification remains `FAILED` or `UNVERIFIED`.

## Impossible mandatory gates

Before execution, inspect every mandatory verification. If a mandatory gate is already known to be impossible to pass without an out-of-scope change, do not proceed while simultaneously declaring that gate mandatory. Either:

- obtain authorization to expand scope and reclassify the change; or
- explicitly redefine the verification contract so the gate is no longer mandatory, with the limitation recorded.

The agent must never knowingly execute a plan containing an impossible mandatory verification and then call the result `COMPLETE`.

## Unrelated failures and scope control

If an unrelated pre-existing compile/test/build failure prevents verification, do not modify unrelated code merely to make the verification pass. Example: if removing E2EE exposes a pre-existing `ContactRequests.tsx` TypeScript error, fixing `ContactRequests.tsx` is outside the E2EE scope unless explicitly authorized. Report what the unrelated failure is, why it is pre-existing, why fixing it would expand scope, and what verification remains possible without fixing it.

## Approved postconditions

Every material postcondition explicitly authorized in the checkpoint must either be demonstrated by post-change evidence or be reported as unverified. If observed state contradicts an approved postcondition, the action cannot be `COMPLETE` and must return to `BLOCKED_EVIDENCE` for investigation or remediation. The agent must not treat implementation intent, source-code presence, or an unexecuted code path as proof that an approved runtime postcondition occurred. If automatic `localStorage` cleanup is required, the relevant storage keys must be absent after exercising the specified application path. If a migration is required, the resulting database schema must be inspected. If plaintext round-trip is required, an actual write/read observation must establish the returned plaintext. If a build artifact must be regenerated, the artifact must actually be regenerated and verified.

## Pre-existing failures

Pre-existing failures affect attribution, not verification status. When a required verification fails because of a pre-existing condition: record the failure as `PREEXISTING_FAILURE`; do not attribute it to the current change unless evidence supports that attribution; do not claim the verification passed; do not claim `COMPLETE` while that mandatory verification remains unresolved; report the narrowest supported next action. If fixing the pre-existing failure would expand scope beyond the authorized action, do not fix it without reclassification and authorization.

## Completion gate

`COMPLETE` is allowed only when all of the following hold:

- the authorized change was actually executed;
- every mandatory post-change claim has sufficient evidence, with the claim-specific provenance chain `claim -> observed fact -> artifact/command/runtime result -> method -> limitation`;
- every mandatory verification gate has a status from `{PASS, PREEXISTING_FAILURE}`, where `PREEXISTING_FAILURE` is supported by a captured baseline comparison and introduces no new failures;
- no evidence contradiction remains;
- no required claim is merely assumed (an `UNVERIFIED` claim is a contradiction);
- no unauthorized scope expansion occurred.

If any mandatory verification is `UNVERIFIED`, `FAIL`, or otherwise unresolved, or if the baseline comparison for a `PREEXISTING_FAILURE` claim is missing, the final disposition is `BLOCKED_EVIDENCE`. The pre-change evidence gate must not be re-entered silently; return to the appropriate unblock condition or re-classify.

Report the action, scope and risk, state, claims with provenance and limitations, missing/conflicting evidence, authorized next action, and required verification. The final report is the terminal disposition of the authorized action. It does not restart a gate cycle.
