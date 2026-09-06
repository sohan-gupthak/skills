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
    def test_evidence_ledger_section_present(self):
        _, body = _frontmatter_and_body()
        self.assertIn("## Evidence Ledger for persistent state", body)
        self.assertIn("references/evidence-ledger.md", body)
    def test_evidence_ledger_record_not_evidence_principle(self):
        _, body = _frontmatter_and_body()
        self.assertIn("The ledger is a record, not evidence", body)
        self.assertIn("UNVERIFIED", body)
    def test_evidence_ledger_risk_tiers_required(self):
        _, body = _frontmatter_and_body()
        ledger_region = body.split("Evidence Ledger for persistent state", 1)[1]
        for token in ("optional", "recommended", "mandatory"):
            with self.subTest(token=token):
                self.assertIn(token, ledger_region)
    def test_evidence_ledger_location_and_gitignore_rule(self):
        _, body = _frontmatter_and_body()
        self.assertIn(".evidence-gated/active/", body)
        self.assertIn("repository conventions and explicit user instructions take precedence", body)
        self.assertIn("must not silently modify `.gitignore`", body)
    def test_evidence_ledger_re_read_required_before_continuing(self):
        _, body = _frontmatter_and_body()
        self.assertIn("Re-read it before", body)
        for item in (
            "a new investigation phase",
            "a significant change execution",
            "requesting checkpoint approval",
            "any scope change",
            "any completion claim",
        ):
            with self.subTest(item=item):
                self.assertIn(item, body)
    def test_evidence_ledger_reference_template_loads(self):
        skill_root = _skill_path().parent
        reference = skill_root / "references" / "evidence-ledger.md"
        self.assertTrue(reference.exists(), f"missing {reference}")
        text = reference.read_text()
        for token in (
            "## Template",
            "## Source of truth hierarchy",
            "Approval and scope rules apply inside the ledger",
            "`PASS`",
            "`FAIL`",
            "`UNVERIFIED`",
            "`PREEXISTING_FAILURE`",
            "Completion gate inside the ledger",
        ):
            with self.subTest(token=token):
                self.assertIn(token, text)
    def test_step3_does_not_force_medium_risk_into_ledger(self):
        _, body = _frontmatter_and_body()
        step3_region = body.split("3. Create a claim-specific evidence contract", 1)[1].split("4. Gather proportional evidence", 1)[0]
        self.assertNotIn("For medium and high-risk work, record", step3_region)
        self.assertNotIn("For high-risk work, baseline", step3_region)
        self.assertIn("risk-tiered policy in", step3_region)
    def test_source_of_truth_hierarchy_is_two_axis(self):
        for path in (_skill_path(), _skill_path().parent / "references" / "evidence-ledger.md"):
            with self.subTest(path=str(path)):
                text = path.read_text()
                self.assertIn("Authority depends on what is being established", text)
                self.assertIn("intent, authorization, desired scope, and acceptable tradeoffs", text)
                self.assertIn("factual repository state, runtime behavior, and verification results", text.replace("\n", " "))

    def test_ledger_separates_phase_from_disposition(self):
        for path in (_skill_path(), _skill_path().parent / "references" / "evidence-ledger.md"):
            with self.subTest(path=str(path)):
                text = path.read_text()
                self.assertIn("Operational Phase", text)
                self.assertIn("Disposition", text)
                for phase in ("DRAFT", "INVESTIGATING", "EXECUTING", "VERIFYING"):
                    with self.subTest(phase=phase):
                        self.assertIn(phase, text)
    def test_template_header_splits_phase_and_disposition(self):
        reference = _skill_path().parent / "references" / "evidence-ledger.md"
        text = reference.read_text()
        template_start = text.split("```md\n# Evidence Ledger", 1)[1].split("```", 1)[0]
        self.assertIn("## Operational Phase", template_start)
        self.assertIn("## Disposition", template_start)
        for phase in ("DRAFT", "INVESTIGATING", "EXECUTING", "VERIFYING"):
            with self.subTest(phase=phase):
                self.assertIn(phase, template_start)
        for disposition in ("BLOCKED_CLARIFICATION", "BLOCKED_EVIDENCE", "ALLOW", "ALLOW_WITH_VERIFICATION", "CHECKPOINT", "COMPLETE"):
            with self.subTest(disposition=disposition):
                self.assertIn(disposition, template_start)

    def test_freshness_section_present_in_skill(self):
        _, body = _frontmatter_and_body()
        freshness_region = body.split("## Evidence freshness and invalidation", 1)[1]
        self.assertIn("`VALID`", freshness_region)
        self.assertIn("`STALE`", freshness_region)
        self.assertIn("`INVALIDATED`", freshness_region)
        self.assertIn("`RE-VERIFIED`", freshness_region)
        self.assertIn("references/evidence-ledger.md", freshness_region)

    def test_freshness_is_state_dependent_not_merely_time(self):
        _, body = _frontmatter_and_body()
        freshness_region = body.split("## Evidence freshness and invalidation", 1)[1]
        self.assertIn("state dependency", freshness_region)
        self.assertIn("wall-clock time", freshness_region)
        self.assertIn("time", freshness_region.lower())

    def test_freshness_requires_material_change_not_every_edit(self):
        _, body = _frontmatter_and_body()
        freshness_region = body.split("## Evidence freshness and invalidation", 1)[1]
        self.assertIn("material change", freshness_region)
        self.assertIn("typo", freshness_region)

    def test_stale_or_invalidated_evidence_blocks_completion(self):
        _, body = _frontmatter_and_body()
        freshness_region = body.split("## Evidence freshness and invalidation", 1)[1]
        self.assertIn("`STALE`", freshness_region)
        self.assertIn("`INVALIDATED`", freshness_region)
        self.assertIn("`COMPLETE`", freshness_region)
        self.assertIn("mandatory", freshness_region)

    def test_freshness_preserves_history_and_avoids_silent_deletion(self):
        _, body = _frontmatter_and_body()
        freshness_region = body.split("## Evidence freshness and invalidation", 1)[1]
        self.assertIn("silently deleted", freshness_region)
        self.assertIn("preserve", freshness_region.lower())

    def test_freshness_distinguishes_baseline_from_current_verification(self):
        _, body = _frontmatter_and_body()
        freshness_region = body.split("## Evidence freshness and invalidation", 1)[1]
        self.assertIn("baseline", freshness_region.lower())
        self.assertIn("pre-change", freshness_region)

    def test_freshness_does_not_replace_runtime_evidence_with_static(self):
        _, body = _frontmatter_and_body()
        freshness_region = body.split("## Evidence freshness and invalidation", 1)[1]
        self.assertIn("runtime", freshness_region.lower())
        self.assertIn("static", freshness_region.lower())

    def test_freshness_does_not_silently_invalidate_authorization(self):
        _, body = _frontmatter_and_body()
        freshness_region = body.split("## Evidence freshness and invalidation", 1)[1]
        self.assertIn("authorization", freshness_region.lower())
        self.assertIn("checkpoint", freshness_region.lower())

    def test_ledger_defines_validity_states(self):
        reference = _skill_path().parent / "references" / "evidence-ledger.md"
        text = reference.read_text()
        region = text.split("## Evidence freshness and validity", 1)[1].split("## Source of truth hierarchy", 1)[0]
        for token in ("`VALID`", "`STALE`", "`INVALIDATED`", "`RE-VERIFIED`"):
            with self.subTest(token=token):
                self.assertIn(token, region)
        self.assertIn("history", region.lower())

    def test_ledger_documents_state_dependency_not_just_age(self):
        reference = _skill_path().parent / "references" / "evidence-ledger.md"
        text = reference.read_text()
        region = text.split("## Evidence freshness and validity", 1)[1].split("## Source of truth hierarchy", 1)[0]
        self.assertIn("state dependency", region)
        self.assertIn("wall-clock time", region)

    def test_ledger_documents_re_evaluation_procedure(self):
        reference = _skill_path().parent / "references" / "evidence-ledger.md"
        text = reference.read_text()
        region = text.split("## Evidence freshness and validity", 1)[1].split("## Source of truth hierarchy", 1)[0]
        for token in (
            "Re-evaluation procedure",
            "Identify affected claims",
            "Identify supporting evidence",
            "Determine impact",
            "Record the reason",
            "Re-verify when required",
            "Preserve history",
        ):
            with self.subTest(token=token):
                self.assertIn(token, region)

    def test_ledger_template_tracks_validity_dependencies_history(self):
        reference = _skill_path().parent / "references" / "evidence-ledger.md"
        text = reference.read_text()
        template_start = text.split("```md\n# Evidence Ledger", 1)[1].split("```", 1)[0]
        self.assertIn("**Validity:**", template_start)
        for token in ("VALID", "STALE", "INVALIDATED", "RE-VERIFIED"):
            with self.subTest(token=token):
                self.assertIn(token, template_start)
        self.assertIn("**Dependencies / Conditions:**", template_start)
        self.assertIn("**Freshness Review:**", template_start)
        self.assertIn("**Invalidation / Staleness History:**", template_start)

    def test_ledger_completion_gate_blocks_on_stale_or_invalidated(self):
        reference = _skill_path().parent / "references" / "evidence-ledger.md"
        text = reference.read_text()
        region = text.split("## Completion gate inside the ledger", 1)[1]
        self.assertIn("`STALE`", region)
        self.assertIn("`INVALIDATED`", region)
        self.assertIn("`COMPLETE`", region)
        self.assertIn("`BLOCKED_EVIDENCE`", region)

    def test_ledger_preserves_baseline_distinct_from_current_verification(self):
        reference = _skill_path().parent / "references" / "evidence-ledger.md"
        text = reference.read_text()
        region = text.split("## Completion gate inside the ledger", 1)[1]
        self.assertIn("baseline", region.lower())
        self.assertIn("historical", region.lower())

    def test_existing_ledger_principles_remain_intact_after_freshness(self):
        for path in (_skill_path(), _skill_path().parent / "references" / "evidence-ledger.md"):
            with self.subTest(path=str(path)):
                text = path.read_text()
                self.assertIn("The ledger is a record, not evidence", text)
                self.assertIn("Authority depends on what is being established", text)
                self.assertIn("two-axis", text.lower())
                self.assertIn("every mandatory verification", text.lower())
                self.assertIn("Operational Phase", text)
                self.assertIn("Disposition", text)

    def test_re_verified_is_current_validity_not_merely_transition(self):
        reference = _skill_path().parent / "references" / "evidence-ledger.md"
        text = reference.read_text()
        region = text.split("## Evidence freshness and validity", 1)[1].split("## Source of truth hierarchy", 1)[0]
        self.assertIn("current-validity state", region)
        self.assertIn("not merely a historical transition", region)
        self.assertIn("Both `VALID` and `RE-VERIFIED` legitimately satisfy the completion gate", region)

    def test_completion_gate_uses_current_validity_status(self):
        reference = _skill_path().parent / "references" / "evidence-ledger.md"
        text = reference.read_text()
        region = text.split("## Completion gate inside the ledger", 1)[1]
        self.assertIn("**current**", region)
        self.assertIn("Historical stale or invalidation history must not", region)
        self.assertIn("permanently block completion", region)
        self.assertIn("may return to `VALID`", region)
        self.assertIn("the new evidence record is `RE-VERIFIED`", region)