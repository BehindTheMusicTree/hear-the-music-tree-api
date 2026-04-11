#!/usr/bin/env python3
"""Prepare a release version bump in one step (on a release/* branch from develop).

1. Sets the live ``## [Unreleased]`` line after the maintainer Note to
   ``## [Unreleased]  <!-- release -->`` for bump2version.
2. Runs bump2version (patch, minor, or major).
3. Runs ``fix_changelog_after_bump.py`` (release date, indent cleanup).
4. Inserts an empty ``## [Unreleased]`` above the new ``## [vX.Y.Z] - …`` heading.

Must be run **inside an activated project virtualenv** (or with that venv's
``python``), after ``pip install -e ".[dev]"`` so ``bump2version`` is
on PATH.

From repo root::

    python3 scripts/prepare_release_bump.py patch
    python3 scripts/prepare_release_bump.py minor --no-allow-dirty

``--no-allow-dirty``: do not pass ``--allow-dirty`` to bump2version (default is to
allow a dirty tree so step 1 can change CHANGELOG.md without a prior commit).
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import NoReturn


REPO_ROOT = Path(__file__).resolve().parent.parent
CHANGELOG_PATH = REPO_ROOT / "CHANGELOG.md"
NOTE_PREFIX = "**Note:** During releases, maintainers will move entries from"
FIRST_RELEASE_HEADING = re.compile(r"\n\n(## \[[^\]]+\][^\n]*)")
RELEASE_VERSION_HEADING = re.compile(
    r"^## \[v\d+\.\d+\.\d+\] - (\d{4}-\d{2}-\d{2}|YYYY-MM-DD)\s*$",
    re.MULTILINE,
)
MARKER_HEADING = "## [Unreleased]  <!-- release -->"


def _fail(msg: str) -> NoReturn:
    print(msg, file=sys.stderr)
    sys.exit(1)


def _require_venv() -> None:
    base = getattr(sys, "base_prefix", sys.prefix)
    if sys.prefix != base:
        return
    _fail(
        "prepare_release_bump.py must run inside a Python virtual environment.\n"
        "Create and use the project venv, install deps, then retry. Example:\n"
        "  python3 -m venv .venv && source .venv/bin/activate "
        '&& pip install -e ".[dev]"\n'
        "  python3 scripts/prepare_release_bump.py patch"
    )


def _find_note_index(text: str) -> int:
    idx = text.find(NOTE_PREFIX)
    if idx == -1:
        _fail(f"CHANGELOG.md: missing maintainer note starting with {NOTE_PREFIX!r}.")
    return idx


def _first_h2_after_note(text: str) -> tuple[int, str]:
    idx = _find_note_index(text)
    rest = text[idx:]
    m = FIRST_RELEASE_HEADING.search(rest)
    if not m:
        _fail("CHANGELOG.md: no ## heading found after blank line following the maintainer Note.")
    heading = m.group(1)
    abs_start = idx + m.start(1)
    return abs_start, heading


def ensure_bump_marker(text: str) -> tuple[str, bool]:
    abs_start, heading = _first_h2_after_note(text)
    if re.match(r"^## \[v\d+\.\d+\.\d+\] - ", heading):
        _fail(
            "CHANGELOG.md: first heading after the Note is already a released version. "
            "Restore an ## [Unreleased] section with pending notes first."
        )
    if heading == MARKER_HEADING:
        return text, False
    if heading == "## [Unreleased]":
        end = abs_start + len(heading)
        return text[:abs_start] + MARKER_HEADING + text[end:], True
    _fail(f"CHANGELOG.md: expected ## [Unreleased] after the Note, found {heading!r}.")


def ensure_empty_unreleased_section(text: str) -> tuple[str, bool]:
    idx = _find_note_index(text)
    tail = text[idx:]
    m = RELEASE_VERSION_HEADING.search(tail)
    if not m:
        _fail(
            "CHANGELOG.md: could not find ## [vX.Y.Z] - <date> after bump (expected version heading from bump2version)."
        )
    version_line_start = idx + m.start()
    head = text[:version_line_start]
    last_h2: str | None = None
    in_fenced_code_block = False
    for line in head.split("\n"):
        s = line.strip()
        if s.startswith("```"):
            in_fenced_code_block = not in_fenced_code_block
            continue
        if in_fenced_code_block:
            continue
        if s.startswith("## ") and not s.startswith("###"):
            last_h2 = s
    if last_h2 == "## [Unreleased]":
        return text, False
    insert = "## [Unreleased]\n\n"
    return text[:version_line_start] + insert + text[version_line_start:], True


def _run_bump2version(kind: str, allow_dirty: bool) -> None:
    if not shutil.which("bump2version"):
        _fail('bump2version not found on PATH. In your project venv run: pip install -e ".[dev]"')
    cmd = ["bump2version", kind]
    if allow_dirty:
        cmd.append("--allow-dirty")
    proc = subprocess.run(cmd, cwd=REPO_ROOT, check=False)
    if proc.returncode != 0:
        sys.exit(proc.returncode)


def _run_fix_changelog() -> None:
    fix_script = REPO_ROOT / "scripts" / "fix_changelog_after_bump.py"
    proc = subprocess.run([sys.executable, str(fix_script)], cwd=REPO_ROOT, check=False)
    if proc.returncode != 0:
        sys.exit(proc.returncode)


def _warn_branch() -> None:
    proc = subprocess.run(
        ["git", "branch", "--show-current"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        return
    branch = (proc.stdout or "").strip()
    if branch and not branch.startswith("release/"):
        print(
            f"Warning: current branch is {branch!r}; expected release/v* for Git Flow.\n",
            file=sys.stderr,
        )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "kind",
        choices=["patch", "minor", "major"],
        help="Semantic version segment to bump.",
    )
    parser.add_argument(
        "--no-allow-dirty",
        action="store_true",
        help="Omit --allow-dirty (bump2version refuses if the working tree is dirty).",
    )
    args = parser.parse_args()
    allow_dirty = not args.no_allow_dirty

    _require_venv()
    _warn_branch()
    raw = CHANGELOG_PATH.read_text()
    updated, changed = ensure_bump_marker(raw)
    if changed:
        CHANGELOG_PATH.write_text(updated)

    _run_bump2version(args.kind, allow_dirty)
    _run_fix_changelog()

    raw = CHANGELOG_PATH.read_text()
    updated, changed = ensure_empty_unreleased_section(raw)
    if changed:
        CHANGELOG_PATH.write_text(updated)

    print(
        "prepare_release_bump: done. Review git diff and CHANGELOG.md, then commit "
        "(e.g. chore: prepare release vX.Y.Z)."
    )


if __name__ == "__main__":
    main()
