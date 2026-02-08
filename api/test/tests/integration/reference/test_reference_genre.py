
from django.urls import reverse
from rest_framework import status

from api.model.criteria.children.genre.Genre import Genre
from api.test.tests.integration.reference.reference_test_case import ReferenceTestCase


class ReferenceGenreTestCase(ReferenceTestCase):
    def test_reference_genre_list_then_200(self):
        self.model_fixture_factory.create_genre("tmta_genre", user=self._system_user)
        self.model_fixture_factory.create_genre("user1_genre", user=self.test_user1)
        response = self.api_client.get(path=reverse('reference-genre-list'))
        self._assert_all_results_belong_to_tmta(response, Genre)

    def test_reference_genre_retrieve_then_200(self):
        genre = self.model_fixture_factory.create_genre("tmta_genre", user=self._system_user)
        response = self.api_client.get(path=reverse('reference-genre-detail', kwargs={'pk': genre.uuid}))
        self._assert_retrieve_result_belongs_to_tmta(response, Genre)

    def test_reference_genre_destroy_then_204(self):
        genre = self.model_fixture_factory.create_genre("tmta_genre", user=self._system_user)
        response = self.api_client.delete(path=reverse('reference-genre-detail', kwargs={'pk': genre.uuid}))
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Genre.objects.filter(uuid=genre.uuid).exists()

    def test_reference_genre_create_then_201(self):
        response = self.api_client.post(path=reverse('reference-genre-list'), data={'name': 'test_reference_genre'})
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        genre = Genre.objects.get(uuid=data['uuid'])
        assert genre.name == 'test_reference_genre'
        assert genre.user == self._system_user

    def test_load_example_tree_then_201(self):
        response = self.api_client.post(path=reverse('reference-genre-load-example-tree'))
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data['message'] == "Example genre tree loaded successfully"
