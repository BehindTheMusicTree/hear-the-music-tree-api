from rest_framework import status

from hear.serializer.model.uploaded_track.input.UploadedTrackInputFieldKey import UploadedTrackInputFieldKey
from hear.test.tests.integration.uploaded_track.UploadedTrackTestCase import UploadedTrackTestCase
from hear.test.utils.field.body_data.method.PutBodyDataTestCase import PutBodyDataTestCase


class TestCase(UploadedTrackTestCase, PutBodyDataTestCase):
    def test_not_provided_then_unchanged(self):
        rating = 5
        uploaded_track = self.model_fixture_factory.create_uploaded_track_with_file(title="Korinto", rating=rating)

        response = self._put_uploaded_track(
            uuid=uploaded_track.uuid, **{UploadedTrackInputFieldKey.TITLE.value: "Wech"}
        )

        assert response.status_code == status.HTTP_200_OK
        assert self.saved_object.rating == rating

    def test_provided_then_update(self):
        rating = 0
        uploaded_track = self.model_fixture_factory.create_uploaded_track_with_file(title="Korinto")

        response = self._put_uploaded_track(
            uuid=uploaded_track.uuid, **{UploadedTrackInputFieldKey.RATING.value: rating}
        )

        assert response.status_code == status.HTTP_200_OK
        assert self.saved_object.rating == rating
