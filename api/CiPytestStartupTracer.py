import os
import sys
from collections.abc import Callable

from django.apps import AppConfig


class CiPytestStartupTracer:
    """Logs each AppConfig.ready() in CI/pytest so hangs after model import are attributable to a specific app."""

    @staticmethod
    def is_ci_or_pytest_argv() -> bool:
        if os.environ.get("ENV") == "ci_test":
            return True
        if "pytest" in (sys.argv[0] or ""):
            return True
        return any(a == "pytest" for a in sys.argv)

    @staticmethod
    def install_appconfig_ready_tracer() -> None:
        if not CiPytestStartupTracer.is_ci_or_pytest_argv():
            return
        original_ready: Callable[[AppConfig], None] = AppConfig.ready

        def traced_ready(self: AppConfig) -> None:
            print(f"[Django] AppConfig.ready() start: {self.label}", flush=True)
            original_ready(self)
            print(f"[Django] AppConfig.ready() end: {self.label}", flush=True)

        AppConfig.ready = traced_ready  # type: ignore[method-assign]
