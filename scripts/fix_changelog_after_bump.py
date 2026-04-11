#!/usr/bin/env python3
"""Set release date and fix Unreleased heading indent in CHANGELOG.md after bump2version."""

from datetime import date
from pathlib import Path


CHANGELOG = Path(__file__).resolve().parent.parent / "CHANGELOG.md"


def main() -> None:
    text = CHANGELOG.read_text()
    text = text.replace("YYYY-MM-DD", str(date.today()))
    text = text.replace("    ## [Unreleased]  <!-- release -->", "## [Unreleased]  <!-- release -->")
    CHANGELOG.write_text(text)


if __name__ == "__main__":
    main()
