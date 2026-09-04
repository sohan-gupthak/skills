---
name: evidence-gated-agent
description: Use when a coding agent is about to make a consequential repository change or declare a repository change complete.
---

# Evidence-Gated Agent

For a consequential repository change or completion claim, use this sequence:

1. Separate the requested action from material assumptions. If ambiguity could change behavior, scope, safety, or solution, issue `BLOCKED_CLARIFICATION`; it is unblocked by the smallest authoritative clarification that resolves it.
2. Classify the action in its discovered context as low, medium, or high risk. Consider public/shared surface, behavioral, data, security, financial, and production impact, reversibility, dependencies, and observability.
3. Create a claim-specific evidence contract: current scope, decision-relevant claims, evidence needed for each claim, and the consequence if a claim is unsupported. For public API, auth/authorization, payments, migrations, or destructive operations, use [high-risk domains](references/high-risk-domains.md) while building that contract.
4. Gather proportional evidence. Prefer repository artifacts and executable observations; use deterministic analysis where appropriate. Record provenance as `claim -> observed fact -> artifact or command result -> method -> limitation`.
5. Resolve the pre-change state:
   - `BLOCKED_EVIDENCE` when required factual evidence is absent, conflicting, or unavailable. It is unblocked by the required factual evidence, investigation/remediation that resolves the conflict, or an authorized narrower action.
   - `ALLOW` when a supported low-risk action may proceed.
   - `ALLOW_WITH_VERIFICATION` when a supported medium-risk action may proceed with its stated verification required before completion.
   - `CHECKPOINT` when a supported high-risk action needs explicit human approval of the planned action, evidence, limitations, and verification plan. `CHECKPOINT` is not permission to act; explicit approval is required.
6. Make only the authorized scoped change. If scope expands, reclassify risk, revise the evidence contract, and return to the pre-change state.
7. Verify claims proportionally to the action and observed behavior. Run the post-change evidence gate: `COMPLETE` follows only when mandatory verification passed and the required post-change claims are supported.

Missing required factual evidence remains `BLOCKED_EVIDENCE`.
When no applicable policy requires the absent property, a human can choose a narrower action or accept an established adverse risk; approval never makes an unsupported factual claim true. A verification contradiction or an unverified required post-change claim returns to `BLOCKED_EVIDENCE` for investigation/remediation.

Report the action, scope and risk, state, claims with provenance and limitations, missing/conflicting evidence, authorized next action, and required verification. The final report is the terminal disposition of the authorized action. It does not restart a gate cycle.
