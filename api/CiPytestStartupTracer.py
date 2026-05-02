import os
import sys
from collections.abc import Callable, Iterable

from django.apps import AppConfig

_installed: bool = False


class CiPytestStartupTracer:
    """CI/pytest-only hooks to locate stalls after settings (populate, ready(), URLconf, resolver)."""

    @staticmethod
    def is_ci_or_pytest_argv() -> bool:
        if os.environ.get("ENV") == "ci_test":
            return True
        if "pytest" in (sys.argv[0] or ""):
            return True
        return any(a == "pytest" for a in sys.argv)

    @staticmethod
    def install_ci_startup_tracers() -> None:
        global _installed
        if _installed or not CiPytestStartupTracer.is_ci_or_pytest_argv():
            return
        CiPytestStartupTracer._install_appconfig_ready_tracer()
        CiPytestStartupTracer._install_apps_populate_tracer()
        CiPytestStartupTracer._install_get_resolver_tracer()
        _installed = True

    @staticmethod
    def _install_appconfig_ready_tracer() -> None:
        original_ready: Callable[[AppConfig], None] = AppConfig.ready

        def traced_ready(self: AppConfig) -> None:
            print(f"[Django] AppConfig.ready() start: {self.label}", flush=True)
            original_ready(self)
            print(f"[Django] AppConfig.ready() end: {self.label}", flush=True)

        AppConfig.ready = traced_ready  # type: ignore[method-assign]

    @staticmethod
    def _install_apps_populate_tracer() -> None:
        from django.apps import apps

        original_populate: Callable[[Iterable[str]], None] = apps.populate

        def traced_populate(installed_apps: Iterable[str] | None = None) -> None:
            print("[Django] apps.populate() start (models, then AppConfig.ready() per app).", flush=True)
            original_populate(installed_apps)
            print("[Django] apps.populate() finished.", flush=True)
            print(
                "[Django] django.setup() is finishing; next is usually [pytest] api/test/conftest.py "
                "(initial conftest load), then tests/conftest.py, configure, sessionstart, collection. "
                "ROOT_URLCONF loads only on first URL resolution / test client.",
                flush=True,
            )

        apps.populate = traced_populate  # type: ignore[method-assign]

    @staticmethod
    def _install_get_resolver_tracer() -> None:
        import django.urls as django_urls
        from django.urls import resolvers

        original_get_resolver: Callable[..., object] = resolvers.get_resolver

        def traced_get_resolver(urlconf: str | None = None) -> object:
            print(
                "[Django] get_resolver() (first call imports ROOT_URLCONF, e.g. api.urls; can be slow).",
                flush=True,
            )
            result = original_get_resolver(urlconf)
            print("[Django] get_resolver() returned.", flush=True)
            return result

        resolvers.get_resolver = traced_get_resolver  # type: ignore[method-assign]
        django_urls.get_resolver = traced_get_resolver  # type: ignore[method-assign]
