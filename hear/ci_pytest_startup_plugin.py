"""Pytest plugin: brackets ``pytest_load_initial_conftests`` (load via ``pytest.ini`` ``addopts`` or
``PYTEST_PLUGINS``).

Conftest files cannot implement this hook. CI sets ``PYTEST_PLUGINS`` and ``CI_STARTUP_TRACE`` in the workflow
so diagnostics work when the workspace is bind-mounted over the image project dir.
"""

from __future__ import annotations

import sys
from collections.abc import Generator

import pytest

from hear.CiStartupTraceEnabled import CiStartupTraceEnabled


def _startup_line(msg: str) -> None:
    if not CiStartupTraceEnabled.is_enabled():
        return
    line = f"[pytest] ci_pytest_startup_plugin: {msg}"
    print(line, flush=True)
    print(line, file=sys.stderr, flush=True)


_startup_line("module loaded (-p / PYTEST_PLUGINS; CI_STARTUP_TRACE=1 enables these lines)")


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
