"""
It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "api.settings")

from api.otel_bootstrap import setup_otel

setup_otel()

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
