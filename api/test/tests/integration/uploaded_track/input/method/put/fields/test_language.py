from rest_framework import status

from api.serializer.model.uploaded_track.input.UploadedTrackInputFieldKey import UploadedTrackInputFieldKey
from api.test.tests.integration.uploaded_track.UploadedTrackTestCase import UploadedTrackTestCase
from api.test.utils.field.body_data.method.PutBodyDataTestCase import PutBodyDataTestCase


class TestCase(UploadedTrackTestCase, PutBodyDataTestCase):
    def test_not_provided_then_unchanged(self):
        language = "Fr"
        uploaded_track = self.model_fixture_factory.create_uploaded_track_with_file(title="Love", language=language)

        response = self._put_uploaded_track(uploaded_track.uuid, **{UploadedTrackInputFieldKey.TITLE.value: "MJ"})

        assert response.status_code == status.HTTP_200_OK
        assert self.saved_object.language == language

    def test_empty_then_none(self):
        uploaded_track = self.model_fixture_factory.create_uploaded_track_with_file(title="Love", language="Fr")

        response = self._put_uploaded_track(uploaded_track.uuid, **{UploadedTrackInputFieldKey.LANGUAGE.value: ""})

        assert response.status_code == status.HTTP_200_OK
        assert self.saved_object.language == None

    def test_provided_then_update(self):
        uploaded_track = self.model_fixture_factory.create_uploaded_track_with_file(title="Love", language="en")

        language = "fr"
        response = self._put_uploaded_track(
            uploaded_track.uuid, **{UploadedTrackInputFieldKey.LANGUAGE.value: language}
        )

        assert response.status_code == status.HTTP_200_OK
        assert self.saved_object.language == language
