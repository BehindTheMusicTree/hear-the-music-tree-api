from collections.abc import Callable, Iterable

from django.apps import AppConfig

from hear.CiStartupTraceEnabled import CiStartupTraceEnabled

_installed: bool = False


class CiPytestStartupTracer:
    """CI/pytest-only hooks to locate stalls after settings (populate, ready(), URLconf, resolver)."""

    @staticmethod
    def install_ci_startup_tracers() -> None:
        global _installed
        if _installed or not CiStartupTraceEnabled.is_tracer_active():
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
                "[Django] django.setup() is finishing (still inside pytest_load_initial_conftests). "
                "Next: [pytest] ci_pytest_startup_plugin outer leave (if CI_STARTUP_TRACE=1 and -p / "
                "PYTEST_PLUGINS), then hear/test/conftest.py, … ROOT_URLCONF loads on first URL resolution / client.",
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
                "[Django] get_resolver() (first call imports ROOT_URLCONF, e.g. hear.urls; can be slow).",
                flush=True,
            )
            result = original_get_resolver(urlconf)
            print("[Django] get_resolver() returned.", flush=True)
            return result

        resolvers.get_resolver = traced_get_resolver  # type: ignore[method-assign]
        django_urls.get_resolver = traced_get_resolver  # type: ignore[method-assign]
