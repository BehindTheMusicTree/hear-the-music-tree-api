from uuid import UUID

from django.db import models
from django.urls import reverse
from rest_framework import status

from api.model.play.Play import Play
from api.test.tests.integration.reference.reference_test_case import ReferenceTestCase
from api.view.pagination.PaginatedResponseFields import PaginatedResponseFields


class ReferencePlayTestCase(ReferenceTestCase):
    def test_reference_play_list_then_200(self):
        response = self.api_client.get(path=reverse("reference-play-list"))
        self._assert_all_results_belong_to_tmta(response, Play)
