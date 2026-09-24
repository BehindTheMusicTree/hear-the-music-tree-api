from unittest.mock import patch

from hear.model.album.Album import Album
from hear.test.tests.integration.artist.ArtistTestCase import ArtistTestCase


class TestCase(ArtistTestCase):
    def test_exception_then_rollback(self):
        artist = self.model_fixture_factory.create_artist(name="Muse")
        album_name = "Black Holes and Revelations"
        self.model_fixture_factory.create_album(name=album_name, album_artists=[artist])
        self.model_fixture_factory.create_uploaded_track_with_file(title="Starlight")

        with patch("hear.model.uploaded_track.UploadedTrack.UploadedTrack.delete") as mock_delete:
            exception_message = "Delete failed!"
            mock_delete.side_effect = Exception(exception_message)

            try:
                self._delete_artist(uuid=artist.uuid)
            except Exception as e:
                assert str(e) == exception_message
                assert Album.objects.filter(user=self.test_user1, name=album_name).exists()
