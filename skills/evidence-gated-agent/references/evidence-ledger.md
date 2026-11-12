# Evidence Ledger

This is the working reference for the Evidence Ledger. It is reached
from the universal protocol in [SKILL.md](../SKILL.md) only when a
medium or high-risk change needs a persistent operational record.

The ledger is an enhancement of the universal protocol. It does not
replace the six-state vocabulary, the static-vs-runtime distinction,
the baseline-vs-post-change rule, the verification integrity rule, the
impossible-mandatory-gate rule, the completion gate, or the final
report. Every rule in [SKILL.md](../SKILL.md) continues to apply
inside a ledger. The ledger adds persistence, not leniency.

## The ledger is a record, not evidence

This is the load-bearing principle of the entire feature.

Writing a claim into a ledger does not make it true. A ledger entry
must preserve the same provenance chain as the rest of the skill:

```text
Claim
    |
    v
Required Evidence
    |
    v
Observed Fact
    |
    v
Artifact or Command Result
    |
    v
Method
    |
    v
Limitation
    |
    v
Status
```

A bare assertion with no observation, no artifact, no method, and no
limitation is `UNVERIFIED`, no matter where it is written. `PASS` in
a ledger means: a recorded observation exists, and on its own terms
it supports the claim. The record is not stronger than the
observation. The ledger preserves the chain; it does not replace it.

### Proportionality budget

The ledger is bounded, not exhaustive:

- A ledger for an isolated change should stay under roughly 200 lines. A larger ledger requires a stated reason (multiple phases, audit requirement, high-risk domain).
- Record each material fact once. Do not re-edit the ledger to reword an existing entry.
- Do not re-read the ledger to verify its own formatting. The ledger is written for a future reader, not for the agent's self-check.
- Stop writing when every required section exists and every mandatory claim has one evidence record. Additional polish is waste.

## When a ledger is required

Use the risk classification in [SKILL.md](../SKILL.md):

- `LOW` risk: optional. A local variable rename, isolated typo fix, or
  non-consequential documentation correction does not need a ledger.
- `MEDIUM` risk: recommended when the change involves meaningful
  evidence tracking, multiple verification steps, or work that may
  span multiple investigation or execution phases.
- `HIGH` risk: mandatory. Public HTTP or WebSocket contracts,
  authentication, authorization, payments, financial operations,
  schema migrations, destructive or irreversible data operations,
  production configuration, shared credential handling, irreversible
  actions, and significant production impact all require one.

Concrete tier examples; when two tiers plausibly apply, the higher
tier wins:

- `LOW`: local rename, comment or typo fix, isolated test addition,
  non-consequential documentation.
- `MEDIUM`: shared type or interface (a contract, not a local edit),
  internal module contract, new internal helper adopted by one call
  site, UI behavior change with no data or auth surface, multi-file
  refactor.
- `HIGH`: the list above.

When in doubt, escalate to the higher tier. The cost of an extra
ledger is a single Markdown file; the cost of a missed one is a
context-lost completion claim.

## Where a ledger lives

Default working location:

```text
.evidence-gated/
├── active/
|   └── <change-id>.md
└── archive/
    └── <change-id>.md
```

The default is working state, not a published artifact. The agent
should add `.evidence-gated/active/` to `.gitignore` for new projects
unless the user or repository conventions say otherwise. Repository
conventions and explicit user instructions take precedence; the agent
must not silently modify `.gitignore` merely because the skill uses a
ledger.

Audit-trail ledgers, kept as part of repository history, are
appropriate when:

- the user explicitly requests an audit trail;
- the change is particularly high-risk and the user wants the record
  preserved;
- repository conventions require persistent documentation for
  consequential changes (for example, `docs/evidence-gated/...`).

The agent must not commit an active ledger without authorization.
Writing the ledger is part of this skill's own operation and is
authorized by the skill unless the caller explicitly forbids it. If a
caller forbids all writes, keep the ledger inline in the report; do not
pretend a ledger file exists and do not skip the ledger silently. If a
caller forbids writes but the change is `HIGH` risk, surface the
conflict before acting.

## Lifecycle

1. **Determine** whether a ledger is required, using the risk tiers
   above.
2. **Locate** an existing active ledger before creating a new one.
   Do not create multiple ledgers for the same active change.
3. **Read** the active ledger before continuing. Re-read it before:
   - a new investigation phase;
   - a significant change execution;
   - requesting checkpoint approval;
   - acting on an approval;
   - any scope change;
   - any verification requirement change;
   - any completion claim.

   The re-read must confirm: current requested action, current
   authorized scope, current risk, active assumptions, mandatory
   claims, mandatory verification, checkpoint state, approval state,
   known limitations, current disposition. Do not rely on memory
   for any of these.
4. **Update** the ledger when material facts change: risk, scope,
   assumptions, evidence, verification requirements, baseline,
   checkpoint state, approval state, execution state, verification
   results, final disposition.
5. **Finalize** the ledger at a terminal disposition. The terminal
   values are `COMPLETE`, `BLOCKED_EVIDENCE`, or
   `BLOCKED_CLARIFICATION`. A ledger implying `COMPLETE` while a
   mandatory claim remains `UNVERIFIED`, `FAIL`, or otherwise
   unresolved is invalid and must be returned to the appropriate
   unblock condition.

## Reopening a finalized ledger

Reopening a finalized ledger is allowed when an external change or new
evidence affects a completed change. On reopen:

1. Set the operational phase to `INVESTIGATING`.
2. Set the disposition to `BLOCKED_EVIDENCE` or
   `BLOCKED_CLARIFICATION` until the affected claims are re-evaluated.
3. Keep the prior final disposition verbatim in a history subsection
   marked `SUPERSEDED`. Never overwrite it.
4. `COMPLETE` may be restored only after the affected evidence is
   `VALID` or `RE-VERIFIED` against current state and every affected
   mandatory verification has been re-run.

## Evidence freshness and validity

The ledger records evidence state, including validity, because persisted evidence can become stale. Evidence is not permanently valid merely because it was once collected. When the relevant state, assumptions, artifacts, or conditions on which an evidence record depended change materially, the affected evidence must be re-evaluated before being relied upon for a consequential decision or completion claim. Freshness is primarily about state dependency, not about age or wall-clock time; a recent inspection can already be `STALE` and an older inspection can still be `VALID` when the relevant state has not changed. Time may matter in some contexts, but it must not become the universal freshness mechanism.

### Validity states

The ledger tracks evidence validity with four states. Do not silently convert one into another, and never silently rewrite history.

- `VALID` — the evidence is currently applicable to the claim it supports. The relevant conditions, assumptions, artifacts, and dependencies have not materially changed in a way known to undermine that evidence. `VALID` does not mean permanently true; it means currently applicable based on known state.
- `STALE` — something relevant has changed, but the effect has not yet been fully determined. `STALE` evidence may still hold; the change has not been shown to undermine it. Re-evaluation is required before relying on this evidence for a consequential decision or completion claim. Do not automatically interpret `STALE` evidence as disproven.
- `INVALIDATED` — a known change directly undermines the conditions under which the evidence was obtained. The evidence can no longer be relied upon for its claim. Historical provenance is preserved in the ledger.
- `RE-VERIFIED` — the evidence is currently applicable, but it previously became `STALE` or `INVALIDATED` and was subsequently re-established against the current state, with its own provenance recorded. `RE-VERIFIED` is a current-validity state, not merely a historical transition. An evidence record whose current status is `VALID` has not required re-verification since being recorded; an evidence record whose current status is `RE-VERIFIED` was previously stale or invalidated and has been re-established. Both `VALID` and `RE-VERIFIED` legitimately satisfy the completion gate when applicable to current state. `RE-VERIFIED` does not retroactively erase the prior `STALE` or `INVALIDATED` state; the chain must be preserved in the ledger.

### Evidence dependencies

Meaningful evidence records should identify the conditions on which they depend, where practical. Examples include the current API schema, current endpoint implementation, known consumer assumptions, current schema, migration implementation, existing production data assumptions, environment, fixtures, and relevant configuration. The skill does not require a complicated dependency graph or automated dependency engine; the requirement is operational. The agent must identify relevant dependencies sufficiently to recognize when evidence may no longer apply. Absence of an explicit dependency list does not, by itself, invalidate evidence; it makes timely re-evaluation harder and is itself a reason for caution.

### Material-change detection

Evidence should be reconsidered when a material change affects any of the following:

- **Artifacts** — relevant source code, schemas, configuration, contracts, migrations, infrastructure definitions.
- **Assumptions** — consumer, data, authorization, or environment assumptions.
- **Scope** — new components added to the change; previously out-of-scope components becoming relevant; authorized behavior changing.
- **Dependencies** — a relevant service changes; an external dependency version changes; a contract changes.
- **Verification conditions** — environment, test fixtures, or relevant configuration changes.
- **New contradictory evidence** — new evidence that contradicts prior evidence requires immediate reconsideration of the affected evidence.

A useful principle: re-evaluate evidence when a reasonable connection exists between the change and the conditions required for that evidence to support its claim. An unrelated typo fix in an unrelated document must not invalidate unrelated API compatibility evidence; proportionality is required.

### Re-evaluation procedure

When a potentially material change occurs, the agent should follow a clear procedure:

1. **Identify affected claims.** Which existing claims may depend on what changed?
2. **Identify supporting evidence.** For each affected claim, what evidence currently supports it?
3. **Determine impact.** Classify the evidence as `VALID`, `STALE`, or `INVALIDATED`.
4. **Record the reason.** Record what changed, why it affects this evidence, and which claim is affected. Do not merely change a status.
5. **Determine whether re-verification is mandatory.** Consider risk level, consequence of relying on stale evidence, whether the evidence supports a mandatory gate, and whether the evidence supports a completion claim.
6. **Re-verify when required.** Gather new evidence against the current state with its own provenance.
7. **Preserve history.** Do not overwrite historical evidence as though it never existed. The ledger should retain enough history to explain what was originally verified, what changed, why the evidence became stale or invalidated, and what replaced it.

### Completion gate interaction

A completion claim must not rely on evidence known to be `STALE` or `INVALIDATED` when that evidence supports a mandatory claim or verification requirement. This is a hard gate: if mandatory evidence is not currently applicable to its claim, `COMPLETE` is not available and the disposition is `BLOCKED_EVIDENCE` until the affected requirement is appropriately re-evaluated. The existing baseline-vs-post-change rule is preserved; historical baseline evidence remains a record of the pre-change state and is not converted into current post-change verification.

### Freshness versus authorization

Freshness does not silently invalidate user authorization. Evidence invalidation (a technical verification is no longer current) is distinct from authorization invalidation (the implementation changed so materially that the approved scope no longer covers the new action). When a material change invalidates a critical assumption behind an approval such that the understood consequences have materially changed, the agent must record the new fact, reassess scope and consequences, determine whether the existing approval still covers the action, and request a new checkpoint if necessary. Do not automatically treat all stale evidence as requiring new user approval.

### Static and runtime evidence

Freshness rules respect the existing distinction between static and runtime evidence. Static evidence (such as a repository inspection finding three consumers) may become stale if relevant repository code changes. Runtime evidence (such as an endpoint returning HTTP 200) may become invalidated if relevant runtime behavior changes. Fresh static evidence does not substitute for required fresh runtime evidence; freshness does not change evidence type requirements.

Static evidence supports presence, absence, shape, type compatibility, call graph, configuration contents, and file-level diffs. Runtime evidence is required for status codes, response bodies, rendered output, emitted events, timing, persistence effects, and any statement that a code path executed. A claim whose wording implies behavior must not be recorded `PASS` on static evidence; record it `UNVERIFIED` and name the missing runtime observation.

### Harness fidelity

Every runtime evidence record states its harness:

- `harness`: real entrypoint, or a named harness listing every stubbed, mocked, or shimmed component.
- `fidelity`: what the observation does and does not establish about the unmodified system.

A runtime observation from a harness with stubbed components may support claims about the exercised components only. It may not support a claim about the unmodified entrypoint, and it may not be the sole evidence for a completion claim unless the contract explicitly accepts it.

## Claim and evidence impact tracking

Impact tracking adds lightweight, optional relationship fields to the
ledger so that material changes can be traced to the claims, evidence,
and verification requirements they may affect. It is a relationship
model, not a graph engine: the goal is operational traceability, not
automated repository analysis.
### Relationship model

The conceptual model is:

```text
Dependency / Condition
        |
        v
Claim
        |
        v
Evidence
        |
        v
Verification Requirement
```

When something changes, the agent walks the same chain in reverse:

```text
Material Change
        |
        v
Affected Dependencies / Conditions
        |
        v
Affected Claims
        |
        v
Affected Evidence
        |
        v
Required Re-evaluation / Verification
```

The agent records these relationships where they materially help
reasoning. They do not need to form a complete graph and are not
required for every trivial observation.

### Claim identity

Where impact tracking is used, give meaningful claims stable
identifiers (`C-001`, `C-002`, ...) so they can be referenced from
evidence, verification, and impact records. Identifiers must be:

- stable for the duration of the active change;
- unique within the Evidence Ledger;
- human-readable;
- lightweight.

Use identifiers primarily for decision-relevant claims, mandatory
claims, high-risk claims, claims with multiple evidence dependencies,
and claims likely to be affected by future changes. Do not require
identifiers for trivial observations.

### Evidence-to-claim relationships

Evidence records should explicitly identify the claims they support
when practical. This prevents an evidence record from becoming an
isolated piece of information and lets the agent answer: "If this
evidence becomes stale or invalidated, which claims are affected?"

### Claim-to-dependency relationships

Claims should identify relevant dependencies or conditions where
impact tracking is needed. Dependencies may optionally carry
identifiers (`D-001`, `D-002`, ...). Use identifiers only when they
materially improve traceability; do not require artificial IDs for
simple tasks.

### Verification-to-claim relationships

Where a claim depends on mandatory verification, make that
relationship explicit. Verification records may similarly indicate
which claims they support. The result is a traceable chain such as:

```text
C-001
  |
  +-- Evidence
  |     +-- E-003
  |     +-- E-007
  |
  +-- Verification
        +-- V-002
        +-- V-003
```

### Direct and indirect impact

Distinguish conceptually between direct impact (the change
immediately affects a claim's conditions) and indirect impact (the
change propagates through one or more known relationships before
reaching a claim). The agent must follow known or reasonably
inferable impact relationships until further analysis would become
speculative or disproportionate. Do not invent dependency chains
without evidence.

### Impact is not proof

Recording a relationship such as `D-001 -> C-001` does not prove
`C-001` is false. Recording `Change -> C-001` does not automatically
prove the claim is broken. Impact tracking identifies what requires
consideration; it does not establish what is true. The actual truth
of a claim still requires appropriate evidence, classified by the
existing freshness model.

### Impact states

Use a small set of impact states. The full vocabulary is not
required for every change:

- `NO_KNOWN_IMPACT` — the change was considered and no reasonable
  connection to the claim was found.
- `POTENTIAL_IMPACT` — a reasonable connection exists but has not
  been confirmed against current state.
- `REQUIRES_REVIEW` — a material connection has been identified and
  the affected evidence or verification must be re-evaluated.
- `CONFIRMED_IMPACT` — re-evaluation has confirmed that the change
  affects the claim, with the specific effect recorded.
- `UNKNOWN` — the change may affect the claim, but the repository
  inspection did not establish the connection.

The most important distinction is between `UNKNOWN` and
`NO_KNOWN_IMPACT`. Unknown impact is not the same as no impact. Do
not silently treat uncertainty as absence of effect.

### Impact Review records

For medium and high-risk changes where material changes occur,
record a lightweight Impact Review. The review preserves the chain:

```text
Change
-> Dependencies / Conditions
-> Claims
-> Evidence
-> Verification
-> Impact Result
-> Required Action
```

Example shape:

```md
## Impact Review IR-001

### Change

API request schema changed.

### Affected Dependencies / Conditions

- D-001 — API schema

### Potentially Affected Claims

- C-001 — Existing clients remain compatible
- C-003 — Existing request format remains accepted

### Supporting Evidence

- E-003
- E-007

### Required Verification

- V-002
- V-003

### Impact Status

REQUIRES_REVIEW

### Result

- E-003 -> STALE
- E-007 -> INVALIDATED

### Required Action

Re-run compatibility verification.
```

The exact field names may vary; the chain
`Change -> Dependencies -> Claims -> Evidence -> Verification -> Impact Result -> Required Action`
must remain.

### Material-change impact analysis procedure

When a potentially material change occurs, the agent performs
impact analysis before deciding whether the change affects existing
claims:

1. **Record the change.** Identify what changed and why it may be
   material.
2. **Identify affected dependencies or conditions.** Ask which known
   dependencies or conditions the change affects (for example,
   API schema, authentication configuration, database schema,
   consumer assumption, runtime environment).
3. **Identify affected claims.** Using explicit relationships where
   available, ask which claims depend on those conditions.
4. **Identify affected evidence.** Ask which evidence records
   support those claims.
5. **Identify affected verification.** Ask which mandatory
   verification requirements support those claims.
6. **Perform freshness classification.** Apply the existing
   freshness model (`VALID` / `STALE` / `INVALIDATED` /
   `RE-VERIFIED`) to the affected evidence. Do not introduce a
   second competing validity system.
7. **Determine required action.** Possible outcomes include no
   action, re-evaluate evidence, re-run verification, gather new
   evidence, request a checkpoint, or request clarification. The
   action must remain proportional to risk and consequence.

### Interaction with evidence freshness

Impact tracking feeds freshness; it does not replace it. The
relationship is:

```text
Impact Analysis
        |
        v
Identifies affected claims / evidence
        |
        v
Freshness Evaluation
        |
        v
VALID / STALE / INVALIDATED / RE-VERIFIED
        |
        v
Re-verification if required
```

Impact answers "what should we reconsider?". Freshness answers "is
the existing evidence still applicable?". Verification answers
"what is true about the current state?". Keep these
responsibilities distinct.

### Interaction with scope changes

When scope changes:

1. Record the scope change.
2. Identify newly affected dependencies.
3. Identify affected claims.
4. Determine whether existing evidence applies to the expanded
   scope.
5. Determine whether new evidence is required.
6. Re-evaluate risk.
7. Determine whether authorization is required.

Do not assume that evidence supporting the old scope automatically
supports the expanded scope unless that is actually established.

### Interaction with authorization

Impact tracking must not silently expand authorization. Discovering
that `Component B affects Component A` does not authorize modifying
`Component B`. When impact analysis reveals work that may be
required outside the authorized scope:

1. Record the impact.
2. Explain why it matters.
3. Determine whether the existing authorization covers it.
4. Request clarification or a checkpoint when required.

Impact discovery and scope authorization remain separate gates.

### Completion gating

For medium and high-risk work using impact tracking, `COMPLETE`
must not be available while a mandatory claim has an unresolved
`UNKNOWN` or `REQUIRES_REVIEW` impact that could materially affect
that claim. Completion blocking remains proportional and tied to:

- mandatory claims;
- required verification;
- risk;
- material consequence.

Do not block completion because of unrelated or low-consequence
unknown relationships.

### Risk-tiered usage

- `LOW` risk — optional. Use only when the relationship materially
  helps reasoning.
- `MEDIUM` risk — recommended when multiple claims depend on shared
  conditions, when multiple components are affected, when scope
  may evolve, or when changes may invalidate multiple evidence
  records.
- `HIGH` risk — required for material changes where multiple
  decision-relevant claims exist, where authorization consequences
  may change, where evidence dependencies are non-trivial, or where
  completion depends on multiple verification requirements.

Elaborate impact records are not required for high-risk changes that
are genuinely simple and isolated. Use judgment while preserving
rigor.

 ## Source of truth hierarchy

Authority depends on what is being established. The skill is
fundamentally about evidence-gated factual claims, so a user
assertion about a factual matter is not a substitute for that
evidence. The hierarchy is two-axis:

For intent, authorization, desired scope, and acceptable tradeoffs:

1. Explicit user instruction or approval.

For factual repository state, runtime behavior, and verification
results:

1. Direct repository and runtime evidence, including command output
   for executed verification.
2. Recorded Evidence Ledger, as a record of that evidence.
3. Agent memory or conversation context.

The Evidence Ledger never overrides its underlying source evidence,
and user assertions about factual matters are not promoted to fact
by being recorded. If the ledger conflicts with current repository
evidence or explicit user instructions: identify the contradiction,
do not silently choose one, update the ledger only after resolving or
explicitly recording the conflict.

## Approval and scope rules apply inside the ledger

Generic approval phrases ("go ahead", "your call", "do what's best",
"use your judgment", or similar) are not authorization in a ledger
any more than they are in conversation. Approval recorded in the
ledger must be tied to the same `CHECKPOINT APPROVAL REQUIRED`
record used by the rest of [SKILL.md](../SKILL.md). A "Reply
APPROVE" or "your call" answer that does not match the record
line-for-line is not authorization; re-present the record or return
`BLOCKED_CLARIFICATION`.

Discovering that another component is related to the change is not
new authorization. A new evidence finding is not a new scope. When
scope materially changes:

1. Record the proposed scope change in the ledger.
2. Identify affected claims and verification requirements.
3. Re-evaluate risk; if risk escalates, re-evaluate the evidence
   contract and the checkpoint requirement.
4. Determine whether new authorization is required.
5. Update the ledger.
6. Do not execute unauthorized expanded scope.

## Risk changes

Risk classification is not permanently fixed. If new evidence changes
blast radius, reversibility, affected consumers, security impact,
financial impact, production impact, or dependency surface, the
agent must reconsider the risk classification, update the ledger,
and, if risk escalates to high, re-evaluate the evidence contract and
determine whether a checkpoint is required.

## Status taxonomy inside the ledger

The ledger header carries two distinct fields. Do not conflate them.

**Operational Phase** describes what the agent is currently doing with
the change, in the order work proceeds:

- `DRAFT` — ledger created, contract not yet written.
- `INVESTIGATING` — gathering evidence, capturing baseline, resolving
  assumptions.
- `EXECUTING` — authorized scoped change in progress.
- `VERIFYING` — post-change verification and finalization.

Phases are bookkeeping. They do not authorize anything; they do not
block anything; they do not count as evidence. A phase transition
without the corresponding disposition change is not a change in
authorization.

**Disposition** is the gate-level decision from the universal
protocol. The dispositions are exactly the six canonical states of
[SKILL.md](../SKILL.md):

- `BLOCKED_CLARIFICATION`
- `BLOCKED_EVIDENCE`
- `ALLOW`
- `ALLOW_WITH_VERIFICATION`
- `CHECKPOINT`
- `COMPLETE`

The disposition is what authorizes execution, gates verification, and
finalizes the change. At finalization, the ledger disposition must be
one of these six. Intermediate phases are not a substitute for a
disposition.

The same change can be in `EXECUTING` phase and `ALLOW_WITH_VERIFICATION`
disposition at the same time. The same change can be in `INVESTIGATING`
phase and `BLOCKED_EVIDENCE` disposition at the same time. Conflating
them makes authorization unclear and hides the gate; do not do it.

Use the same verification-status taxonomy as [SKILL.md](../SKILL.md):
`PASS`, `FAIL`, `UNVERIFIED`, `PREEXISTING_FAILURE`,
`BLOCKED_EVIDENCE`, `BLOCKED_CLARIFICATION`, `CHECKPOINT`,
`COMPLETE`. Do not silently convert one into another. A `PASS` in
the ledger is a recorded observation that, on its own terms,
supports the claim; it is not stronger than the observation.

## Template

The template below is the minimum content for an active ledger. The
sections are required; the content within each section is
proportional to the change.

```md
# Evidence Ledger

## Change ID

<identifier, for example a short slug or ticket reference>

## Operational Phase

<DRAFT | INVESTIGATING | EXECUTING | VERIFYING>

## Disposition

<BLOCKED_CLARIFICATION | BLOCKED_EVIDENCE | ALLOW | ALLOW_WITH_VERIFICATION | CHECKPOINT | COMPLETE>

## Requested Action

<exact requested action, quoted where possible>

## Authorized Scope

- ...

## Explicitly Out of Scope

- ...

## Scope Limitations / Unknowns

- ...

## Risk Classification

Level: LOW | MEDIUM | HIGH

### Reasons

- ...

## Material Assumptions

| Assumption | Status | Supporting Evidence / Limitation |
| --- | --- | --- |
| Existing clients use API v1 | CONFIRMED | repo search found three internal call sites |
| No external consumers exist | UNVERIFIED | no external registry; cannot establish from repo alone |

## Evidence Contract

### Claim: <decision-relevant claim>

**Claim ID:** C-001

**Claim:**

<decision-relevant claim>

**Dependencies / Conditions:**

- D-001 — <condition the claim depends on>
- D-002 — <condition the claim depends on>

**Required Evidence**

- E-001
- E-002

**Required Verification**

- V-001

**Evidence Type**

Static | Runtime | Both

**Consequence if Unsupported**

<concrete consequence>

**Status**

UNVERIFIED | PASS | FAIL | PREEXISTING_FAILURE

### Claim: <next decision-relevant claim>
(repeat for each)

## Evidence Records

### Evidence Record E-001

**Claim:** <claim>

**Supports Claims:**

- C-001

**Observed Fact:** <what was actually observed>

**Artifact / Command:** <exact command, log path, or artifact reference>

**Method:** <how the observation was made>

**Evidence Type:** Static | Runtime

**Harness:** real entrypoint, or named harness with stubbed/mocked/shimmed components

**Fidelity:** what this observation does and does not establish about the unmodified system

**Limitation:** <what this evidence does not establish>

**Status:** PASS | FAIL | UNVERIFIED | PREEXISTING_FAILURE

**Validity:** VALID | STALE | INVALIDATED | RE-VERIFIED

**Dependencies / Conditions:**

- D-001 — <condition>

**Freshness Review:**

Last reviewed against current relevant state: <phase, change id, or operational context>

**Invalidation / Staleness History:**

- <phase or change id>: marked STALE because ...
- <phase or change id>: RE-VERIFIED after ... (new evidence E-00N)

(repeat for each material evidence item)

## Baseline Verification

### Verification

<verification name>

### Command / Method

<exact command or method>

### Result

PASS | FAIL | PREEXISTING_FAILURE | UNVERIFIED

### Exact Observations

<verbatim output, file paths, exit code>

### Exit Code

<n>

### Baseline Captured

YES | NO

## Checkpoint

### Status

NOT_REQUIRED | PENDING_APPROVAL | APPROVED | REJECTED

### Approval Covers

- ...

### Irreversible Consequences

- ...

### Required Verification

- ...

### Approval Record

<verbatim `CHECKPOINT APPROVAL REQUIRED` record and the matching
"Reply APPROVE" answer, or a reference to where it is stored. A bare
"go ahead" or "your call" is not an approval record.>

## Execution Log

### Change E-001

Status: COMPLETE | IN_PROGRESS | BLOCKED

Files / Components Affected:

- ...

Reason:

...

Scope Authorization:

...

Verification Impact:

...

(repeat for each material state transition; trivial edits are not
required)

## Verification

### Verification V-001

**Requirement:**

...

**Supports Claims:**

- C-001

**Command / Method:**

...

**Baseline:**

...

**Post-change Result:**

...

**Status:**

PASS | FAIL | PREEXISTING_FAILURE | UNVERIFIED

**Limitations:**

...

(repeat for every mandatory verification)

## Impact Reviews

### Impact Review IR-001

**Change:**

<description of the material change>

**Affected Dependencies / Conditions:**

- D-001 — <condition>

**Potentially Affected Claims:**

- C-001 — <claim>

**Supporting Evidence:**

- E-001

**Required Verification:**

- V-001

**Impact Status:**

NO_KNOWN_IMPACT | POTENTIAL_IMPACT | REQUIRES_REVIEW | CONFIRMED_IMPACT | UNKNOWN

**Result:**

- E-001 -> STALE
- E-002 -> INVALIDATED

**Required Action:**

<re-run verification, gather new evidence, request checkpoint, request clarification, or no action>

## Limitations

- ...

## Missing Evidence

- ...

## Conflicting Evidence

- ...

## Unresolved Claims

- ...

## Final Disposition

Status:

COMPLETE | BLOCKED_EVIDENCE | BLOCKED_CLARIFICATION

### Reason

...

### Remaining Limitations

...

### Authorized Next Action

...

### Required Verification

...
```

## Example evidence record (correct shape)

The following is a correct entry. The claim, the observation, the
artifact, the method, the limitation, and the status are all
present; `PASS` reflects the observation, not an assertion.

```md
### Evidence Record E-001

**Claim:** Unauthenticated requests to the public endpoint are
rejected with HTTP 401.

**Observed Fact:** `curl -i http://localhost:3000/api/example` returned
`HTTP/1.1 401 Unauthorized` with a `WWW-Authenticate: Bearer` header.

**Artifact / Command:** `curl -i http://localhost:3000/api/example`

**Method:** Direct runtime execution against a local instance started
from the current commit.

**Evidence Type:** Runtime.

**Limitation:** Verified against a single local instance; production
proxy and rate-limiter behavior was not exercised.

**Status:** PASS
```

## Example evidence record (incorrect shape)

The following is unacceptable and must be reported as `UNVERIFIED`,
not `PASS`. The claim is unbacked, the observation is missing, the
artifact is missing, and the method is missing:

```md
### Evidence Record E-002

**Claim:** Authentication works correctly.

**Status:** PASS
```

This entry records an unsupported assertion, not evidence. The
ledger is not stronger than its weakest entry.

## Completion gate inside the ledger

The completion gate is the same as in [SKILL.md](../SKILL.md).
`COMPLETE` is allowed only when:

- the authorized change was actually executed;
- every mandatory post-change claim has sufficient evidence, with the
  provenance chain above;
- every mandatory verification gate has a status from
  `{PASS, PREEXISTING_FAILURE}` with a captured baseline comparison;
- no evidence contradiction remains;
- no required claim is merely assumed;
- no unauthorized scope expansion occurred;
- no mandatory evidence record is currently `STALE` or `INVALIDATED`
  for the change on which its claim depends. A completion claim must
  not rely on evidence known to be `STALE` or `INVALIDATED` when that
  evidence supports a mandatory claim or verification requirement.
  This rule does not retroactively delete historical `STALE` or
  `INVALIDATED` records; it requires that the affected claim have
  fresh evidence (`VALID` or `RE-VERIFIED` against the current state)
  before `COMPLETE` is available.

If any mandatory verification is `UNVERIFIED`, `FAIL`, or otherwise
unresolved, or if any mandatory evidence record's **current**
validity status is `STALE` or `INVALIDATED` for the change on
which its claim depends, the final disposition in the ledger is
`BLOCKED_EVIDENCE`. The pre-change evidence gate must not be
re-entered silently; return to the appropriate unblock condition or
re-classify.

A mandatory claim must not rely on evidence whose **current**
validity status is `STALE` or `INVALIDATED`. If re-evaluation
determines that previously `STALE` evidence remains applicable to
the current state, the evidence record must document the
re-evaluation and may return to `VALID` according to the defined
history rules. If new evidence is gathered against the current
state, the new evidence record is `RE-VERIFIED` with its own
provenance. Historical stale or invalidation history must not
permanently block completion; only the current validity status of
mandatory evidence gates completion.

Historical baseline evidence remains a record of the pre-change
state and is distinct from current post-change verification
evidence; a baseline does not prove current behavior after relevant
changes, and a historical baseline record is not itself `STALE` or
`INVALIDATED` merely because time has passed.

