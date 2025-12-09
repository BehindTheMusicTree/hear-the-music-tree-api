import pytest
from rest_framework import status

from api.model.playlist.children.manual.ManualPlaylist import ManualPlaylist
from api.model.playlist.Playlist import Fields as PlaylistFields
from api.test.integration.view.playlist.children.manual.ManualPlaylistTestCase import ManualPlaylistTestCase
from api.test.utils.AppTestCase import AppTestCase
from api.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename


@pytest.mark.e2e
class TestCase(AppTestCase):
    """
    E2E test for complete manual playlist creation and track management.

    This test verifies the complete workflow:
    1. User authenticates
    2. User uploads multiple tracks
    3. User creates a manual playlist
    4. User adds tracks to playlist
    5. User retrieves playlist and verifies tracks
    6. User removes a track from playlist
    7. User updates playlist name
    8. User deletes playlist
    """

    def test_manual_playlist_creation_and_management_then_ok(self):
        from api.serializer.model.playlist.children.manual.input.Fields import Fields as ManualPlaylistFields

        manual_playlist_test_case = ManualPlaylistTestCase()
        manual_playlist_test_case.setUp()
        manual_playlist_test_case.api_client = self.api_client
        manual_playlist_test_case._login_as_test_user1()

        track1 = self.model_fixture_factory.create_uploaded_track_with_file(
            title="Track 1", test_uploaded_track_filename=UploadedTrackTestFilename.DEFAULT_MP3)
        track2 = self.model_fixture_factory.create_uploaded_track_with_file(
            title="Track 2", test_uploaded_track_filename=UploadedTrackTestFilename.DEFAULT_MP3)
        track3 = self.model_fixture_factory.create_uploaded_track_with_file(
            title="Track 3", test_uploaded_track_filename=UploadedTrackTestFilename.DEFAULT_MP3)

        playlist_name = "My Playlist"
        response = manual_playlist_test_case._post_manual_playlist(**{ManualPlaylistFields.NAME_PUBLIC: playlist_name})
        assert response.status_code == status.HTTP_201_CREATED
        playlist = manual_playlist_test_case.saved_object
        assert isinstance(playlist, ManualPlaylist)
        assert playlist.name == playlist_name

        from api.model.uploaded_track_playlist_rel.UploadedTrackPlaylistRel import UploadedTrackPlaylistRel
        from api.model.uploaded_track_playlist_rel.Fields import Fields as RelFields

        UploadedTrackPlaylistRel.objects.create(
            user=self.test_user1, playlist=playlist.playlist, uploaded_track=track1)
        UploadedTrackPlaylistRel.objects.create(
            user=self.test_user1, playlist=playlist.playlist, uploaded_track=track2)
        UploadedTrackPlaylistRel.objects.create(
            user=self.test_user1, playlist=playlist.playlist, uploaded_track=track3)

        playlist.refresh_from_db()
        playlist_tracks = playlist.uploaded_tracks.filter(user=self.test_user1)
        assert playlist_tracks.count() == 3
        assert track1 in playlist_tracks
        assert track2 in playlist_tracks
        assert track3 in playlist_tracks

        response = manual_playlist_test_case._retrieve_manual_playlist(playlist.uuid)
        assert response.status_code == status.HTTP_200_OK
        retrieved_playlist = manual_playlist_test_case.saved_object
        assert retrieved_playlist.uuid == playlist.uuid
        assert retrieved_playlist.name == playlist_name

        UploadedTrackPlaylistRel.objects.filter(
            user=self.test_user1, playlist=playlist.playlist, uploaded_track=track2).delete()

        playlist.refresh_from_db()
        playlist_tracks = playlist.uploaded_tracks.filter(user=self.test_user1)
        assert playlist_tracks.count() == 2
        assert track1 in playlist_tracks
        assert track2 not in playlist_tracks
        assert track3 in playlist_tracks

        new_playlist_name = "Updated Playlist Name"
        response = manual_playlist_test_case._put_manual_playlist(
            playlist.uuid, **{PlaylistFields.NAME_PUBLIC: new_playlist_name})
        assert response.status_code == status.HTTP_200_OK

        playlist.refresh_from_db()
        assert playlist.name == new_playlist_name

        response = manual_playlist_test_case._delete_manual_playlist(playlist.uuid)
        assert response.status_code == status.HTTP_204_NO_CONTENT

        assert not ManualPlaylist.objects.filter(uuid=playlist.uuid, user=self.test_user1).exists()
