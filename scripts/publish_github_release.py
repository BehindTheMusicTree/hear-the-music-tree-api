#!/usr/bin/env python3
"""Create a GitHub Release from CHANGELOG.md using the GitHub CLI (`gh`)."""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path


def _gh_token_from_actions() -> bool:
    return os.environ.get("GITHUB_ACTIONS") == "true" and bool(
        os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    )


def _git_root() -> Path:
    p = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        check=True,
        capture_output=True,
        text=True,
    )
    return Path(p.stdout.strip())


def _read_version(root: Path, explicit: str | None) -> str:
    if explicit:
        return explicit.removeprefix("v")
    return (root / "STANDARDS_VERSION").read_text(encoding="utf-8").strip().removeprefix("v")


def _extract_changelog_body(changelog_text: str, version: str) -> str | None:
    # Tags are vX.Y.Z; CHANGELOG may use ## [X.Y.Z] or ## [vX.Y.Z].
    bracket_versions = [version]
    if not version.startswith("v"):
        bracket_versions.append(f"v{version}")
    next_section = re.compile(r"^## \[")
    for bracket_ver in bracket_versions:
        header = re.compile(rf"^## \[{re.escape(bracket_ver)}\]")
        lines = changelog_text.splitlines(keepends=True)
        started = False
        out: list[str] = []
        for line in lines:
            if not started:
                if header.match(line):
                    started = True
                continue
            if next_section.match(line):
                break
            out.append(line)
        if not started:
            continue
        body = "".join(out).strip()
        return body + "\n" if body else "\n"
    return None


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Publish a GitHub Release for tag vX.Y.Z using the matching CHANGELOG section.",
    )
    parser.add_argument(
        "version",
        nargs="?",
        help="SemVer without v (default: STANDARDS_VERSION)",
    )
    parser.add_argument(
        "--draft",
        action="store_true",
        help="Create a draft release",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print release notes and gh command only",
    )
    args = parser.parse_args()

    root = _git_root()
    ver = _read_version(root, args.version)
    tag = f"v{ver}"

    changelog_path = root / "CHANGELOG.md"
    if not changelog_path.is_file():
        print("CHANGELOG.md not found.", file=sys.stderr)
        sys.exit(1)

    body = _extract_changelog_body(changelog_path.read_text(encoding="utf-8"), ver)
    if body is None:
        print(f"No '## [{ver}]' or '## [v{ver}]' section found in CHANGELOG.md.", file=sys.stderr)
        sys.exit(1)

    if args.dry_run:
        print(f"--- Release notes for {tag} ---\n{body}", end="")
        cmd = [
            "gh",
            "release",
            "create",
            tag,
            "--verify-tag",
            "--title",
            tag,
            "--notes-file",
            "<tmp>",
        ]
        if args.draft:
            cmd.append("--draft")
        print("Would run:", " ".join(cmd).replace("<tmp>", "(changelog body)"))
        return

    if not _gh_token_from_actions():
        gh_check = subprocess.run(
            ["gh", "auth", "status"],
            capture_output=True,
            check=False,
        )
        if gh_check.returncode != 0:
            print(
                "GitHub CLI is not logged in. Run `gh auth login` and retry.",
                file=sys.stderr,
            )
            sys.exit(1)

    tag_check = subprocess.run(
        ["git", "rev-parse", "--verify", f"{tag}^{{commit}}"],
        capture_output=True,
        cwd=root,
        check=False,
    )
    if tag_check.returncode != 0:
        print(
            f"Git tag {tag} not found locally. Create and push the tag first.",
            file=sys.stderr,
        )
        sys.exit(1)

    view = subprocess.run(
        ["gh", "release", "view", tag],
        capture_output=True,
        cwd=root,
        check=False,
    )
    if view.returncode == 0:
        print(f"Release {tag} already exists. Nothing to do.", file=sys.stderr)
        sys.exit(0)

    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".md",
        encoding="utf-8",
        delete=False,
    ) as tmp:
        tmp.write(body)
        tmp_path = tmp.name

    try:
        cmd = [
            "gh",
            "release",
            "create",
            tag,
            "--verify-tag",
            "--title",
            tag,
            "--notes-file",
            tmp_path,
        ]
        if args.draft:
            cmd.append("--draft")
        subprocess.run(cmd, check=True, cwd=root)
    finally:
        Path(tmp_path).unlink(missing_ok=True)

    print(f"Published GitHub release {tag}.")


if __name__ == "__main__":
    main()
