from rest_framework import status

from hear.model.artist.Artist import Artist
from hear.serializer.model.uploaded_track.input.UploadedTrackInputFieldKey import UploadedTrackInputFieldKey
from hear.test.tests.integration.uploaded_track.UploadedTrackTestCase import UploadedTrackTestCase
from hear.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename


class TestCase(UploadedTrackTestCase):
    def test_value_then_ok(self) -> None:
        value = "rovk"
        response = self._post_uploaded_track(
            UploadedTrackTestFilename.METADATA_NONE_MP3,
            **{UploadedTrackInputFieldKey.ARTISTS_NAMES_MULTIPART.value: [value]},
        )

        assert response.status_code == status.HTTP_201_CREATED
        artists_list: list[Artist] = list(self.saved_object.artists.all())
        assert len(artists_list) > 0
        assert artists_list[0].name == value

    def test_empty_then_none(self) -> None:
        response = self._post_uploaded_track(
            UploadedTrackTestFilename.RATING_ID3V2_1_STAR_MP3,
            **{UploadedTrackInputFieldKey.ARTISTS_NAMES_MULTIPART.value: []},
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.artists.count() == 0
