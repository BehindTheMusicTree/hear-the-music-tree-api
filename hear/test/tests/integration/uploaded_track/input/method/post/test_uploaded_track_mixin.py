from typing import cast

from rest_framework import status

from hear.model.uploaded_track.UploadedTrack import UploadedTrack
from hear.serializer.model.uploaded_track.input.UploadedTrackInputFieldKey import UploadedTrackInputFieldKey
from hear.test.tests.integration.uploaded_track.UploadedTrackTestCase import UploadedTrackTestCase
from hear.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename


class TestCase(UploadedTrackTestCase):
    def test_create_then_in_uploaded_track_mixin(self):
        title = "test"
        response = self._post_uploaded_track(
            UploadedTrackTestFilename.METADATA_NONE_MP3, **{UploadedTrackInputFieldKey.TITLE.value: title}
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert self.test_user1.all_uploaded_tracks_mixin.uploaded_tracks.count() == 1
        uploaded_track = cast(
            UploadedTrack | None, self.test_user1.all_uploaded_tracks_mixin.uploaded_tracks_not_archived.first()
        )
        assert uploaded_track
        assert uploaded_track.title == title
