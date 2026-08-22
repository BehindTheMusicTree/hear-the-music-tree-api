from rest_framework import status

from hear.serializer.model.criteria.input.post import Fields as PostFields
from hear.test.tests.integration.criteria.TagTestCase import TagTestCase


class TestCase(TagTestCase):
    def test_ok(self):
        tag_name = "Sport"
        response = self._post_tag(**{PostFields.NAME_PUBLIC: tag_name})

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.name == tag_name
