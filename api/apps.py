import os
import sys

from django.apps import AppConfig


class ApiConfig(AppConfig):
    name = "api"

    def ready(self) -> None:
        if "pytest" in sys.argv[0] or os.environ.get("ENV") == "ci_test":
            print(
                "[Django] ApiConfig.ready() - django.setup() finished loading the api app.",
                flush=True,
            )
