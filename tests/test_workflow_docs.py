"""Validate maintained workflow templates without executing their mutations."""

import json
import os
from pathlib import Path
import re
import shlex
import shutil
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / "docs/wood-delivery-workflow.md"


def command_blocks():
    text = WORKFLOW.read_text()
    return [
        [shlex.split(line) for line in block.splitlines() if line.startswith("wood ")]
        for block in re.findall(r"```text\n(.*?)\n```", text, re.S)
    ]


class WorkflowDocumentationTest(unittest.TestCase):
    def test_relative_document_links_resolve(self):
        documents = [ROOT / "AGENTS.md", ROOT / "README.md"]
        for directory in ("skills", "docs", "overrides"):
            documents.extend((ROOT / directory).rglob("*.md"))
        for document in documents:
            for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", document.read_text()):
                if "://" in target or target.startswith("#"):
                    continue
                with self.subTest(document=document.relative_to(ROOT), target=target):
                    path = target.split("#", 1)[0]
                    self.assertTrue((document.parent / path).exists())

    def test_templates_use_json_and_preview_identical_mutations(self):
        blocks = command_blocks()
        self.assertEqual(len(blocks), 3)
        for commands in blocks:
            for index, command in enumerate(commands):
                with self.subTest(command=command):
                    self.assertIn("--json", command)
                    if "--apply" not in command:
                        continue
                    preview = command.copy()
                    preview.remove("--apply")
                    if "--plan-hash" in preview:
                        offset = preview.index("--plan-hash")
                        self.assertEqual(preview[offset + 1], "<reviewed-hash>")
                        del preview[offset:offset + 2]
                    self.assertGreater(index, 0)
                    self.assertEqual(commands[index - 1], preview)

    def test_story_records_flow_into_closeout(self):
        commands = command_blocks()[0]
        names = [" ".join(command[1:3]) for command in commands]
        self.assertLess(names.index("repo validate"), names.index("ci status"))
        self.assertLess(names.index("ci status"), names.index("delivery status"))
        self.assertLess(names.index("delivery status"), names.index("repo verify"))
        self.assertLess(names.index("repo verify"), names.index("story evidence"))
        self.assertLess(names.index("story evidence"), names.index("story activity"))
        self.assertLess(names.index("story activity"), names.index("story complete"))
        evidence = [command for command in commands if command[1:3] == ["story", "evidence"]]
        for command in evidence:
            self.assertEqual(command[command.index("--validation") + 1], "<validation-file>")
            self.assertEqual(command[command.index("--verification") + 1], "<verification-file>")
            self.assertEqual(command[command.index("--ci-run") + 1], "<run-id>")
        consumers = [command for command in commands if "--evidence" in command]
        self.assertTrue(consumers)
        for command in consumers:
            self.assertEqual(command[command.index("--evidence") + 1], "<evidence-file>")

    def test_summary_edit_has_observed_content_precondition(self):
        for command in command_blocks()[1][1:]:
            self.assertEqual(command[command.index("--expected-sha256") + 1], "<observed-hash>")
            self.assertIn("--evidence", command)

    def test_retained_helpers_exist_and_no_legacy_entrypoints_are_documented(self):
        text = WORKFLOW.read_text()
        helpers = re.findall(r"\| `([^`]+\.(?:py|sh))` \|", text)
        self.assertEqual(len(helpers), 4)
        for helper in helpers:
            self.assertTrue((ROOT / helper).is_file(), helper)
        for document in [ROOT / "README.md", ROOT / "AGENTS.md", WORKFLOW,
                         *list((ROOT / "skills").rglob("*.md"))]:
            self.assertNotRegex(document.read_text(), r"\bwood-(?:next-story|set-story-status|close-story|project|repo|openproject)\b")

    def test_templates_match_selected_wood_contract_and_options(self):
        executable = os.environ.get("CODEX_WOOD_EXECUTABLE") or shutil.which("wood")
        if not executable:
            self.skipTest("No Wood Tools executable; set CODEX_WOOD_EXECUTABLE for integration.")
        result = subprocess.run([executable, "contract", "--json"], capture_output=True,
                                text=True, timeout=15, check=True)
        capabilities = json.loads(result.stdout)["data"]["capabilities"]
        help_outputs = {}
        for command in [command for block in command_blocks() for command in block]:
            with self.subTest(command=command):
                matches = [name for name in capabilities
                           if command[1:1 + len(name.split())] == name.split()]
                self.assertTrue(matches, f"Unsupported command: {command}")
                capability = max(matches, key=len)
                if capability not in help_outputs:
                    help_result = subprocess.run([executable, *capability.split(), "--help"],
                                                 capture_output=True, text=True,
                                                 timeout=15, check=True)
                    help_outputs[capability] = help_result.stdout
                supported = set(re.findall(r"--[a-z][a-z0-9-]*", help_outputs[capability]))
                declared = {item for item in command if item.startswith("--")}
                self.assertFalse(declared - supported, f"Unsupported options: {declared - supported}")


if __name__ == "__main__":
    unittest.main()
