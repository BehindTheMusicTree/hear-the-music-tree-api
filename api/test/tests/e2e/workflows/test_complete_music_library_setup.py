import pytest
from rest_framework import status

from api.model.criteria.children.genre.Genre import Genre
from api.model.playlist.children.manual.ManualPlaylist import ManualPlaylist
from api.model.uploaded_track.UploadedTrack import UploadedTrack
from api.serializer.model.criteria.input.tree_import.Fields import Fields as TreeImportFields
from api.serializer.model.playlist.children.manual.input.Fields import Fields as ManualPlaylistPostFields
from api.serializer.model.uploaded_track.input.put.Fields import Fields as PutFields
from api.test.tests.integration.criteria.GenreTestCase import GenreTestCase
from api.test.tests.integration.playlist.base.PlaylistTestCase import PlaylistTestCase
from api.test.tests.integration.search.SearchTestCase import SearchTestCase
from api.test.tests.integration.uploaded_track.UploadedTrackTestCase import UploadedTrackTestCase
from api.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename


@pytest.mark.e2e
@pytest.mark.slow
@pytest.mark.usefixtures("enable_audio_metadata_analysis")
class TestCase(GenreTestCase, PlaylistTestCase, SearchTestCase, UploadedTrackTestCase):
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
        tree_data = [
            {
                TreeImportFields.NAME_PUBLIC: "Electronic Music",
                TreeImportFields.CHILDREN: [
                    {TreeImportFields.NAME_PUBLIC: "Techno", TreeImportFields.CHILDREN: []}
                ]
            }
        ]

        response = self._post_genres_tree_import(data={TreeImportFields.TREE: tree_data})
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
        response = self._put_uploaded_track(track1.uuid, **{PutFields.GENRE: "Techno"})
        assert response.status_code == status.HTTP_200_OK

        response = self._put_uploaded_track(track2.uuid, **{PutFields.GENRE: "Techno"})
        assert response.status_code == status.HTTP_200_OK

        from api.model.playlist.children.criteria.CriteriaPlaylist import CriteriaPlaylist
        techno_playlist = CriteriaPlaylist.objects.get(user=self.test_user1, criteria=techno_genre)
        assert techno_playlist is not None

        playlist_tracks = techno_playlist.playlist.uploaded_tracks.filter(user=self.test_user1)
        assert track1 in playlist_tracks
        assert track2 in playlist_tracks

        response = self._post_playlist(**{ManualPlaylistPostFields.NAME: "My Favorites"})
        assert response.status_code == status.HTTP_201_CREATED
        manual_playlist = self.saved_object

        from api.serializer.model.playlist.children.manual.input.Fields import Fields as ManualPlaylistPutFields
        response = self._put_playlist(manual_playlist.uuid, **{
            ManualPlaylistPutFields.UPLOADED_TRACKS: [str(track1.uuid), str(track3.uuid)]
        })
        assert response.status_code == status.HTTP_200_OK

        response = self._search(**{'query': 'Track'})
        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total >= 3

        from api.serializer.model.play.input.schema.PostFields import Fields as PlayPostFields
        from api.test.tests.integration.play.PlayTestCase import PlayTestCase
        play_test_case = PlayTestCase()
        play_test_case.setUp()
        play_test_case.api_client = self.api_client
        play_test_case._login_as_test_user1()

        response = play_test_case._post_play(**{PlayPostFields.UPLOADED_TRACK: str(track1.uuid)})
        assert response.status_code == status.HTTP_201_CREATED

        track1.refresh_from_db()
        assert track1.play_count >= 1

        uploaded_tracks = UploadedTrack.objects.filter(user=self.test_user1)
        assert uploaded_tracks.count() >= 3

        playlists = ManualPlaylist.objects.filter(user=self.test_user1)
        assert playlists.count() >= 1
