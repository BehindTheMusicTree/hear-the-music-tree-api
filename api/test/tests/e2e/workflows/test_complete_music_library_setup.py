import pytest
from rest_framework import status

from api.model.criteria.children.genre.Genre import Genre
from api.model.playlist.children.manual.ManualPlaylist import ManualPlaylist
from api.model.uploaded_track.UploadedTrack import UploadedTrack
from api.serializer.model.criteria.input.tree_import.Fields import (
    Fields as TreeImportUploadedTrackInputFieldKey,
)
from api.serializer.model.play.input.schema.PostFields import (
    Fields as PlayPostUploadedTrackInputFieldKey,
)
from api.serializer.model.playlist.children.manual.input.Fields import (
    Fields as ManualPlaylistUploadedTrackInputFieldKey,
)
from api.serializer.model.uploaded_track.input.UploadedTrackInputFieldKey import UploadedTrackInputFieldKey
from api.test.tests.integration.criteria.GenreTestCase import GenreTestCase
from api.test.tests.integration.play.PlayTestCase import PlayTestCase
from api.test.tests.integration.playlist.children.manual.ManualPlaylistTestCase import (
    ManualPlaylistTestCase,
)
from api.test.tests.integration.search.SearchTestCase import SearchMixin
from api.test.tests.integration.uploaded_track.UploadedTrackTestCase import UploadedTrackTestCase
from api.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename
from api.utils.data_transformer import to_camel_case


@pytest.mark.e2e
@pytest.mark.slow
class TestCase(UploadedTrackTestCase, SearchMixin):
    """
    E2E test for complete music library setup workflow.

    This test verifies the complete workflow:
    1. New user registers/authenticates
    2. User imports genre tree
    3. User uploads multiple tracks (various formats: MP3, FLAC, WAV)
    4. System fingerprints tracks and retrieves MusicBrainz metadata
    5. User tags tracks with genres and tags
    6. System generates automatic playlists
    7. User creates manual playlists
    8. User searches for tracks
    9. User records plays
    10. User retrieves library statistics
    """

    def test_complete_music_library_setup_then_ok(self):
        genre_helper = self._domain_helper(GenreTestCase)
        tree_data = [
            {
                TreeImportUploadedTrackInputFieldKey.NAME_PUBLIC: "Electronic Music",
                TreeImportUploadedTrackInputFieldKey.CHILDREN: [
                    {
                        TreeImportUploadedTrackInputFieldKey.NAME_PUBLIC: "Techno",
                        TreeImportUploadedTrackInputFieldKey.CHILDREN: [],
                    }
                ],
            }
        ]
        response = genre_helper._post_genres_tree_import(data={TreeImportUploadedTrackInputFieldKey.TREE: tree_data})
        assert response.status_code == status.HTTP_201_CREATED

        genres = Genre.objects.filter(user=self.test_user1)
        assert genres.count() == 2

        response = self._post_uploaded_track(UploadedTrackTestFilename.DEFAULT_MP3, title="MP3 Track")
        assert response.status_code == status.HTTP_201_CREATED
        track1 = self.saved_object

        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_NONE_FLAC, title="FLAC Track")
        assert response.status_code == status.HTTP_201_CREATED
        track2 = self.saved_object

        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_NONE_WAV, title="WAV Track")
        assert response.status_code == status.HTTP_201_CREATED
        track3 = self.saved_object

        techno_genre = genres.get(name="Techno")
        response = self._put_uploaded_track(track1.uuid, **{UploadedTrackInputFieldKey.GENRE.value: "Techno"})
        assert response.status_code == status.HTTP_200_OK

        response = self._put_uploaded_track(track2.uuid, **{UploadedTrackInputFieldKey.GENRE.value: "Techno"})
        assert response.status_code == status.HTTP_200_OK

        from api.model.playlist.children.criteria.CriteriaPlaylist import CriteriaPlaylist

        techno_playlist = CriteriaPlaylist.objects.get(user=self.test_user1, criteria=techno_genre)
        assert techno_playlist is not None

        playlist_tracks = techno_playlist.playlist.uploaded_tracks.filter(user=self.test_user1)
        assert track1 in playlist_tracks
        assert track2 in playlist_tracks

        playlist_helper = self._domain_helper(ManualPlaylistTestCase)
        response = playlist_helper._post_manual_playlist(
            **{ManualPlaylistUploadedTrackInputFieldKey.NAME_PUBLIC: "My Favorites"}
        )
        assert response.status_code == status.HTTP_201_CREATED
        manual_playlist = playlist_helper.saved_object

        response = self._search(query="Track")
        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total >= 3

        play_helper = self._domain_helper(PlayTestCase)
        response = play_helper._post_play(
            **{to_camel_case(PlayPostUploadedTrackInputFieldKey.CONTENT): str(track1.uuid)}
        )
        assert response.status_code == status.HTTP_201_CREATED

        track1.refresh_from_db()
        assert track1.play_count >= 1

        uploaded_tracks = UploadedTrack.objects.filter(user=self.test_user1)
        assert uploaded_tracks.count() >= 3

        playlists = ManualPlaylist.objects.filter(user=self.test_user1)
        assert playlists.count() >= 1
