import pytest
from rest_framework import status

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
        # `side` (genre-kit v0.14.0) moved off the shared `Criteria` table onto the
        # `Genre` MTI subtype only -- `Tag` (a `Criteria` proxy) has no such column at
        # all, so passing it is now a plain unexpected-keyword-argument `TypeError`
        # rather than the old runtime `AppValidationException`/DEPENDENCY_MISSING check.
        # "side is genre-only" is enforced by the schema now, not by application code.
        with pytest.raises(TypeError):
            self.model_fixture_factory.create_tag(name="Sport", side="core")
