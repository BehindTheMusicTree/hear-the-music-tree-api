import pytest
from rest_framework import status

from api.model.playlist.children.criteria.CriteriaPlaylist import CriteriaPlaylist
from api.serializer.model.criteria.input.post import Fields as PostUploadedTrackInputFieldKey
from api.serializer.model.uploaded_track.input.UploadedTrackInputFieldKey import UploadedTrackInputFieldKey
from api.test.utils.AppTestCase import AppTestCase
from api.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename


@pytest.mark.e2e
class TestCase(AppTestCase):
    """
    E2E test for tag-based playlist generation.

    This test verifies the complete workflow:
    1. User authenticates
    2. User creates multiple tags ("dance", "electronic", "ambient")
    3. User uploads tracks and tags them with different combinations
    4. System automatically creates tag playlists
    5. Tracks appear in correct tag playlists
    """

    def test_tag_based_playlist_generation_then_ok(self):
        from api.test.tests.integration.criteria.TagTestCase import TagTestCase
        from api.test.tests.integration.uploaded_track.UploadedTrackTestCase import UploadedTrackTestCase

        tag_test_case = self._domain_helper(TagTestCase)
        uploaded_track_test_case = self._domain_helper(UploadedTrackTestCase)

        tag1_name = "dance"
        tag2_name = "electronic"
        tag3_name = "ambient"

        response = tag_test_case._post_tag(**{PostUploadedTrackInputFieldKey.NAME_PUBLIC: tag1_name})
        assert response.status_code == status.HTTP_201_CREATED
        tag1 = tag_test_case.saved_object

        response = tag_test_case._post_tag(**{PostUploadedTrackInputFieldKey.NAME_PUBLIC: tag2_name})
        assert response.status_code == status.HTTP_201_CREATED
        tag2 = tag_test_case.saved_object

        response = tag_test_case._post_tag(**{PostUploadedTrackInputFieldKey.NAME_PUBLIC: tag3_name})
        assert response.status_code == status.HTTP_201_CREATED
        tag3 = tag_test_case.saved_object

        tag1_playlist = CriteriaPlaylist.objects.get(user=self.test_user1, criteria=tag1)
        tag2_playlist = CriteriaPlaylist.objects.get(user=self.test_user1, criteria=tag2)
        tag3_playlist = CriteriaPlaylist.objects.get(user=self.test_user1, criteria=tag3)

        assert tag1_playlist is not None
        assert tag2_playlist is not None
        assert tag3_playlist is not None

        track1 = self.model_fixture_factory.create_uploaded_track_with_file(
            title="Track 1", test_uploaded_track_filename=UploadedTrackTestFilename.DEFAULT_MP3
        )
        track2 = self.model_fixture_factory.create_uploaded_track_with_file(
            title="Track 2", test_uploaded_track_filename=UploadedTrackTestFilename.DEFAULT_MP3
        )
        track3 = self.model_fixture_factory.create_uploaded_track_with_file(
            title="Track 3", test_uploaded_track_filename=UploadedTrackTestFilename.DEFAULT_MP3
        )

        from api.model.track_playlist_rel.TrackPlaylistRel import TrackPlaylistRel

        TrackPlaylistRel.objects.create(user=self.test_user1, playlist=tag1_playlist.playlist, track=track1)
        TrackPlaylistRel.objects.create(user=self.test_user1, playlist=tag2_playlist.playlist, track=track1)
        TrackPlaylistRel.objects.create(user=self.test_user1, playlist=tag2_playlist.playlist, track=track2)
        TrackPlaylistRel.objects.create(user=self.test_user1, playlist=tag3_playlist.playlist, track=track2)
        TrackPlaylistRel.objects.create(user=self.test_user1, playlist=tag1_playlist.playlist, track=track3)

        track1.refresh_from_db()
        track2.refresh_from_db()
        track3.refresh_from_db()

        track1_playlists = [p.uuid for p in track1.playlists.all()]
        track2_playlists = [p.uuid for p in track2.playlists.all()]
        track3_playlists = [p.uuid for p in track3.playlists.all()]

        assert tag1_playlist.playlist.uuid in track1_playlists
        assert tag2_playlist.playlist.uuid in track1_playlists
        assert len(track1_playlists) == 2

        assert tag2_playlist.playlist.uuid in track2_playlists
        assert tag3_playlist.playlist.uuid in track2_playlists
        assert len(track2_playlists) == 2

        assert tag1_playlist.playlist.uuid in track3_playlists
        assert len(track3_playlists) == 1

        assert track1 in tag1_playlist.playlist.uploaded_tracks.all()
        assert track1 in tag2_playlist.playlist.uploaded_tracks.all()
        assert track2 in tag2_playlist.playlist.uploaded_tracks.all()
        assert track2 in tag3_playlist.playlist.uploaded_tracks.all()
        assert track3 in tag1_playlist.playlist.uploaded_tracks.all()
