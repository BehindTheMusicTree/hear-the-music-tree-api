from uuid import UUID

from django.db import models
from django.urls import reverse
from rest_framework import status

from api.model.album.Album import Album
from api.test.tests.integration.reference.base import ReferenceTestCase
from api.view.pagination.PaginatedResponseFields import PaginatedResponseFields


class ReferenceAlbumTestCase(ReferenceTestCase):
    def test_reference_album_list_then_200(self):
        self.model_fixture_factory.create_album("tmta_album", user=self._system_user)
        self.model_fixture_factory.create_album("user1_album", user=self.test_user1)
        response = self.api_client.get(path=reverse('reference-album-list'))
        self._assert_all_results_belong_to_tmta(response, Album)
