from rest_framework import status

from api.model.artist.Artist import Artist
from api.serializer.model.uploaded_track.input.UploadedTrackInputFieldKey import UploadedTrackInputFieldKey
from api.test.tests.integration.uploaded_track.UploadedTrackTestCase import UploadedTrackTestCase


class TestCase(UploadedTrackTestCase):

    def test_archived_uploaded_track_then_artist_has_plus_1_archived_uploaded_tracks(self):
        artist = self.model_fixture_factory.create_artist(name="Jojo")
        self.model_fixture_factory.create_uploaded_track_with_file(title="not archived 1", artists=[artist])
        self.model_fixture_factory.create_uploaded_track_with_file(title="not archived 2", artists=[artist])
        self.model_fixture_factory.create_uploaded_track_with_file(title="not archived 3", artists=[artist])
        self.model_fixture_factory.create_uploaded_track_with_file(title="archived 1", artists=[artist], archived=True)
        track_love = self.model_fixture_factory.create_uploaded_track_with_file(title="Love", artists=[artist])

        response = self._put_uploaded_track(uuid=track_love.uuid, **{UploadedTrackInputFieldKey.ARCHIVED.value: "true"})

        assert response.status_code == status.HTTP_200_OK
        artists_list: list[Artist] = list(self.saved_object.artists.all())
        assert len(artists_list) > 0
        assert artists_list[0].uploaded_tracks_archived_count == 2

    def test_unarchived_then_artist_has_minus_1_archived_uploaded_tracks(self):
        artist = self.model_fixture_factory.create_artist(name="Jojo")
        self.model_fixture_factory.create_uploaded_track_with_file(title="not archived 1", artists=[artist])
        self.model_fixture_factory.create_uploaded_track_with_file(title="not archived 2", artists=[artist])
        self.model_fixture_factory.create_uploaded_track_with_file(title="not archived 3", artists=[artist])
        self.model_fixture_factory.create_uploaded_track_with_file(title="archived 1", artists=[artist], archived=True)
        track = self.model_fixture_factory.create_uploaded_track_with_file(
            title="Love", artists=[artist], archived=True)

        response = self._put_uploaded_track(uuid=track.uuid, **{UploadedTrackInputFieldKey.ARCHIVED.value: "false"})

        assert response.status_code == status.HTTP_200_OK
        artists_list: list[Artist] = list(self.saved_object.artists.all())
        assert len(artists_list) > 0
        assert artists_list[0].uploaded_tracks_archived_count == 1
