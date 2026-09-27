from rest_framework import status

from hear.serializer.model.uploaded_track.input.UploadedTrackInputFieldKey import UploadedTrackInputFieldKey
from hear.test.tests.integration.uploaded_track.UploadedTrackTestCase import UploadedTrackTestCase


class TestCase(UploadedTrackTestCase):
    def test_archived_uploaded_track_then_criteria_has_plus_1_archived_uploaded_tracks(self):
        criteria = self.model_fixture_factory.create_genre(name="Jojo")
        self.model_fixture_factory.create_uploaded_track_with_file(title="not archived 1", genre=criteria)
        self.model_fixture_factory.create_uploaded_track_with_file(title="not archived 2", genre=criteria)
        self.model_fixture_factory.create_uploaded_track_with_file(title="not archived 3", genre=criteria)
        self.model_fixture_factory.create_uploaded_track_with_file(title="archived 1", genre=criteria, archived=True)
        self.model_fixture_factory.create_uploaded_track_with_file(title="archived 2", genre=criteria, archived=True)
        self.model_fixture_factory.create_uploaded_track_with_file(title="archived 3", genre=criteria, archived=True)
        track_love = self.model_fixture_factory.create_uploaded_track_with_file(title="Love", genre=criteria)
        data = {UploadedTrackInputFieldKey.ARCHIVED.value: "true"}
        response = self._put_uploaded_track(uuid=track_love.uuid, **data)
        assert response.status_code == status.HTTP_200_OK
        assert self.saved_object.genre and self.saved_object.genre.uploaded_tracks_archived_count == 4

    def test_unarchived_then_criteria_has_minus_1_archived_uploaded_tracks(self):
        criteria = self.model_fixture_factory.create_genre(name="Jojo")
        self.model_fixture_factory.create_uploaded_track_with_file(title="not archived 1", genre=criteria)
        self.model_fixture_factory.create_uploaded_track_with_file(title="not archived 2", genre=criteria)
        self.model_fixture_factory.create_uploaded_track_with_file(title="not archived 3", genre=criteria)
        self.model_fixture_factory.create_uploaded_track_with_file(title="archived 1", genre=criteria, archived=True)
        self.model_fixture_factory.create_uploaded_track_with_file(title="archived 2", genre=criteria, archived=True)
        track = self.model_fixture_factory.create_uploaded_track_with_file(title="Love", genre=criteria, archived=True)
        data = {UploadedTrackInputFieldKey.ARCHIVED.value: "false"}
        response = self._put_uploaded_track(uuid=track.uuid, **data)
        assert response.status_code == status.HTTP_200_OK
        assert self.saved_object.genre and self.saved_object.genre.uploaded_tracks_archived_count == 2
