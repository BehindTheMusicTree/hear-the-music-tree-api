import pytest
from rest_framework import status

from api.model.uploaded_track.UploadedTrack import UploadedTrack
from api.serializer.model.criteria.input.post import Fields as PostUploadedTrackInputFieldKey
from api.filtering.set.search.Fields import Fields as SearchUploadedTrackInputFieldKey
from api.serializer.model.uploaded_track.input.UploadedTrackInputFieldKey import UploadedTrackInputFieldKey
from api.test.tests.integration.criteria.GenreTestCase import GenreTestCase
from api.test.tests.integration.search.SearchTestCase import SearchMixin
from api.test.tests.integration.uploaded_track.UploadedTrackTestCase import UploadedTrackTestCase
from api.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename


@pytest.mark.e2e
class TestCase(GenreTestCase, SearchMixin):
    """
    E2E test for search with genre hierarchy.

    This test verifies the complete workflow:
    1. User authenticates
    2. User creates genre hierarchy (Electronic Music > Techno > Minimal Techno)
    3. User uploads tracks tagged with different genres
    4. User searches for tracks by genre name
    5. User verifies search finds tracks in hierarchy
    """

    def test_search_with_genre_hierarchy_then_ok(self):
        parent_genre_name = "Electronic Music"
        child_genre_name = "Techno"
        grandchild_genre_name = "Minimal Techno"

        response = self._post_genre(**{PostUploadedTrackInputFieldKey.NAME_PUBLIC: parent_genre_name})
        assert response.status_code == status.HTTP_201_CREATED
        parent_genre = self.saved_object

        response = self._post_genre(**{PostUploadedTrackInputFieldKey.NAME_PUBLIC: child_genre_name, PostUploadedTrackInputFieldKey.PARENT: parent_genre.uuid})
        assert response.status_code == status.HTTP_201_CREATED
        child_genre = self.saved_object

        response = self._post_genre(**{PostUploadedTrackInputFieldKey.NAME_PUBLIC: grandchild_genre_name,
                                    PostUploadedTrackInputFieldKey.PARENT: child_genre.uuid})
        assert response.status_code == status.HTTP_201_CREATED
        grandchild_genre = self.saved_object

        track_helper = self._domain_helper(UploadedTrackTestCase)
        track1 = self.model_fixture_factory.create_uploaded_track_with_file(
            title="Electronic Minimal Track",
            test_uploaded_track_filename=UploadedTrackTestFilename.DEFAULT_MP3)
        track2 = self.model_fixture_factory.create_uploaded_track_with_file(
            title="Techno Track",
            test_uploaded_track_filename=UploadedTrackTestFilename.DEFAULT_MP3)

        response = track_helper._put_uploaded_track(track1.uuid, **{UploadedTrackInputFieldKey.GENRE.value: grandchild_genre_name})
        assert response.status_code == status.HTTP_200_OK

        response = track_helper._put_uploaded_track(track2.uuid, **{UploadedTrackInputFieldKey.GENRE.value: child_genre_name})
        assert response.status_code == status.HTTP_200_OK

        response = self._search(**{SearchUploadedTrackInputFieldKey.QUERY: "Electronic"})
        assert response.status_code == status.HTTP_200_OK
        assert UploadedTrack.__name__ in self.results
        track_titles = [t.get("title") for t in self.results[UploadedTrack.__name__]]
        assert track1.title in track_titles

        response = self._search(**{SearchUploadedTrackInputFieldKey.QUERY: "Techno"})
        assert response.status_code == status.HTTP_200_OK
        assert UploadedTrack.__name__ in self.results
        track_titles = [t.get("title") for t in self.results[UploadedTrack.__name__]]
        assert track2.title in track_titles

        response = self._search(**{SearchUploadedTrackInputFieldKey.QUERY: "Minimal"})
        assert response.status_code == status.HTTP_200_OK
        assert UploadedTrack.__name__ in self.results
        track_titles = [t.get("title") for t in self.results[UploadedTrack.__name__]]
        assert track1.title in track_titles
