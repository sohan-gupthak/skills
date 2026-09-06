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

## When a ledger is required

Use the risk classification in [SKILL.md](../SKILL.md):

- `LOW` risk: optional. A local variable rename, isolated typo fix, or
  non-consequential documentation correction does not need a ledger.
- `MEDIUM` risk: recommended when the change involves meaningful
  evidence tracking, multiple verification steps, or work that may
  span multiple investigation or execution phases.
- `HIGH` risk: mandatory. Public API or contract changes,
  authentication, authorization, payments, financial operations,
  schema migrations, destructive operations, irreversible actions,
  and significant production impact all require one.

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

**Required Evidence**

- ...

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

**Observed Fact:** <what was actually observed>

**Artifact / Command:** <exact command, log path, or artifact reference>

**Method:** <how the observation was made>

**Evidence Type:** Static | Runtime

**Limitation:** <what this evidence does not establish>

**Status:** PASS | FAIL | UNVERIFIED | PREEXISTING_FAILURE

**Validity:** VALID | STALE | INVALIDATED | RE-VERIFIED

**Dependencies / Conditions:**

- ...

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

