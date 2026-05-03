"""Pytest plugin: brackets ``pytest_load_initial_conftests`` (loaded via ``pytest.ini`` ``-p
api.ci_pytest_startup_plugin``).

Conftest files cannot implement this hook. CI bind-mounts the workspace over the image project dir, so
setuptools ``pytest11`` entry points from the build layer are unreliable; ``-p`` imports this module by path.
"""

from __future__ import annotations

import sys
from collections.abc import Generator

import pytest


def _startup_line(msg: str) -> None:
    line = f"[pytest] ci_pytest_startup_plugin: {msg}"
    print(line, flush=True)
    print(line, file=sys.stderr, flush=True)


_startup_line("module loaded (-p api.ci_pytest_startup_plugin from pytest.ini)")


@pytest.hookimpl(wrapper=True, tryfirst=True)
def pytest_load_initial_conftests(
    early_config: pytest.Config,
    parser: pytest.Parser,
    args: list[str],
) -> Generator[None]:
    del early_config, parser, args
    _startup_line(
        "pytest_load_initial_conftests outer enter (inner: capture, pytest-django django.setup, core conftest load, …)"
    )
    yield
    _startup_line("pytest_load_initial_conftests outer leave (initial conftest phase done for this hook)")
