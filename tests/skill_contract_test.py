from pathlib import Path
import unittest


def _skill_path() -> Path:
    candidates = (
        Path("skills/evidence-gated-agent/SKILL.md"),
        Path("evidence-gated-agent/SKILL.md"),
    )
    for path in candidates:
        if path.exists():
            return path
    searched = ", ".join(str(path) for path in candidates)
    raise AssertionError(f"Could not locate evidence-gated-agent skill; searched: {searched}")


def _skill_text() -> str:
    return _skill_path().read_text()


def _frontmatter_and_body() -> tuple[str, str]:
    text = _skill_text()
    parts = text.split("---", 2)
    if len(parts) < 3:
        raise AssertionError("Expected YAML frontmatter delimited by ---")
    return parts[1], parts[2]


def _description_value(frontmatter: str) -> str:
    for line in frontmatter.splitlines():
        if line.strip().startswith("description:"):
            return line.split(":", 1)[1].strip()
    raise AssertionError("Expected YAML frontmatter to contain a description field")


class SkillContractTest(unittest.TestCase):
    def test_description_is_a_concise_trigger_pointer(self):
        frontmatter, _ = _frontmatter_and_body()
        description = _description_value(frontmatter)
        self.assertTrue(description.startswith("Use when"))
        self.assertLess(len(description), 500)
        self.assertNotIn("risk-scaled evidence gate", description)

    def test_gate_state_tokens_cover_all_outcomes(self):
        _, body = _frontmatter_and_body()
        for state in (
            "BLOCKED_CLARIFICATION",
            "BLOCKED_EVIDENCE",
            "ALLOW",
            "ALLOW_WITH_VERIFICATION",
            "CHECKPOINT",
            "COMPLETE",
        ):
            with self.subTest(state=state):
                self.assertIn(state, body)

    def test_missing_required_evidence_never_authorizes_change(self):
        _, body = _frontmatter_and_body()
        self.assertIn(
            "Missing required factual evidence remains `BLOCKED_EVIDENCE`.",
            body,
        )

    def test_completion_report_is_terminal_not_a_new_gate_cycle(self):
        _, body = _frontmatter_and_body()
        self.assertIn(
            "The final report is the terminal disposition of the authorized action.",
            body,
        )

    def test_generic_approval_does_not_authorize_checkpoint(self):
        _, body = _frontmatter_and_body()
        self.assertIn("Generic approval phrases", body)
        self.assertIn(
            "BLOCKED_CLARIFICATION",
            body.split("Generic approval phrases", 1)[1],
        )

    def test_checkpoint_approval_record_has_all_required_sections(self):
        _, body = _frontmatter_and_body()
        self.assertIn("CHECKPOINT APPROVAL REQUIRED", body)
        for section in ("Approval covers", "Irreversible consequences", "Required verification"):
            with self.subTest(section=section):
                self.assertIn(section, body)
        self.assertIn("Reply APPROVE to authorize exactly the actions above.", body)

    def test_plan_modification_requires_dependent_re_evaluation(self):
        _, body = _frontmatter_and_body()
        self.assertIn("Re-evaluate all dependent claims", body)
        self.assertIn("Preservation of bytes is not preservation of semantics.", body)

    def test_preexisting_failure_cannot_be_reported_as_passing(self):
        _, body = _frontmatter_and_body()
        self.assertIn("UNVERIFIABLE", body)
        self.assertIn("distinguish targeted checks from repository-wide verification", body)

    def test_completion_gate_requires_all_mandatory_verifications(self):
        _, body = _frontmatter_and_body()
        self.assertIn("`COMPLETE` is allowed only when all of the following hold", body)
        self.assertIn("PREEXISTING_FAILURE", body)
        self.assertIn(
            "Targeted or alternative verification may be reported as supplementary evidence, but the original required verification remains `FAILED` or `UNVERIFIED`",
            body,
        )

    def test_verification_integrity_forbids_replacing_required_verification(self):
        _, body = _frontmatter_and_body()
        self.assertIn("A required verification must be evaluated exactly as defined in the active evidence contract.", body)
        self.assertIn("must not replace, weaken, narrow, reinterpret, or downgrade", body)
        self.assertIn("original required verification remains `FAILED` or `UNVERIFIED`", body)

    def test_approved_postconditions_require_demonstrated_evidence(self):
        _, body = _frontmatter_and_body()
        self.assertIn("Every material postcondition explicitly authorized in the checkpoint must either be demonstrated by post-change evidence or be reported as unverified.", body)
        self.assertIn("must not treat implementation intent, source-code presence, or an unexecuted code path as proof", body)

    def test_preexisting_failure_does_not_become_passing(self):
        _, body = _frontmatter_and_body()
        self.assertIn("Pre-existing failures affect attribution, not verification status.", body)
        self.assertIn("If fixing the pre-existing failure would expand scope beyond the authorized action, do not fix it without reclassification and authorization.", body)

    def test_checkpoint_authorization_does_not_cover_scope_or_evidence_relaxation(self):
        _, body = _frontmatter_and_body()
        self.assertIn("Approval authorizes execution of the stated scope", body)
        self.assertIn("it does not authorize changing the scope, relaxing evidence requirements, or accepting unsupported post-change claims.", body)

    def test_scope_must_not_expand_to_adjacent_functionality(self):
        _, body = _frontmatter_and_body()
        self.assertIn("Do not expand the requested scope merely because a component, transport, dependency, or subsystem is related to the changed behavior.", body)
        self.assertIn("Only remove adjacent functionality when repository evidence establishes that it is unused, incompatible with the authorized change, or explicitly included in the requested scope.", body)
        self.assertIn("When functionality can remain operational without the removed feature, preserve it unless the user authorizes its removal.", body)

    def test_unexecuted_required_verification_blocks_complete(self):
        _, body = _frontmatter_and_body()
        self.assertIn("An inability to execute a required verification is also insufficient evidence for `COMPLETE`", body)
        self.assertIn("UNVERIFIED", body)

    def test_verification_status_taxonomy_present(self):
        _, body = _frontmatter_and_body()
        for token in (
            "`PASS`",
            "`FAIL`",
            "`UNVERIFIED`",
            "`PREEXISTING_FAILURE`",
            "`BLOCKED_EVIDENCE`",
            "`BLOCKED_CLARIFICATION`",
            "`CHECKPOINT`",
            "`COMPLETE`",
        ):
            with self.subTest(token=token):
                self.assertIn(token, body)

    def test_static_vs_runtime_evidence_distinction(self):
        _, body = _frontmatter_and_body()
        self.assertIn("A source-level check is not proof of runtime behavior", body)
        self.assertIn("if runtime verification cannot be performed, the claim is `UNVERIFIED`, not `PASS` or `COMPLETE`", body)

    def test_baseline_capture_required_before_change(self):
        _, body = _frontmatter_and_body()
        self.assertIn("Before making changes, run the verification and capture the baseline result verbatim", body)
        self.assertIn("`PREEXISTING_FAILURE` only when the command still fails, the exact failures are demonstrably identical to the captured baseline", body)
        self.assertIn('Do not allow statements such as "zero new errors" merely because an error was previously described as pre-existing.', body)

    def test_impossible_mandatory_gate_forbidden(self):
        _, body = _frontmatter_and_body()
        self.assertIn("must never knowingly execute a plan containing an impossible mandatory verification and then call the result `COMPLETE`", body)

    def test_unrelated_failure_must_not_be_fixed_to_pass_verification(self):
        _, body = _frontmatter_and_body()
        self.assertIn("do not modify unrelated code merely to make the verification pass", body)
        self.assertIn("if removing E2EE exposes a pre-existing `ContactRequests.tsx` TypeScript error", body)

    def test_completion_gate_conditions_enumerated(self):
        _, body = _frontmatter_and_body()
        self.assertIn("`COMPLETE` is allowed only when all of the following hold", body)
        self.assertIn("the authorized change was actually executed", body)
        self.assertIn("every mandatory post-change claim has sufficient evidence", body)
        self.assertIn("no required claim is merely assumed", body)
        self.assertIn("no unauthorized scope expansion occurred", body)

    def test_completion_gate_required_provenance(self):
        _, body = _frontmatter_and_body()
        self.assertIn("`claim -> observed fact -> artifact/command/runtime result -> method -> limitation`", body)

    def test_mandatory_step3_classifies_static_vs_runtime(self):
        _, body = _frontmatter_and_body()
        step3_region = body.split("3. Create a claim-specific evidence contract", 1)[1].split("4. Gather proportional evidence", 1)[0]
        self.assertIn("`static`", step3_region)
        self.assertIn("`runtime`", step3_region)