import pytest
from rest_framework import status

from api.model.criteria.children.genre.Genre import Genre
from api.model.playlist.children.criteria.CriteriaPlaylist import CriteriaPlaylist
from api.serializer.model.criteria.input.post import Fields as PostFields
from api.serializer.model.uploaded_track.input.put.Fields import Fields as PutFields
from api.test.utils.AppTestCase import AppTestCase
from api.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename


@pytest.mark.e2e
class TestCase(AppTestCase):
    """
    E2E test for complete genre hierarchy creation and automatic playlist generation.

    This test verifies the complete workflow:
    1. User authenticates
    2. User creates parent genre "Electronic Music"
    3. User creates child genre "Techno" with parent "Electronic Music"
    4. User creates grandchild genre "Minimal Techno" with parent "Techno"
    5. User uploads a track and tags it with "Minimal Techno"
    6. System automatically creates playlists for all three genres
    7. Track appears in all three playlists (Minimal Techno, Techno, Electronic Music)
    """

    def test_create_genre_hierarchy_and_automatic_playlists_then_ok(self):
        from api.test.tests.integration.criteria.GenreTestCase import GenreTestCase
        from api.test.tests.integration.uploaded_track.UploadedTrackTestCase import UploadedTrackTestCase

        genre_test_case = self._domain_helper(GenreTestCase)
        uploaded_track_test_case = self._domain_helper(UploadedTrackTestCase)

        parent_genre_name = "Electronic Music"
        child_genre_name = "Techno"
        grandchild_genre_name = "Minimal Techno"

        response = genre_test_case._post_genre(**{PostFields.NAME_PUBLIC: parent_genre_name})
        assert response.status_code == status.HTTP_201_CREATED
        parent_genre = genre_test_case.saved_object
        assert parent_genre.name == parent_genre_name
        assert parent_genre.parent is None

        response = genre_test_case._post_genre(
            **{PostFields.NAME_PUBLIC: child_genre_name, PostFields.PARENT: parent_genre.uuid})
        assert response.status_code == status.HTTP_201_CREATED
        child_genre = genre_test_case.saved_object
        assert child_genre.name == child_genre_name
        assert child_genre.parent == parent_genre

        response = genre_test_case._post_genre(**{PostFields.NAME_PUBLIC: grandchild_genre_name,
                                                  PostFields.PARENT: child_genre.uuid})
        assert response.status_code == status.HTTP_201_CREATED
        grandchild_genre = genre_test_case.saved_object
        assert grandchild_genre.name == grandchild_genre_name
        assert grandchild_genre.parent == child_genre

        genres = Genre.objects.filter(user=self.test_user1)
        assert genres.count() == 3
        assert genres.filter(name=parent_genre_name).exists()
        assert genres.filter(name=child_genre_name).exists()
        assert genres.filter(name=grandchild_genre_name).exists()

        parent_genre_playlist = CriteriaPlaylist.objects.get(
            user=self.test_user1, criteria__name=parent_genre_name)
        child_genre_playlist = CriteriaPlaylist.objects.get(
            user=self.test_user1, criteria__name=child_genre_name)
        grandchild_genre_playlist = CriteriaPlaylist.objects.get(
            user=self.test_user1, criteria__name=grandchild_genre_name)

        assert parent_genre_playlist is not None
        assert child_genre_playlist is not None
        assert grandchild_genre_playlist is not None

        response = uploaded_track_test_case._post_uploaded_track(
            UploadedTrackTestFilename.DEFAULT_MP3, title="Test Track")
        assert response.status_code == status.HTTP_201_CREATED
        track = uploaded_track_test_case.saved_object

        response = uploaded_track_test_case._put_uploaded_track(track.uuid, **{PutFields.GENRE: grandchild_genre_name})
        assert response.status_code == status.HTTP_200_OK

        track.refresh_from_db()
        assert track.genre == grandchild_genre

        track_playlists_uuids = [playlist.uuid for playlist in track.playlists.all()]
        assert len(track_playlists_uuids) == 3

        assert parent_genre_playlist.playlist.uuid in track_playlists_uuids
        assert child_genre_playlist.playlist.uuid in track_playlists_uuids
        assert grandchild_genre_playlist.playlist.uuid in track_playlists_uuids

        parent_playlist_tracks = parent_genre_playlist.playlist.uploaded_tracks.filter(user=self.test_user1)
        child_playlist_tracks = child_genre_playlist.playlist.uploaded_tracks.filter(user=self.test_user1)
        grandchild_playlist_tracks = grandchild_genre_playlist.playlist.uploaded_tracks.filter(user=self.test_user1)

        assert track in parent_playlist_tracks
        assert track in child_playlist_tracks
        assert track in grandchild_playlist_tracks
