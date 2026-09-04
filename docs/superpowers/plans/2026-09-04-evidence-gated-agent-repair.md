# Evidence-Gated Agent Repair Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Repair the Evidence-Gated Agent’s state semantics and validation claims, then package its publishable source, fixture, and validation evidence in clear repository boundaries.

**Architecture:** `skills/evidence-gated-agent/` is the only publishable skill artifact. A compact `SKILL.md` holds the universal state transition protocol and points to claim-specific high-risk material. The Python service moves to a non-runtime test fixture, and its corrected validation record moves to `docs/validation/`.

**Tech Stack:** Markdown Agent Skill files; Python/pytest fixture; Git; bundled `skill-creator` validator.

**Spec:** User-approved repair plan in this task, based on the reviews of `skill-creator`, `superpowers:writing-skills`, and `writing-for-agents`.

## Global Constraints

- Retain model invocation: this skill must be discoverable before consequential repository work.
- Frontmatter description is a concise, third-person `Use when…` trigger pointer, not a workflow summary.
- Missing required factual evidence remains `BLOCKED_EVIDENCE`; approval cannot convert an unsupported claim into evidence.
- The post-change report is the terminal disposition of the authorized action, not a new action that restarts the protocol.
- Create no root packaging/configuration files unless a task demonstrates their necessity.
- Preserve fixture files as ordinary test inputs; remove their nested Git metadata because no replayable history harness consumes it.

---

### Task 1: Establish failing documentation-contract checks

**Files:**
- Create: `tests/skill_contract_test.py`
- Test: `evidence-gated-agent/SKILL.md`

**Interfaces:**
- Consumes: the current source skill’s YAML frontmatter and Markdown body.
- Produces: executable checks for the state vocabulary, strict evidence block, nonrecursive completion rule, and frontmatter discovery contract.

- [ ] **Step 1: Write failing checks for the current skill**

```python
from pathlib import Path


SKILL = Path("evidence-gated-agent/SKILL.md")


def test_description_is_a_concise_trigger_pointer():
    description = SKILL.read_text().split("---", 2)[1]
    assert "description: Use when" in description
    assert len(description) < 500
    assert "risk-scaled evidence gate" not in description


def test_gate_states_are_defined_once_and_cover_all_outcomes():
    body = SKILL.read_text()
    for state in (
        "BLOCKED_CLARIFICATION",
        "BLOCKED_EVIDENCE",
        "ALLOW",
        "ALLOW_WITH_VERIFICATION",
        "CHECKPOINT",
        "COMPLETE",
    ):
        assert state in body


def test_missing_required_evidence_never_authorizes_change():
    body = SKILL.read_text()
    assert "Missing required factual evidence remains `BLOCKED_EVIDENCE`." in body


def test_completion_report_is_terminal_not_a_new_gate_cycle():
    body = SKILL.read_text()
    assert "The final report is the terminal disposition of the authorized action." in body
```

- [ ] **Step 2: Run the checks and observe the expected failures**

Run: `python3 -m pytest tests/skill_contract_test.py -q`

Expected: failures because the original description is a workflow summary, no unified state contract exists, the evidence-gap exception exists, and completion restarts the gate.

- [ ] **Step 3: Record the observed baseline behavior test**

Keep the two no-skill pressure-control transcripts in the validation record. They show that the chosen prompts did not elicit the target failure, so they cannot substantiate a claim that the skill changed behavior. Add a distinct, stronger pressure scenario only if it produces an observed no-skill rationalization; do not invent a rationalization.

### Task 2: Repair and compress the skill protocol

**Files:**
- Create: `skills/evidence-gated-agent/SKILL.md`
- Create: `skills/evidence-gated-agent/references/high-risk-domains.md`
- Delete after move: `evidence-gated-agent/SKILL.md`
- Delete after move: `evidence-gated-agent/references/high-risk-domains.md`
- Test: `tests/skill_contract_test.py`

**Interfaces:**
- Consumes: the policy requirements in this plan and the current high-risk reference.
- Produces: a model-invoked skill with one state vocabulary and one precise pointer to high-risk domain evidence.

- [ ] **Step 1: Write the minimal state transition contract**

Define `BLOCKED_CLARIFICATION`, `BLOCKED_EVIDENCE`, `ALLOW`, `ALLOW_WITH_VERIFICATION`, `CHECKPOINT`, and `COMPLETE` together. State that the first two allow only read-only investigation or a focused user question; `CHECKPOINT` requires explicit approval after its contract is satisfied; and `COMPLETE` follows the post-change evidence gate.

- [ ] **Step 2: Replace the evidence-gap loophole**

Use this exact policy:

```markdown
Missing required factual evidence remains `BLOCKED_EVIDENCE`.
Human approval can select a narrower action or accept a known adverse
risk only when that adverse fact is established and no applicable rule
requires its absence. It never makes an unsupported factual claim true.
```

- [ ] **Step 3: Remove recursive completion wording**

Use this exact terminal rule:

```markdown
The final report is the terminal disposition of the authorized action.
It records the post-change gate; it does not initiate another gate cycle.
```

- [ ] **Step 4: Prune and relocate conditional detail**

Keep only the universal sequence, state contract, evidence/provenance rule, scope-expansion trigger, and short reporting shape in `SKILL.md`. Retain the existing high-risk-domain reference only because the public API, auth, payments, and migration branches have distinct claims; point to it only when building a high-risk contract in those domains.

- [ ] **Step 5: Run the documentation-contract checks to green**

Run: `python3 -m pytest tests/skill_contract_test.py -q`

Expected: all checks pass after paths are adjusted to `skills/evidence-gated-agent/SKILL.md`.

### Task 3: Correct fixture and validation evidence

**Files:**
- Modify: `fixture-repo/src/api/public.py`
- Modify: `fixture-repo/tests/test_api_public.py`
- Create: `docs/validation/evidence-gated-agent.md`
- Test: `fixture-repo/tests/test_api_public.py`

**Interfaces:**
- Consumes: the stable `/v1` contract in `fixture-repo/docs/api.md`.
- Produces: fixture behavior aligned with its documented contract and a validation record that distinguishes observed evidence from unrun or invalid tests.

- [ ] **Step 1: Write the failing public-contract regression test**

Replace the current key-set assertion with:

```python
assert set(profile) == {"id", "display_name", "email", "created_at"}
assert "phone_number" not in profile
```

- [ ] **Step 2: Run the focused test and observe the failure**

Run: `cd fixture-repo && python3 -m pytest tests/test_api_public.py -q`

Expected: failure because `get_user_profile` returns undocumented `phone_number`.

- [ ] **Step 3: Restore the documented API contract minimally**

Remove the `phone_number` entry from `get_user_profile` and delete the test that asserts missing-phone normalization. Do not alter the documented `/v1` contract or claim a completed public contract change.

- [ ] **Step 4: Run the fixture suite**

Run: `cd fixture-repo && python3 -m pytest -q`

Expected: all remaining fixture tests pass.

- [ ] **Step 5: Write an honest validation record**

The record must:

- say the old report was replaced because its Scenario 2 and Scenario 7 outcomes contradicted the skill;
- identify the precise reason: payment retry work is `HIGH`, and the documented `/v1` contract was changed without a checkpoint;
- record the two observed no-skill pressure controls as non-failing controls, not as proof of effectiveness;
- list structural validation and fixture tests actually run, with their commands and outputs; and
- state that independent GREEN testing remains pending until a no-skill baseline reveals a concrete rationalization and a fresh agent is tested against the revised skill.

### Task 4: Normalize repository boundaries

**Files:**
- Move: `evidence-gated-agent/` → `skills/evidence-gated-agent/`
- Move: `fixture-repo/` → `tests/fixtures/evidence-gated-agent/repository/`
- Move: `REPORT.md` → `docs/validation/evidence-gated-agent.md` (replace with Task 3’s corrected record)
- Retain: `tests/skill_contract_test.py`
- Delete: `tests/fixtures/evidence-gated-agent/repository/.git/`

**Interfaces:**
- Publishable assets resolve under `skills/`.
- Test inputs resolve under `tests/fixtures/` and are not read by the published skill.
- Validation evidence resolves under `docs/validation/` and is not part of the published skill’s runtime protocol.

- [ ] **Step 1: Confirm the inner Git repository has no uncommitted fixture work**

Run: `git -C fixture-repo status --short`

Expected: no output.

- [ ] **Step 2: Move source, fixture, and validation artifacts**

Use explicit `mv` paths after creating their parents. Do not create package files, root agent instructions, changelogs, or a root README.

- [ ] **Step 3: Remove the nested fixture Git metadata**

Run: `rm -rf tests/fixtures/evidence-gated-agent/repository/.git`

This is authorized because the approved plan selects ordinary fixture files and no harness consumes the nested history. Confirm afterward that `find tests/fixtures/evidence-gated-agent/repository -name .git` returns no results.

- [ ] **Step 4: Update every path in tests and validation documentation**

Ensure the documentation-contract test targets `skills/evidence-gated-agent/SKILL.md`; use repository-relative paths in validation commands.

### Task 5: Validate the packaged result

**Files:**
- Verify: `skills/evidence-gated-agent/`
- Verify: `tests/skill_contract_test.py`
- Verify: `tests/fixtures/evidence-gated-agent/repository/`
- Verify: `docs/validation/evidence-gated-agent.md`

**Interfaces:**
- The bundled validator consumes the publishable skill directory.
- Pytest consumes the documentation contract test and fixture test suite.

- [ ] **Step 1: Run the skill validator from its actual installed path**

Run: `python3 /home/sohanguptha/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/evidence-gated-agent`

Expected: `Skill is valid!`

- [ ] **Step 2: Run documentation-contract checks**

Run: `python3 -m pytest tests/skill_contract_test.py -q`

Expected: all checks pass.

- [ ] **Step 3: Run the fixture suite through its new location**

Run: `cd tests/fixtures/evidence-gated-agent/repository && python3 -m pytest -q`

Expected: all tests pass.

- [ ] **Step 4: Inspect paths and Git state**

Run:

```bash
find skills tests docs -maxdepth 5 -type f | sort
find tests/fixtures/evidence-gated-agent/repository -name .git -print
git status --short
```

Expected: publishable source, fixture, validation record, and contract test occupy their declared boundaries; no nested `.git` is reported.

- [ ] **Step 5: Compare every repair requirement against the resulting files**

Confirm: no evidence-gap bypass, complete gate vocabulary, nonrecursive completion, concise trigger-only description, corrected fixture contract, honest validation record, and no unjustified root scaffolding.
