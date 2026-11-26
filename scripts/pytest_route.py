"""Route a PR to the full `Pytest` job or to a skip (BehindTheMusicTree/github-config#97).

Reads NUL-separated changed paths on stdin (`git diff --no-renames -z --name-only`, so a rename lists both names)
and prints `applicable=false` (skip pytest and coverage) or `applicable=true`, the scope output the `Tests success`
gate reads. Skip only when every path is explicitly known to have no effect on the suite; anything unknown, an empty
input or a mixed diff runs in full. Stdlib only: runs on the runner's system python.
Add a path here only after checking that `hear/`, `pyproject.toml` and what they import do not read it.
"""

import sys

SKIP_SUFFIXES = (".md",)
SKIP_FILES = frozenset(
    {
        "LICENSE",
        ".github/FUNDING.yml",
        ".github/labeler.yml",
        ".github/dependabot.yml",
        ".github/org-conformance.json",
        ".github/release-policy.json",
        ".github/actionlint.yaml",
        ".github/workflows/agent-drift.yml",
        ".github/workflows/branch-protection.yml",
        ".github/workflows/labeler.yml",
        ".github/workflows/org-conformance.yml",
        ".github/workflows/release-on-tag.yml",
        ".github/workflows/release-tag.yml",
        ".github/workflows/static-files.yml",
        ".github/workflows/build-and-deploy.yml",
    }
)
SKIP_PREFIXES = (
    ".github/ISSUE_TEMPLATE/",
    ".github/DISCUSSIONS/",
    ".agents/",
    ".claude/",
    ".vscode/",
    "bruno/",
    "docs/",
)


def is_skippable(path: str) -> bool:
    return path in SKIP_FILES or path.endswith(SKIP_SUFFIXES) or path.startswith(SKIP_PREFIXES)


def classify(paths: list[str]) -> tuple[bool, list[str]]:
    """Return (whether the suite applies, the paths that made it apply)."""
    if not paths:
        return True, []
    offending = [p for p in paths if not is_skippable(p)]
    return bool(offending), offending


def main() -> None:
    paths = [p for p in sys.stdin.buffer.read().decode("utf-8", "surrogateescape").split("\0") if p]
    applicable, offending = classify(paths)
    if applicable:
        print(f"pytest_route: full run ({'; '.join(offending[:5]) or 'no changed files reported'})", file=sys.stderr)
    print(f"applicable={str(applicable).lower()}")


if __name__ == "__main__":
    main()
