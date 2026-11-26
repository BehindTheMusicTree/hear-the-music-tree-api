import subprocess
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import pytest_route


class ClassifyTests(unittest.TestCase):
    def test_empty_diff_applies(self):
        assert pytest_route.classify([]) == (True, [])

    def test_docs_only_is_skipped(self):
        assert pytest_route.classify(["README.md", "docs/workflows.md"]) == (False, [])

    def test_source_applies(self):
        assert pytest_route.classify(["hear/models.py"]) == (True, ["hear/models.py"])

    def test_mixed_diff_applies_and_reports_offending(self):
        assert pytest_route.classify(["README.md", "pyproject.toml"]) == (True, ["pyproject.toml"])

    def test_test_workflow_applies(self):
        assert pytest_route.classify([".github/workflows/test.yml"])[0]

    def test_org_workflow_is_skipped(self):
        assert not pytest_route.classify([".github/workflows/labeler.yml"])[0]

    def test_unknown_root_file_applies(self):
        assert pytest_route.classify(["something.cfg"])[0]


class MainTests(unittest.TestCase):
    def run_route(self, paths):
        return subprocess.run(
            [sys.executable, pytest_route.__file__],
            input="\0".join(paths).encode(),
            capture_output=True,
            check=True,
        ).stdout.decode()

    def test_inert_diff_prints_false(self):
        assert self.run_route(["README.md", "docs/a.md"]).strip() == "applicable=false"

    def test_code_diff_prints_true(self):
        assert self.run_route(["hear/models.py"]).strip() == "applicable=true"


if __name__ == "__main__":
    unittest.main()
