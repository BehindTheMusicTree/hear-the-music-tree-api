"""Pytest plugin (pytest11): brackets the full ``pytest_load_initial_conftests`` hook chain.

Conftest files cannot implement this hook; a setuptools entry point is used so we still see
progress when another inner hook (e.g. capture) runs between ``django.setup()`` and conftest import.
"""

from __future__ import annotations

from collections.abc import Generator

import pytest


@pytest.hookimpl(wrapper=True, tryfirst=True)
def pytest_load_initial_conftests(
    early_config: pytest.Config,
    parser: pytest.Parser,
    args: list[str],
) -> Generator[None]:
    del parser, args
    print(
        "[pytest] ci_pytest_startup_plugin: pytest_load_initial_conftests outer enter "
        "(inner: capture, pytest-django django.setup, core conftest load, …)",
        flush=True,
    )
    yield
    print(
        "[pytest] ci_pytest_startup_plugin: pytest_load_initial_conftests outer leave "
        "(initial conftest import phase completed for this hook)",
        flush=True,
    )
