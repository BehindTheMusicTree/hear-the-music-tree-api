import os
from uuid import UUID

from django.contrib.auth.hashers import make_password
from django.db import models
from django.urls import reverse
from rest_framework import status

from api.model.uploaded_track.UploadedTrack import UploadedTrack
from api.model.user.User import User
from api.test.utils.AppTestCase import AppTestCase
from api.view.pagination.PaginatedResponseFields import PaginatedResponseFields


SYSTEM_USER_USERNAME = "test_reference_system_user"


class ReferenceUploadedTrackTestCase(AppTestCase):
    def setUp(self):
        super().setUp()
        self._logout()

        self._system_user, created = User.objects.get_or_create(
            username=SYSTEM_USER_USERNAME,
            defaults={
                "is_system": True,
                "is_active": True,
                "is_staff": False,
                "is_superuser": False,
                "email": "system@test.com",
                "is_test_user": True,
                "password": make_password(None),
            },
        )
        if created or not self._system_user.password.startswith("!"):
            self._system_user.set_unusable_password()
            self._system_user.save(update_fields=["password"])
        self._original_tmta_username = os.environ.get("TMTA_USERNAME")
        os.environ["TMTA_USERNAME"] = SYSTEM_USER_USERNAME

    def tearDown(self):
        if self._original_tmta_username is not None:
            os.environ["TMTA_USERNAME"] = self._original_tmta_username
        elif "TMTA_USERNAME" in os.environ:
            del os.environ["TMTA_USERNAME"]
        super().tearDown()

    def _assert_all_results_belong_to_tmta(
        self, response, model_class: type[models.Model], uuid_field: str = "uuid"
    ) -> None:
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

    def test_reference_uploaded_track_list_then_200(self):
        self.model_fixture_factory._create_uploaded_track(user=self._system_user, title="tmta track")
        self.model_fixture_factory._create_uploaded_track(user=self.test_user1, title="user1 track")
        response = self.api_client.get(path=reverse('reference-uploaded-track-list'))
        self._assert_all_results_belong_to_tmta(response, UploadedTrack)
