"""Focused behavior checks for bounded output, token accounting, and discovery."""

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class HelpersTest(unittest.TestCase):
    def test_installer_leaves_neighboring_wood_tools_checkout_untouched(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            source = home / "codex-config"
            (source / "scripts").mkdir(parents=True)
            (source / "skills").mkdir()
            (source / "AGENTS.md").write_text("guidance")
            installer = source / "scripts/install.sh"
            installer.write_bytes((ROOT / "scripts/install.sh").read_bytes())
            neighbor = home / "Projects/internal/Wood Tools/wood-tools"
            (neighbor / ".git/info").mkdir(parents=True)
            exclude = neighbor / ".git/info/exclude"
            exclude.write_text("# existing local excludes\n")
            subprocess.run(["/bin/sh", str(installer)],
                           env={**os.environ, "HOME": directory}, check=True)
            self.assertEqual(exclude.read_text(), "# existing local excludes\n")
            self.assertFalse((neighbor / "AGENTS.override.md").is_symlink())
            self.assertFalse((neighbor / "AGENTS.override.md").exists())

    def test_installer_keeps_story_skill_canonical_and_propagates_updates(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source"
            home = root / "profiles"
            (source / "scripts").mkdir(parents=True)
            skill = source / "skills/openproject-development-workflow"
            skill.mkdir(parents=True)
            canonical = ROOT / "skills/openproject-development-workflow/SKILL.md"
            (skill / "SKILL.md").write_bytes(canonical.read_bytes())
            (source / "AGENTS.md").write_bytes((ROOT / "AGENTS.md").read_bytes())
            installer = source / "scripts/install.sh"
            installer.write_bytes((ROOT / "scripts/install.sh").read_bytes())
            env = {**os.environ, "HOME": str(home)}
            subprocess.run(["/bin/sh", str(installer)], env=env, check=True)
            installed = [home / profile / "skills" / skill.name
                         for profile in (".codex", ".codex-secondary")]
            for link in installed:
                self.assertTrue(link.is_symlink())
                self.assertEqual(link.resolve(), skill.resolve())
                self.assertEqual((link / "SKILL.md").read_bytes(), canonical.read_bytes())
            # Canonical changes propagate to both profiles without copying or rewriting.
            updated = canonical.read_bytes() + b"\nCanonical update fixture.\n"
            (skill / "SKILL.md").write_bytes(updated)
            subprocess.run(["/bin/sh", str(installer)], env=env, check=True)
            for link in installed:
                self.assertEqual((link / "SKILL.md").read_bytes(), updated)

    def test_installer_refuses_divergent_story_skill_without_overwriting(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "scripts").mkdir()
            skill = root / "skills/openproject-development-workflow"
            skill.mkdir(parents=True)
            (skill / "SKILL.md").write_bytes(
                (ROOT / "skills/openproject-development-workflow/SKILL.md").read_bytes())
            (root / "AGENTS.md").write_text("guidance")
            installer = root / "scripts/install.sh"
            installer.write_bytes((ROOT / "scripts/install.sh").read_bytes())
            divergent = root / ".codex/skills" / skill.name
            divergent.mkdir(parents=True)
            (divergent / "SKILL.md").write_text("local divergent content")
            result = subprocess.run(["/bin/sh", str(installer)],
                                    env={**os.environ, "HOME": directory},
                                    capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn(str(divergent), result.stderr)
            self.assertEqual((divergent / "SKILL.md").read_text(), "local divergent content")

    def test_brief_check_success(self):
        with tempfile.TemporaryDirectory() as directory:
            result = subprocess.run(
                [sys.executable, str(ROOT / "scripts/brief-check.py"), "--log-dir", directory, "--", sys.executable, "-c", "print('ready')"],
                capture_output=True, text=True, check=True,
            )
            report = json.loads(result.stdout)
            self.assertTrue(report["success"])
            self.assertEqual(report["exit_code"], 0)
            self.assertEqual(report["failure_summary"], "")
            self.assertEqual(Path(report["raw_log_path"]).read_text(), "ready\n")

    def test_brief_check_keeps_full_log_and_bounds_json(self):
        with tempfile.TemporaryDirectory() as directory:
            result = subprocess.run(
                [sys.executable, str(ROOT / "scripts/brief-check.py"), "--log-dir", directory, "--", sys.executable, "-c", "import sys; print('x' * 1000); print('ERROR: broken', file=sys.stderr); raise SystemExit(3)"],
                capture_output=True, text=True, check=True,
            )
            report = json.loads(result.stdout)
            self.assertEqual(report["exit_code"], 3)
            self.assertFalse(report["success"])
            self.assertIn(sys.executable, report["command"])
            self.assertLess(len(result.stdout), 1000)
            self.assertIn("ERROR: broken", report["failure_summary"])
            self.assertIn("x" * 1000, Path(report["raw_log_path"]).read_text())

    def test_brief_check_large_output_stays_bounded(self):
        with tempfile.TemporaryDirectory() as directory:
            result = subprocess.run(
                [sys.executable, str(ROOT / "scripts/brief-check.py"), "--log-dir", directory, "--", sys.executable, "-c", "for _ in range(20000): print('x' * 100)"],
                capture_output=True, text=True, check=True,
            )
            report = json.loads(result.stdout)
            self.assertTrue(report["success"])
            self.assertLess(len(result.stdout), 1000)
            self.assertEqual(report["line_count"], 20000)
            self.assertGreater(Path(report["raw_log_path"]).stat().st_size, 2_000_000)

    def test_token_report_uses_latest_cumulative_usage(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            session = home / "sessions/2026/09/25/test.jsonl"
            session.parent.mkdir(parents=True)
            events = [
                {"type": "session_meta", "payload": {"id": "abc"}},
                {"type": "event_msg", "payload": {"type": "token_count", "info": {"total_token_usage": {"input_tokens": 10, "cached_input_tokens": 3, "output_tokens": 2}, "last_token_usage": {"input_tokens": 10}}}},
                {"type": "response_item", "payload": {"type": "function_call_output"}},
                {"type": "event_msg", "payload": {"type": "token_count", "info": {"total_token_usage": {"input_tokens": 20, "cached_input_tokens": 8, "output_tokens": 5}, "last_token_usage": {"input_tokens": 10}}}},
            ]
            session.write_text("\n".join(json.dumps(event) for event in events))
            result = subprocess.run([sys.executable, str(ROOT / "scripts/token-report.py"), "--codex-home", directory], capture_output=True, text=True, check=True)
            report = json.loads(result.stdout)
            self.assertEqual(report["totals"], {"input_tokens": 20, "cached_input_tokens": 8, "output_tokens": 5, "request_count": 2, "tool_result_count": 1})

    def test_installer_discovers_new_skill_in_both_homes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "scripts").mkdir()
            (root / "skills/new-skill").mkdir(parents=True)
            (root / "skills/new-skill/SKILL.md").write_text("---\nname: new-skill\n---\n")
            (root / "AGENTS.md").write_text("guidance")
            (root / "scripts/install.sh").write_bytes((ROOT / "scripts/install.sh").read_bytes())
            env = {"HOME": directory, "PATH": "/usr/bin:/bin"}
            subprocess.run(["/bin/sh", str(root / "scripts/install.sh")], env=env, check=True)
            for name in (".codex", ".codex-secondary"):
                self.assertEqual((root / name / "skills/new-skill").resolve(), (root / "skills/new-skill").resolve())
                self.assertEqual((root / name / "AGENTS.md").resolve(), (root / "AGENTS.md").resolve())


if __name__ == "__main__":
    unittest.main()
