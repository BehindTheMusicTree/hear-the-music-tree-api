from uuid import UUID

from django.db import models
from django.urls import reverse
from rest_framework import status

from api.model.criteria.children.genre.Genre import Genre
from api.test.tests.integration.reference.base import ReferenceTestCase
from api.view.pagination.PaginatedResponseFields import PaginatedResponseFields


class ReferenceGenreTestCase(ReferenceTestCase):
    def test_reference_genre_list_then_200(self):
        self.model_fixture_factory.create_genre("tmta_genre", user=self._system_user)
        self.model_fixture_factory.create_genre("user1_genre", user=self.test_user1)
        response = self.api_client.get(path=reverse('reference-genre-list'))
        self._assert_all_results_belong_to_tmta(response, Genre)
