from unittest.mock import patch

from django.db import IntegrityError
from django.test import override_settings
from rest_framework import status
from the_music_tree_api_kit.view.error.ApiErrorCode import ApiErrorCodeNumeric

from hear.test.tests.integration.uploaded_track.UploadedTrackTestCase import UploadedTrackTestCase
from hear.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename


class TestCase(UploadedTrackTestCase):
    @override_settings(DEBUG=False)
    def test_internal_error_then_500_with_response_error_code(self):
        with patch("hear.model.uploaded_track.UploadedTrack.UploadedTrack.save") as mock:
            exception_message = "DB Integrity Error"
            mock.side_effect = IntegrityError(exception_message)

            results = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_NONE_MP3, title="test")
            assert results.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
            json = results.json()
            assert json["code"] == ApiErrorCodeNumeric.SYSTEM_INTERNAL_ERROR
