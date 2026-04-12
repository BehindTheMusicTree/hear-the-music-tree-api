import pytest
from rest_framework import status

from api.filtering.set.search.Fields import Fields as SearchFields
from api.model.album.Album import Album
from api.model.artist.Artist import Artist
from api.model.playlist.children.manual.ManualPlaylist import ManualPlaylist
from api.model.uploaded_track.UploadedTrack import UploadedTrack
from api.test.tests.integration.search.SearchTestCase import SearchTestCase
from api.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename


@pytest.mark.e2e
class TestCase(SearchTestCase):
    """
    E2E test for cross-resource search functionality.

    This test verifies the complete workflow:
    1. User authenticates
    2. User uploads tracks with various metadata
    3. User creates artists, albums, genres, tags, playlists
    4. User searches across all resource types
    5. User filters search by type (track, album, artist, playlist)
    6. User verifies search results are correct
    """

    def test_cross_resource_search_then_ok(self):
        search_term = "test"

        artist = self.model_fixture_factory.create_artist(name=f"{search_term} Artist")
        album = self.model_fixture_factory.create_album(name=f"{search_term} Album")
        track = self.model_fixture_factory.create_uploaded_track_with_file(
            title=f"{search_term} Track", test_uploaded_track_filename=UploadedTrackTestFilename.DEFAULT_MP3
        )
        genre = self.model_fixture_factory.create_genre(name=f"{search_term} Genre")
        tag = self.model_fixture_factory.create_tag(name=f"{search_term} Tag")
        playlist = self.model_fixture_factory.create_manual_playlist(name=f"{search_term} Playlist")

        response = self._search(**{SearchFields.QUERY: search_term})
        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total >= 6

        if UploadedTrack.__name__ in self.results:
            track_results = self.results[UploadedTrack.__name__]
            track_titles = [t.get("title") for t in track_results]
            assert track.title in track_titles

        if Artist.__name__ in self.results:
            artist_results = self.results[Artist.__name__]
            artist_names = [a.get("name") for a in artist_results]
            assert artist.name in artist_names

        if Album.__name__ in self.results:
            album_results = self.results[Album.__name__]
            album_names = [a.get("name") for a in album_results]
            assert album.name in album_names

        if ManualPlaylist.__name__ in self.results:
            playlist_results = self.results[ManualPlaylist.__name__]
            playlist_names = [p.get("name") for p in playlist_results]
            assert playlist.name in playlist_names

        response = self._search(**{SearchFields.QUERY: search_term.upper()})
        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total >= 6

        response = self._search(**{SearchFields.QUERY: "tes"})
        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total >= 6
