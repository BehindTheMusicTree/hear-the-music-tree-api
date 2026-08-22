"""Parent conftest for the hear/test tree (loaded before hear/test/tests/conftest.py).

Pytest loads initial conftests after pytest-django’s ``pytest_load_initial_conftests`` runs
``django.setup()`` (see pytest hook order: django plugin runs before core ``Config`` trylast
that imports conftest files). This module therefore usually prints *after* the
``[Django] apps.populate() finished`` lines — if it never appears, the stall is between
``django.setup()`` returning and conftest import (another ``pytest_load_initial_conftests``
implementation or conftest discovery).
"""

from __future__ import annotations

import sys

from hear.CiStartupTraceEnabled import CiStartupTraceEnabled


def _pytest_parent_progress(msg: str) -> None:
    if not CiStartupTraceEnabled.is_tracer_active():
        return
    print(f"[pytest] {msg}", flush=True)


_pytest_parent_progress(
    "hear/test/conftest.py: imported (parent; pytest-django has typically already run django.setup())"
)
