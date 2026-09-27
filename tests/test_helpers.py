"""Focused behavior checks for bounded output, token accounting, and discovery."""

import json
import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import types
import unittest
from dataclasses import dataclass
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]


class HelpersTest(unittest.TestCase):
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
            (root / "scripts/openproject").mkdir()
            (root / "skills/new-skill").mkdir(parents=True)
            (root / "skills/new-skill/SKILL.md").write_text("---\nname: new-skill\n---\n")
            (root / "AGENTS.md").write_text("guidance")
            (root / "scripts/install.sh").write_bytes((ROOT / "scripts/install.sh").read_bytes())
            helper = root / "scripts/openproject/wood_openproject_env.py"
            helper.write_bytes((ROOT / "scripts/openproject/wood_openproject_env.py").read_bytes())
            env = {"HOME": directory, "PATH": "/usr/bin:/bin"}
            subprocess.run(["/bin/sh", str(root / "scripts/install.sh")], env=env, check=True)
            for name in (".codex", ".codex-secondary"):
                self.assertEqual((root / name / "skills/new-skill").resolve(), (root / "skills/new-skill").resolve())
                self.assertEqual((root / name / "AGENTS.md").resolve(), (root / "AGENTS.md").resolve())
            self.assertEqual((root / ".wood/scripts/wood_openproject_env.py").resolve(), helper.resolve())

    def test_openproject_helper_uses_supported_client_settings(self):
        @dataclass(frozen=True)
        class Settings:
            base_url: str
            project_id: str
            token: str
            token_provider: str
            user_agent: str

        class Client:
            def __init__(self, settings):
                self.settings = settings

        package = types.ModuleType("wood_project")
        openproject = types.ModuleType("wood_project.openproject")
        openproject.OpenProjectSettings = Settings
        openproject.OpenProjectClient = Client
        source = ROOT / "scripts/openproject/wood_openproject_env.py"
        spec = importlib.util.spec_from_file_location("tested_wood_openproject_env", source)
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = importlib.util.module_from_spec(spec)
        with tempfile.TemporaryDirectory() as directory, mock.patch.dict(
            sys.modules, {"wood_project": package, "wood_project.openproject": openproject}
        ):
            spec.loader.exec_module(module)
            module.GLOBAL_CREDENTIAL_FILE = Path(directory) / "absent.env"
            client = module.client_from_env(
                {"OPENPROJECT_URL": "https://projects.example.test/",
                 "OPENPROJECT_PROJECT_ID": "3", "OPENPROJECT_INITIATIVE_ID": "208",
                 "OPENPROJECT_API_TOKEN": "test-token"},
                user_agent="test-next-story",
            )
        self.assertEqual(client.settings.base_url, "https://projects.example.test")
        self.assertEqual(client.settings.project_id, "3")
        self.assertEqual(client.settings.token, "test-token")
        self.assertEqual(client.settings.user_agent, "test-next-story")

    def test_installer_adopts_matching_openproject_helper_and_rejects_differences(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "scripts/openproject").mkdir(parents=True)
            (root / "AGENTS.md").write_text("guidance")
            (root / "scripts/install.sh").write_bytes((ROOT / "scripts/install.sh").read_bytes())
            source = root / "scripts/openproject/wood_openproject_env.py"
            source.write_bytes((ROOT / "scripts/openproject/wood_openproject_env.py").read_bytes())
            target = root / ".wood/scripts/wood_openproject_env.py"
            target.parent.mkdir(parents=True)
            target.write_bytes(source.read_bytes())
            env = {"HOME": directory, "PATH": "/usr/bin:/bin"}
            subprocess.run(["/bin/sh", str(root / "scripts/install.sh")], env=env, check=True)
            self.assertTrue(target.is_symlink())
            self.assertEqual(target.resolve(), source.resolve())
            subprocess.run(["/bin/sh", str(root / "scripts/install.sh")], env=env, check=True)
            target.unlink()
            target.write_text("locally modified")
            result = subprocess.run(
                ["/bin/sh", str(root / "scripts/install.sh")], env=env,
                capture_output=True, text=True, check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Existing path needs review", result.stderr)
            self.assertEqual(target.read_text(), "locally modified")


if __name__ == "__main__":
    unittest.main()
