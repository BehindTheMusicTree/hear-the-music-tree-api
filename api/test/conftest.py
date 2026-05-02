"""Parent conftest for the api/test tree (loaded before api/test/tests/conftest.py).

Pytest loads initial conftests after pytest-django’s ``pytest_load_initial_conftests`` runs
``django.setup()`` (see pytest hook order: django plugin runs before core ``Config`` trylast
that imports conftest files). This module therefore usually prints *after* the
``[Django] apps.populate() finished`` lines — if it never appears, the stall is between
``django.setup()`` returning and conftest import (another ``pytest_load_initial_conftests``
implementation or conftest discovery).
"""

from __future__ import annotations

import os
import sys


def _pytest_parent_progress(msg: str) -> None:
    if os.environ.get("ENV") == "ci_test":
        print(f"[pytest] {msg}", flush=True)
        return
    if "pytest" in (sys.argv[0] or ""):
        print(f"[pytest] {msg}", flush=True)
        return
    if any(a == "pytest" for a in sys.argv):
        print(f"[pytest] {msg}", flush=True)


_pytest_parent_progress(
    "api/test/conftest.py: imported (parent; pytest-django has typically already run django.setup())"
)
