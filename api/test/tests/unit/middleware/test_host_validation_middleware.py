import json
from unittest.mock import Mock, patch

import pytest
from django.core.exceptions import DisallowedHost
from django.http import HttpRequest

from api.middleware.HostValidationMiddleware import HostValidationMiddleware
from api.view.error.ApiErrorCode import ApiErrorCodeNumeric


class TestHostValidationMiddleware:
    def test_disallowed_host_then_400_bad_request(self):
        """Test that requests with invalid Host headers return appropriate error response"""
        middleware = HostValidationMiddleware(get_response=Mock())

        request = HttpRequest()
        request.META["HTTP_HOST"] = "malicious.example.com"

        # Mock settings to have a specific ALLOWED_HOSTS list
        with patch("django.conf.settings") as mock_settings:
            mock_settings.ALLOWED_HOSTS = ["localhost", "example.com"]
            mock_settings.DEBUG = False

            response = middleware.__call__(request)

            assert response.status_code == 400

            response_json = json.loads(response.content)
            assert response_json["code"] == ApiErrorCodeNumeric.SECURITY_ERROR
            assert response_json["details"]["message"] == "Invalid host header"

    def test_allowed_host_then_passes(self):
        """Test that requests with allowed Host headers pass through"""
        mock_response = Mock()
        mock_response.status_code = 200

        def mock_get_response(req):
            return mock_response

        middleware = HostValidationMiddleware(get_response=mock_get_response)

        request = HttpRequest()
        request.META["HTTP_HOST"] = "localhost"

        # Mock settings to allow localhost
        with patch("django.conf.settings") as mock_settings:
            mock_settings.ALLOWED_HOSTS = ["localhost", "example.com"]

            response = middleware.__call__(request)

            assert response == mock_response
