from uuid import UUID

from django.db import models
from django.urls import reverse
from rest_framework import status
from the_music_tree_api_kit.view.pagination.PaginatedResponseFields import PaginatedResponseFields

from api.model.artist.Artist import Artist
from api.test.tests.integration.reference.reference_test_case import ReferenceTestCase


class ReferenceArtistTestCase(ReferenceTestCase):
    def test_reference_artist_list_then_200(self):
        self.model_fixture_factory.create_artist("tmta_artist", user=self._system_user)
        self.model_fixture_factory.create_artist("user1_artist", user=self.test_user1)
        response = self.api_client.get(path=reverse("reference-artist-list"))
        self._assert_all_results_belong_to_tmta(response, Artist)

    def test_reference_artist_retrieve_then_200(self):
        artist = self.model_fixture_factory.create_artist("tmta_artist", user=self._system_user)
        response = self.api_client.get(path=reverse("reference-artist-detail", kwargs={"pk": artist.uuid}))
        self._assert_retrieve_result_belongs_to_tmta(response, Artist)

    def test_reference_artist_destroy_then_204(self):
        artist = self.model_fixture_factory.create_artist("tmta_artist", user=self._system_user)
        response = self.api_client.delete(path=reverse("reference-artist-detail", kwargs={"pk": artist.uuid}))
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Artist.objects.filter(uuid=artist.uuid).exists()
