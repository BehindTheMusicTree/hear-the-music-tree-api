"""
It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "api.settings")

from api.otel_bootstrap import setup_otel

setup_otel()

from django.core.asgi import get_asgi_application

application = get_asgi_application()
