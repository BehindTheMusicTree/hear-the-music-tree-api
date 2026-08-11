from uuid import UUID

from django.db import models
from django.urls import reverse
from rest_framework import status

from api.model.album.Album import Album
from api.test.tests.integration.reference.reference_test_case import ReferenceTestCase
from the_music_tree_api_kit.view.pagination.PaginatedResponseFields import PaginatedResponseFields


class ReferenceAlbumTestCase(ReferenceTestCase):
    def test_reference_album_list_then_200(self):
        self.model_fixture_factory.create_album("tmta_album", user=self._system_user)
        self.model_fixture_factory.create_album("user1_album", user=self.test_user1)
        response = self.api_client.get(path=reverse("reference-album-list"))
        self._assert_all_results_belong_to_tmta(response, Album)

    def test_reference_album_retrieve_then_200(self):
        album = self.model_fixture_factory.create_album("tmta_album", user=self._system_user)
        response = self.api_client.get(path=reverse("reference-album-detail", kwargs={"pk": album.uuid}))
        self._assert_retrieve_result_belongs_to_tmta(response, Album)

    def test_reference_album_destroy_then_204(self):
        album = self.model_fixture_factory.create_album("tmta_album", user=self._system_user)
        response = self.api_client.delete(path=reverse("reference-album-detail", kwargs={"pk": album.uuid}))
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Album.objects.filter(uuid=album.uuid).exists()
