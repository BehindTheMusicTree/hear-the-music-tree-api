"""Test release preparation using disposable Git repositories and a fake bump CLI."""

import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("preparation", ROOT / "scripts/prepare_release_bump.py")
prep = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prep)


class PreparationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        for name in ("VERSION", "package.json", "pyproject.toml", "CHANGELOG.md"):
            shutil.copy(ROOT / name, self.root / name)
        self.git("init", "-q", "-b", "main")
        self.git("config", "user.email", "fixture@example.test")
        self.git("config", "user.name", "Fixture")
        self.commit()
        self.patches = [
            patch.object(prep, "REPO_ROOT", self.root),
            patch.object(prep, "CHANGELOG_PATH", self.root / "CHANGELOG.md"),
            patch.object(prep.shutil, "which", return_value="/fake/bump-my-version"),
        ]
        for item in self.patches:
            item.start()
            self.addCleanup(item.stop)

    def git(self, *args):
        return subprocess.check_output(["git", *args], cwd=self.root, text=True).strip()

    def commit(self):
        self.git("add", ".")
        self.git("-c", "core.hooksPath=/dev/null", "commit", "-qm", "fixture")

    def test_main_develop_and_detached_fail_without_writes(self):
        for name in ("main", "develop", "detached"):
            if name == "develop":
                self.git("switch", "-qc", name)
            elif name == "detached":
                self.git("checkout", "--detach", "-q")
            with self.assertRaises(SystemExit):
                prep._require_preparation_state()
            assert self.git("status", "--porcelain") == ""

    def test_clean_release_and_hotfix_pass_but_dirty_fails(self):
        self.git("switch", "-qc", "release/fixture")
        prep._require_preparation_state()
        self.git("switch", "-qc", "hotfix/fixture")
        prep._require_preparation_state()
        (self.root / "VERSION").write_text("dirty")
        with self.assertRaises(SystemExit):
            prep._require_preparation_state()

    def test_mismatched_versions_and_tagging_configuration_fail(self):
        self.git("switch", "-qc", "release/fixture")
        p = self.root / "package.json"
        data = json.loads(p.read_text())
        data["version"] = "0.0.0"
        p.write_text(json.dumps(data))
        self.commit()
        with self.assertRaises(SystemExit):
            prep._require_preparation_state()

    def test_empty_notes_fail_before_bump_or_write(self):
        self.git("switch", "-qc", "release/fixture")
        p = self.root / "CHANGELOG.md"
        p.write_text(
            "**Note:** During releases, maintainers will move entries from Unreleased.\n\n## [Unreleased]\n\n### Changed\n<!-- draft -->\n"
        )
        self.commit()
        with patch.object(sys, "argv", ["prepare", "patch"]), patch.object(prep, "_run_bump_my_version") as bump:
            with self.assertRaises(SystemExit):
                prep.main()
            bump.assert_not_called()
        assert self.git("status", "--porcelain") == ""

    def test_preparation_edits_only_files_without_tag_cleanup(self):
        self.git("switch", "-qc", "release/fixture")
        current = (self.root / "VERSION").read_text().strip()
        major, minor, patch_version = map(int, current.split("."))
        target = f"{major}.{minor}.{patch_version + 1}"
        (self.root / "CHANGELOG.md").write_text(
            "**Note:** During releases, maintainers will move entries from Unreleased.\n\n"
            "## [Unreleased]\n\n### Changed\n\n- Prepare a fixture release.\n"
        )
        self.commit()
        head = self.git("rev-parse", "HEAD")

        def bump(kind, allow_dirty):
            assert (kind, allow_dirty) == ("patch", True)
            p = self.root / "CHANGELOG.md"
            p.write_text(p.read_text().replace(prep.MARKER_HEADING, f"## [{target}] - 2026-11-05"))
            (self.root / "VERSION").write_text(f"{target}\n")

        with (
            patch.object(sys, "argv", ["prepare", "patch"]),
            patch.object(prep, "_run_bump_my_version", side_effect=bump),
            patch.object(prep, "_run_fix_changelog"),
        ):
            prep.main()
        assert self.git("rev-parse", "HEAD") == head
        assert self.git("tag") == ""
        assert f"## [Unreleased]\n\n## [{target}]" in (self.root / "CHANGELOG.md").read_text()

    def test_local_publication_refused_and_preview_succeeds(self):
        for dry in (False, True):
            command = [sys.executable, str(ROOT / "scripts/publish_github_release.py"), "8.1.0"]
            if dry:
                command.append("--dry-run")
            result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=False)
            assert (result.returncode == 0) == dry
            if not dry:
                assert "CI owns" in result.stderr


if __name__ == "__main__":
    unittest.main()
