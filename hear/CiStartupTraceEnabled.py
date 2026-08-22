import os
import sys


class CiStartupTraceEnabled:
    """Gates verbose Django/pytest startup diagnostics behind ``CI_STARTUP_TRACE`` (1/true/yes)."""

    @staticmethod
    def is_enabled() -> bool:
        return os.environ.get("CI_STARTUP_TRACE", "").strip().lower() in ("1", "true", "yes")

    @staticmethod
    def is_pytest_or_ci_test_argv() -> bool:
        if os.environ.get("ENV") == "ci_test":
            return True
        if "pytest" in (sys.argv[0] or ""):
            return True
        return any(a == "pytest" for a in sys.argv)

    @staticmethod
    def is_tracer_active() -> bool:
        return CiStartupTraceEnabled.is_enabled() and CiStartupTraceEnabled.is_pytest_or_ci_test_argv()
