from uuid import UUID

from django.db import models
from django.urls import reverse
from rest_framework import status

from api.model.artist.Artist import Artist
from api.test.tests.integration.reference.base import ReferenceTestCase
from api.view.pagination.PaginatedResponseFields import PaginatedResponseFields


class ReferenceArtistTestCase(ReferenceTestCase):
    def test_reference_artist_list_then_200(self):
        self.model_fixture_factory.create_artist("tmta_artist", user=self._system_user)
        self.model_fixture_factory.create_artist("user1_artist", user=self.test_user1)
        response = self.api_client.get(path=reverse('reference-artist-list'))
        self._assert_all_results_belong_to_tmta(response, Artist)
