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
