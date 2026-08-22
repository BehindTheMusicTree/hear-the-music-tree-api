#!/usr/bin/env python3
"""Fail if Python files define string enums with ``class X(str, Enum)`` instead of ``StrEnum``.

Primary enforcement in this repo is Ruff **UP042** (``replace-str-enum``) via ``ruff check`` / pre-commit.
This script is an optional duplicate check for the same pattern.

Policy: https://github.com/BehindTheMusicTree/python-project-standards/blob/main/docs/development.md
(string enums: https://github.com/BehindTheMusicTree/python-project-standards/blob/main/docs/string-enums.md).
"""

from __future__ import annotations

import ast
import sys
from pathlib import Path


def _is_str_base(node: ast.expr) -> bool:
    return isinstance(node, ast.Name) and node.id == "str"


def _is_enum_base(node: ast.expr) -> bool:
    if isinstance(node, ast.Name) and node.id == "Enum":
        return True
    return isinstance(node, ast.Attribute) and node.attr == "Enum"


def _uses_str_enum_mixin(classdef: ast.ClassDef) -> bool:
    if len(classdef.bases) != 2:
        return False
    a, b = classdef.bases
    return (_is_str_base(a) and _is_enum_base(b)) or (_is_enum_base(a) and _is_str_base(b))


def _scan_file(path: Path) -> list[tuple[int, str]]:
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except SyntaxError as e:
        return [(e.lineno or 1, f"syntax error while scanning: {e}")]
    violations: list[tuple[int, str]] = []
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and _uses_str_enum_mixin(node):
            violations.append(
                (
                    node.lineno,
                    f"{path}: use `class {node.name}(StrEnum):` and `from enum import StrEnum` "
                    "instead of `(str, Enum)` (see DEVELOPMENT.md)",
                )
            )
    return violations


def _default_roots(repo_root: Path) -> list[Path]:
    return [repo_root / "hear"]


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    paths: list[Path]
    if len(sys.argv) > 1:
        paths = [Path(p).resolve() for p in sys.argv[1:] if p.endswith(".py")]
    else:
        paths = sorted(
            p
            for root in _default_roots(repo_root)
            if root.is_dir()
            for p in root.rglob("*.py")
            if "migrations" not in p.parts
        )

    all_violations: list[str] = []
    for path in paths:
        if not path.is_file():
            continue
        for _line, message in _scan_file(path):
            all_violations.append(message)

    if not all_violations:
        return 0

    for message in sorted(all_violations):
        print(message, file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
