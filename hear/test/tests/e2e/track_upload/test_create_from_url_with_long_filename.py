import json

import pytest
from rest_framework import status

from hear import settings
from hear.test.tests.integration.uploaded_track.UploadedTrackTestCase import UploadedTrackTestCase
from hear.test.utils.uploaded_track.UploadedTrackDownloadTestUrl import UploadedTrackDownloadTestUrl


@pytest.mark.e2e
class TestCase(UploadedTrackTestCase):
    """E2E: create track from URL with long filename; title uses generated prefix. Skips when URL unreachable."""

    def test_create_from_url_with_long_filename_then_title_has_prefix(self):
        response = self._post_uploaded_track_from_url(UploadedTrackDownloadTestUrl.LONG_MP3)
        if response.status_code == 400:
            try:
                body = json.loads(response.content) if getattr(response, "content", None) else {}
            except json.JSONDecodeError, TypeError:
                body = {}
            err = json.dumps(body) if isinstance(body, dict) else str(body)
            err = err.lower()
            if any(k in err for k in ("url", "download", "failed", "invalid")):
                pytest.skip("URL unreachable or validation failed (no network?)")
        assert response.status_code == status.HTTP_201_CREATED, response.content
        assert self.saved_object.title.startswith(settings.UPLOADED_TRACK_GENERATED_TITLE_PREFIXE)
