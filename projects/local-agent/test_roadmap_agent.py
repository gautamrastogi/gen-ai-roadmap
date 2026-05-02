#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from roadmap_agent import core


class RoadmapAgentTests(unittest.TestCase):
    def test_load_progress_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            progress_path = Path(tmp) / "progress.json"
            progress_path.write_text(
                json.dumps(
                    {
                        "current_phase": 2,
                        "current_project": "p2-summarizer",
                        "completed_projects": ["p1-prompt-playground"],
                        "focus": "finish roadmap first",
                        "notes": ["keep it small"],
                    }
                ),
                encoding="utf-8",
            )

            progress = core.load_progress(progress_path)

        self.assertTrue(progress["available"])
        self.assertEqual(progress["current_phase"], 2)
        self.assertEqual(progress["current_project"], "p2-summarizer")
        self.assertEqual(progress["completed_projects"], ["p1-prompt-playground"])

    def test_missing_progress_file_fallback(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            progress = core.load_progress(Path(tmp) / "missing.json")

        self.assertFalse(progress["available"])
        self.assertIn("No local progress file found", progress["message"])
        self.assertEqual(progress["completed_projects"], [])

    def test_phase_extraction(self) -> None:
        phases = core.parse_phases()
        phase_ids = {phase.id for phase in phases}

        self.assertIn(2, phase_ids)
        self.assertIn(6, phase_ids)
        self.assertTrue(any(phase.projects for phase in phases))

    def test_next_task_output_has_required_sections(self) -> None:
        task = core.next_task()

        self.assertTrue(task["files_to_inspect"])
        self.assertGreaterEqual(len(task["steps"]), 3)
        self.assertTrue(task["verification_commands"])
        self.assertTrue(task["done_when"])

    def test_coach_falls_back_when_model_unavailable(self) -> None:
        original = core.call_local_model

        def failing_call(*_: object, **__: object) -> dict[str, object]:
            raise RuntimeError("model offline")

        core.call_local_model = failing_call
        try:
            task = core.coach_next_task()
        finally:
            core.call_local_model = original

        self.assertEqual(task["coach_mode"], "fallback")
        self.assertIn("model offline", task["coach_error"])
        self.assertIn("Continue Phase", task["coach_response"])

    def test_clean_coach_output_prefers_final_answer(self) -> None:
        raw = """
Thinking Process:
Draft:
**Next Move:** rough draft

Final:
Next Move: do the real thing
Why This Matters: because it is the final answer
Steps:
- one
Checks:
- two
Done When: complete

*Word Count:* 30
"""
        cleaned = core._clean_coach_output(raw)

        self.assertTrue(cleaned.startswith("Next Move: do the real thing"))
        self.assertNotIn("Thinking Process", cleaned)
        self.assertNotIn("Word Count", cleaned)


if __name__ == "__main__":
    unittest.main()
