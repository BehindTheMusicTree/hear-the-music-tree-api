from uuid import UUID

from django.db import models
from django.urls import reverse
from rest_framework import status

from api.model.uploaded_track.UploadedTrack import UploadedTrack
from api.test.tests.integration.reference.reference_test_case import ReferenceTestCase
from api.view.pagination.PaginatedResponseFields import PaginatedResponseFields


class ReferenceUploadedTrackTestCase(ReferenceTestCase):
    def test_reference_uploaded_track_list_then_200(self):
        self.model_fixture_factory._create_uploaded_track(user=self._system_user, title="tmta track")
        self.model_fixture_factory._create_uploaded_track(user=self.test_user1, title="user1 track")
        response = self.api_client.get(path=reverse("reference-uploaded-track-list"))
        self._assert_all_results_belong_to_tmta(response, UploadedTrack)
