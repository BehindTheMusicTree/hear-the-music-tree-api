# api/health.py
"""
Health check endpoint pour monitoring et orchestration Docker
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.db import connection
from django.conf import settings
from django.core.cache import cache
import time

# Track application start time
START_TIME = time.time()


class HealthCheckView(APIView):
    """
    Health check endpoint accessible sans authentification
    Utilisé par Docker, Kubernetes, et les load balancers
    """
    permission_classes = [AllowAny]
    authentication_classes = []  # Désactive complètement l'auth

    def get(self, request):
        """
        GET /health/

        Returns:
            200 OK si tous les checks passent
            503 Service Unavailable si un check critique échoue
        """
        health_status = {
            "status": "healthy",
            "version": getattr(settings, 'APP_VERSION', 'unknown'),
            "uptime_seconds": int(time.time() - START_TIME),
            "checks": {}
        }

        # Critical check: Database
        db_healthy = self._check_database(health_status)

        # Optional check: Cache
        self._check_cache(health_status)

        # Determine overall status
        if not db_healthy:
            health_status["status"] = "unhealthy"
            return Response(
                health_status,
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        return Response(health_status, status=status.HTTP_200_OK)

    def _check_database(self, health_status):
        """
        Vérifie la connexion à la base de données

        Returns:
            bool: True si la DB est accessible
        """
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")

            health_status["checks"]["database"] = {
                "status": "ok",
                "vendor": connection.vendor
            }
            return True

        except Exception as e:
            health_status["checks"]["database"] = {
                "status": "error",
                "message": str(e)
            }
            return False

    def _check_cache(self, health_status):
        """
        Vérifie le cache (non-critique)
        """
        try:
            test_key = 'health_check_test'
            cache.set(test_key, 'ok', timeout=10)
            result = cache.get(test_key)

            health_status["checks"]["cache"] = {
                "status": "ok" if result == 'ok' else "warning"
            }

        except Exception as e:
            health_status["checks"]["cache"] = {
                "status": "warning",
                "message": str(e)
            }
