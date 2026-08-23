from rest_framework import status

from hear.model.playlist.children.criteria.genre.GenrePlaylist import GenrePlaylist
from hear.model.uploaded_track.UploadedTrack import UploadedTrack
from hear.model.uploaded_track.UploadedTrackFieldKey import UploadedTrackFieldKey as UploadedTrackFields
from hear.serializer.model.uploaded_track.input.UploadedTrackInputFieldKey import UploadedTrackInputFieldKey
from hear.test.tests.integration.uploaded_track.UploadedTrackTestCase import UploadedTrackTestCase
from hear.test.utils.field.body_data.method.PutBodyDataTestCase import PutBodyDataTestCase


class TestCase(UploadedTrackTestCase, PutBodyDataTestCase):
    def test_not_provided_then_unchanged(self):
        rap_criteria = self.model_fixture_factory.create_genre(name="Rap")
        uploaded_track = self.model_fixture_factory.create_uploaded_track_with_file(
            **{UploadedTrackInputFieldKey.TITLE.value: "Love", UploadedTrackInputFieldKey.GENRE.value: rap_criteria}
        )

        response = self._put_uploaded_track(uploaded_track.uuid, **{UploadedTrackInputFieldKey.TITLE.value: "koko"})

        assert response.status_code == status.HTTP_200_OK
        updated_uploaded_track = UploadedTrack.objects.get(uuid=uploaded_track.uuid)
        assert updated_uploaded_track.genre == rap_criteria

    def test_ok_when_updating_to_not_none(self):
        rap_criteria = self.model_fixture_factory.create_genre(name="Rap")
        uploaded_track = self.model_fixture_factory.create_uploaded_track_with_file(
            title="hoyo", use_manager_for_genre_playlist_adding=True, genre=rap_criteria
        )
        rock_criteria = self.model_fixture_factory.create_genre(name="Rock")

        response = self._put_uploaded_track(
            uuid=uploaded_track.uuid, **{UploadedTrackInputFieldKey.GENRE.value: rock_criteria.name}
        )

        assert response.status_code == status.HTTP_200_OK
        assert self.saved_object.genre == rock_criteria

    def test_empty_then_none(self):
        rap_criteria = self.model_fixture_factory.create_genre(name="Rap")
        uploaded_track = self.model_fixture_factory.create_uploaded_track_with_file(
            title="wech", genre=rap_criteria, use_manager_for_genre_playlist_adding=True
        )

        response = self._put_uploaded_track(uuid=uploaded_track.uuid, **{UploadedTrackInputFieldKey.GENRE.value: ""})

        assert response.status_code == status.HTTP_200_OK
        assert self.saved_object.genre == None

    def test_empty_then_removed_from_genre_playlists_and_added_to_genreless_playlist(self):
        rock_criteria = self.model_fixture_factory.create_genre(name="Rock")
        punk_criteria = self.model_fixture_factory.create_genre(name="Punk", parent=rock_criteria)
        uploaded_track = self.model_fixture_factory.create_uploaded_track_with_file(
            title="wech", genre=punk_criteria, use_manager_for_genre_playlist_adding=True
        )

        response = self._put_uploaded_track(uuid=uploaded_track.uuid, **{UploadedTrackInputFieldKey.GENRE.value: ""})

        assert response.status_code == status.HTTP_200_OK
        assert self.saved_object.genre == None

        rock_tracks_dict_by_position = rock_criteria.criteria_playlist.tracks_not_archived_dict_by_position
        assert uploaded_track.uuid not in [track.uuid for track in rock_tracks_dict_by_position.values()]

        punk_tracks_dict_by_position = punk_criteria.criteria_playlist.tracks_not_archived_dict_by_position
        assert uploaded_track.uuid not in [track.uuid for track in punk_tracks_dict_by_position.values()]

        genreless_playlist = GenrePlaylist.objects.get(user=self.test_user1, criteria=None)
        genreless_tracks_dict_by_position = genreless_playlist.tracks_not_archived_dict_by_position
        assert len(genreless_tracks_dict_by_position) == 1
        assert genreless_tracks_dict_by_position[1].uuid == uploaded_track.uuid

    def test_provided_then_update(self):
        genre_name = "rap"
        uploaded_track = self.model_fixture_factory.create_uploaded_track_with_file(title="lolo")

        response = self._put_uploaded_track(uploaded_track.uuid, **{UploadedTrackInputFieldKey.GENRE.value: genre_name})

        assert response.status_code == status.HTTP_200_OK
        assert self.saved_object.genre
        assert self.saved_object.genre.name == genre_name
