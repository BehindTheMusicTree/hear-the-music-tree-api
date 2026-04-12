from unittest.mock import patch

import pytest
from rest_framework import status

from api.test.tests.integration.uploaded_track.UploadedTrackTestCase import UploadedTrackTestCase
from api.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename


@pytest.mark.patches_musicbrainz_lookup
class TestCase(UploadedTrackTestCase):
    @patch("api.utils.musicbrainz.service.acoustid.lookup")
    def test_totaleclipe_5m35_flac_then_ok(self, mock_lookup):
        mock_lookup.return_value = {
            "status": "ok",
            "results": [
                {
                    "score": 1.0,
                    "recordings": [
                        {
                            "id": "0383dadf-2a4e-4d10-a46a-e9e041da8eb3",
                            "title": "Total Eclipse of the Heart",
                            "artists": [{"id": "0383dadf-2a4e-4d10-a46a-e9e041da8eb3", "name": "Bonnie Tyler"}],
                            "duration": 335,
                        }
                    ],
                }
            ],
        }
        response = self._post_uploaded_track(UploadedTrackTestFilename.RECORDING_TOTAL_ECLIPSE_5M35_FLAC)

        assert response.status_code == status.HTTP_201_CREATED
        if self.saved_object.track_file.musicbrainz_recording_missing_cause:
            print(self.saved_object.track_file.musicbrainz_recording_missing_cause)
            raise AssertionError

        assert self.saved_object.track_file.musicbrainz_recording
        assert self.saved_object.track_file.musicbrainz_recording.title == "Total Eclipse of the Heart"
