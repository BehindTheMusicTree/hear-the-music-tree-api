from rest_framework import status
from the_music_tree_api_kit.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode

from hear.serializer.model.criteria.input.post import Fields as PostFields
from hear.test.tests.integration.criteria.GenreTestCase import GenreTestCase


class TestCase(GenreTestCase):
    def test_extra_field_then_400_bad_request(self):
        extra_field = "extraField"
        response = self._post_genre(**{PostFields.NAME_PUBLIC: "Rock", extra_field: "extra_value"})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error["field"] == extra_field
        assert error["code"] == FieldValidationErrorCode.UNKNOWN
