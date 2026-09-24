from rest_framework import status

from hear.model.playlist.children.criteria.CriteriaPlaylist import CriteriaPlaylist
from hear.model.uploaded_track.UploadedTrackFieldKey import UploadedTrackFieldKey as UploadedTrackFields
from hear.serializer.model.uploaded_track.input.UploadedTrackInputFieldKey import UploadedTrackInputFieldKey
from hear.test.tests.integration.uploaded_track.UploadedTrackTestCase import UploadedTrackTestCase


class TestCase(UploadedTrackTestCase):
    def test_new_criteria_then_not_in_old_criteria_playlist_anymore(self):
        old_genre = self.model_fixture_factory.create_genre(name="Metal")
        data = {UploadedTrackInputFieldKey.TITLE.value: "Love", UploadedTrackInputFieldKey.GENRE.value: old_genre}
        uploaded_track = self.model_fixture_factory.create_uploaded_track_with_file(
            use_manager_for_genre_playlist_adding=True, **data
        )
        assert uploaded_track.uuid in old_genre.criteria_playlist.tracks.values_list("uuid", flat=True)

        new_genre_name = "Rock"
        response = self._put_uploaded_track(
            uploaded_track.uuid, **{UploadedTrackInputFieldKey.GENRE.value: new_genre_name}
        )

        assert response.status_code == status.HTTP_200_OK
        old_genre_playlist: CriteriaPlaylist = CriteriaPlaylist.objects.get(criteria=old_genre)
        assert uploaded_track.uuid not in old_genre_playlist.tracks.values_list("uuid", flat=True)
