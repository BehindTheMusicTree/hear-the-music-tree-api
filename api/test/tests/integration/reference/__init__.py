from uuid import UUID

from django.db import models
from rest_framework import status

from api.test.utils.AppTestCase import AppTestCase
from api.view.pagination.PaginatedResponseFields import PaginatedResponseFields


class ReferenceTestCase(AppTestCase):
    """Base test case for reference endpoint tests that require system user setup."""

    SYSTEM_USER_USERNAME = "test_reference_system_user"

    def setUp(self):
        super().setUp()
        self._logout()
        self._system_user = self._setup_system_user_for_reference_tests(self.SYSTEM_USER_USERNAME)

    def _assert_all_results_belong_to_tmta(
        self, response, model_class: type[models.Model], uuid_field: str = "uuid"
    ) -> None:
        """Assert that all results in the response belong to the system user (TMTA)."""
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        results = data.get(PaginatedResponseFields.RESULTS, [])
        for item in results:
            obj_uuid = item.get(uuid_field)
            if obj_uuid is None:
                continue
            obj = model_class.objects.get(**{uuid_field: UUID(str(obj_uuid))
                                          if isinstance(obj_uuid, str) else obj_uuid})
            assert getattr(obj, "user_id") == self._system_user.id
