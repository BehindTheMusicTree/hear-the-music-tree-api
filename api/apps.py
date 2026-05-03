from django.apps import AppConfig

from api.CiStartupTraceEnabled import CiStartupTraceEnabled


class ApiConfig(AppConfig):
    name = "api"

    def ready(self) -> None:
        if CiStartupTraceEnabled.is_tracer_active():
            print(
                "[Django] ApiConfig.ready() - django.setup() finished loading the api app.",
                flush=True,
            )
