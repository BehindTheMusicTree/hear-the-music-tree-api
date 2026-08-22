from unittest.mock import patch

import pytest
from rest_framework import status

from hear.model.musicbrainz_resource.children.artist.MbArtist import MbArtist
from hear.test.tests.integration.uploaded_track.UploadedTrackTestCase import UploadedTrackTestCase
from hear.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename


@pytest.mark.patches_musicbrainz_lookup
class TestCase(UploadedTrackTestCase):
    def test_musicbrainz_link(self):
        with patch("hear.utils.musicbrainz.service.acoustid.lookup") as mock_lookup:
            mock_lookup.return_value = {
                "status": "ok",
                "results": [
                    {
                        "score": 1.0,
                        "recordings": [
                            {
                                "id": "some_recording_id",
                                "title": "We Are the Champions",
                                "artists": [{"id": "0383dadf-2a4e-4d10-a46a-e9e041da8eb3", "name": "Queen"}],
                                "duration": 180,
                            }
                        ],
                    }
                ],
            }
            response = self._post_uploaded_track(UploadedTrackTestFilename.RECORDING_QUEEN_WEARETHECHAMPIONS_MP3)

            assert response.status_code == status.HTTP_201_CREATED
            assert self.saved_object.track_file.musicbrainz_recording
            musicbrainz_artists: list[MbArtist] = list(
                self.saved_object.track_file.musicbrainz_recording.musicbrainz_artists.all()
            )
            assert musicbrainz_artists[0].musicbrainz_link == (
                "https://musicbrainz.org/artist/0383dadf-2a4e-4d10-a46a-e9e041da8eb3"
            )
