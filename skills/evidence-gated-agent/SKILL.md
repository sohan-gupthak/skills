---
name: evidence-gated-agent
description: Use when a coding agent is about to make a consequential repository change or declare a repository change complete.
---

# Evidence-Gated Agent

For a consequential repository change or completion claim, use this sequence:

1. Separate the requested action from material assumptions. If ambiguity could change behavior, scope, safety, or solution, issue `BLOCKED_CLARIFICATION`; it is unblocked by the smallest authoritative clarification that resolves it.
2. Classify the action in its discovered context as low, medium, or high risk. Consider public/shared surface, behavioral, data, security, financial, and production impact, reversibility, dependencies, and observability.
3. Create a claim-specific evidence contract: current scope, decision-relevant claims, evidence needed for each claim, and the consequence if a claim is unsupported. For public API, auth/authorization, payments, migrations, or destructive operations, use [high-risk domains](references/high-risk-domains.md) while building that contract. For every mandatory verification, classify the evidence as `static` (source inspection, grep, type checking, configuration inspection) or `runtime` (actually executing the application and observing behavior). A source-level check is not proof of runtime behavior; a runtime claim must be supported by an actual executed observation.
4. Gather proportional evidence. Prefer repository artifacts and executable observations; use deterministic analysis where appropriate. Record provenance as `claim -> observed fact -> artifact or command result -> method -> limitation`. For mandatory verifications, capture a baseline run before any change so a later pre-existing failure can be compared against it instead of assumed.
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
