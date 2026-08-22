from rest_framework import status

from hear.model.playlist.children.criteria.CriteriaPlaylist import CriteriaPlaylist
from hear.test.tests.integration.uploaded_track.UploadedTrackTestCase import UploadedTrackTestCase
from hear.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename


class TestCase(UploadedTrackTestCase):
    def test_no_genre_then_in_genreless_playlists(self):
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_NONE_MP3)

        assert response.status_code == status.HTTP_201_CREATED
        track_playlists = self.saved_object.playlists.all()
        assert len(track_playlists) == 1
        track_criteria_playlists = CriteriaPlaylist.objects.filter(user=self.test_user1, playlist__in=track_playlists)
        assert track_criteria_playlists.filter(user=self.test_user1, criteria=None).exists()
