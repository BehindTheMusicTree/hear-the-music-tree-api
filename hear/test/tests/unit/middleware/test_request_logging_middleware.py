from unittest.mock import Mock

from django.http import HttpRequest

from hear.middleware.RequestLoggingMiddleware import RequestLoggingMiddleware


class TestRequestLoggingMiddleware:
    def test_multipart_post_then_passes_through_without_reading_body(self):
        """Multipart request must not read request.body (stream already consumed by POST/FILES)."""
        mock_response = Mock()
        mock_response.status_code = 200

        def mock_get_response(req):
            return mock_response

        middleware = RequestLoggingMiddleware(get_response=mock_get_response)

        request = HttpRequest()
        request.method = "POST"
        request.path = "/me/library/uploaded/"
        request.META = {"REMOTE_ADDR": "127.0.0.1"}
        request.content_type = "multipart/form-data; boundary=----boundary"
        request.headers = {}

        response = middleware.__call__(request)

        assert response == mock_response
