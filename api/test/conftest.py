"""Parent conftest for the api/test tree (loaded before api/test/tests/conftest.py).

Pytest loads initial conftests after pytest-django’s ``pytest_load_initial_conftests`` runs
``django.setup()`` (see pytest hook order: django plugin runs before core ``Config`` trylast
that imports conftest files). This module therefore usually prints *after* the
``[Django] apps.populate() finished`` lines — if it never appears, the stall is between
``django.setup()`` returning and conftest import (another ``pytest_load_initial_conftests``
implementation or conftest discovery).
"""

from __future__ import annotations

import sys
import traceback

from api.CiStartupTraceEnabled import CiStartupTraceEnabled


def _pytest_parent_progress(msg: str) -> None:
    if not CiStartupTraceEnabled.is_tracer_active():
        return
    print(f"[pytest] {msg}", flush=True)


_pytest_parent_progress(
    "api/test/conftest.py: imported (parent; pytest-django has typically already run django.setup())"
)


def _install_unhandled_exception_tracer() -> None:
    """TEMPORARY diagnostic: log the real traceback behind ErrorResponse's swallowed 500s.

    ErrorResponse.handle_exception falls through to a generic {"internal_error"} JSON response
    with no logging, so CI's pytest output otherwise gives no clue what raised. Gated on the
    same CI_STARTUP_TRACE flag CI already sets, so this is a no-op locally unless opted in.
    To be reverted once sub-step 6f's failing test is root-caused.
    """
    if not CiStartupTraceEnabled.is_tracer_active():
        return
    from the_music_tree_api_kit.view.error.ErrorResponse import ErrorResponse

    original_handle_exception = ErrorResponse.handle_exception.__func__

    def _traced_handle_exception(cls, exc):
        print("[pytest] ErrorResponse.handle_exception: unhandled exception traceback follows:", flush=True)
        traceback.print_exception(type(exc), exc, exc.__traceback__)
        return original_handle_exception(cls, exc)

    ErrorResponse.handle_exception = classmethod(_traced_handle_exception)


_install_unhandled_exception_tracer()
