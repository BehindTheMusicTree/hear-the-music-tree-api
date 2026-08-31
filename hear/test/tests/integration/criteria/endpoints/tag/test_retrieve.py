import pytest
from rest_framework import status
from the_music_tree_api_kit.exception.validation.app.AppValidationException import AppValidationException
from the_music_tree_api_kit.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode

from hear.serializer.model.criteria.output.CriteriaOutputFieldKey import CriteriaOutputFieldKey
from hear.test.tests.integration.criteria.TagTestCase import TagTestCase


class TestCase(TagTestCase):
    def test_ok(self):
        name = "Sport"
        uuid = self.model_fixture_factory.create_tag(name=name).uuid

        response = self._retrieve_tag(uuid=uuid)

        assert response.status_code == status.HTTP_200_OK
        assert self.result[CriteriaOutputFieldKey.NAME.value] == name

    def test_side_raises_for_tag(self):
        with pytest.raises(AppValidationException) as exc_info:
            self.model_fixture_factory.create_tag(name="Sport", side="core")

        assert exc_info.value.field_validation_error_code == FieldValidationErrorCode.DEPENDENCY_MISSING
