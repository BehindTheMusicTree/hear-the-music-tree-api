import json
from unittest.mock import MagicMock

from django.test import TestCase
from rest_framework import status
from rest_framework.exceptions import PermissionDenied

from api.view.error.ApiErrorCode import ApiErrorCodeNumeric
from api.view.error.exception_handler import _handle_exception_with_request


class TestExceptionHandlerPermissionDenied(TestCase):
    def test_permission_denied_with_unauthenticated_request_then_401_auth_not_authenticated(self):
        exc = PermissionDenied()
        request = MagicMock()
        request.user.is_authenticated = False
        context = {'request': request}

        response = _handle_exception_with_request(exc, context)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        data = json.loads(response.content)
        assert data['code'] == ApiErrorCodeNumeric.AUTH_NOT_AUTHENTICATED
        assert data['details']['code'] == 'authentication_required'
        assert data['details']['message'] == 'Authentication required'
        assert data['success'] is False

    def test_permission_denied_with_authenticated_request_then_403_forbidden(self):
        exc = PermissionDenied()
        request = MagicMock()
        request.user.is_authenticated = True
        context = {'request': request}

        response = _handle_exception_with_request(exc, context)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        data = json.loads(response.content)
        assert data['code'] == ApiErrorCodeNumeric.AUTH_INSUFFICIENT_PERMISSIONS
        assert data['success'] is False

    def test_permission_denied_with_no_request_in_context_then_401_unauthorized(self):
        exc = PermissionDenied()
        context = {}

        response = _handle_exception_with_request(exc, context)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        data = json.loads(response.content)
        assert data['code'] == ApiErrorCodeNumeric.AUTH_NOT_AUTHENTICATED
        assert data['success'] is False

    def test_permission_denied_with_none_context_then_401_unauthorized(self):
        exc = PermissionDenied()

        response = _handle_exception_with_request(exc, None)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        data = json.loads(response.content)
        assert data['code'] == ApiErrorCodeNumeric.AUTH_NOT_AUTHENTICATED
        assert data['success'] is False
